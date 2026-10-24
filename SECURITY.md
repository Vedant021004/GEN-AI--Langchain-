# Security review

Scope: full repository scan for hardcoded secrets, SQL injection, unvalidated input,
vulnerable dependencies, permissive CORS/CSRF settings, exposed debug surfaces and
missing authorization. Findings below are ordered by severity; items marked **Fixed**
are addressed in this repository, the rest are recommendations.

## Critical

### 1. Hardcoded MySQL root credentials — **Fixed**
`AAPROJECT/sql_agent.py` connected with `mysql+pymysql://root:ved%40nt@127.0.0.1:3306/analyzer_ai`,
committing the database root password (`ved@nt`) to git history. The connection string now
comes from the `DATABASE_URI` environment variable (`.env`, see `.env.example`) and the script
fails fast if it is missing.

**Action still required by the repository owner:** the password remains in git history, so it
must be considered compromised — rotate the MySQL root password (and use a non-root account
with only the privileges the agent needs).

### 2. CORS and CSRF protection disabled — **Fixed**
`.devcontainer/devcontainer.json` started Streamlit with
`--server.enableCORS false --server.enableXsrfProtection false`. Together these allow any
website to issue cross-origin requests to the running app and remove XSRF token validation,
so a visited page can drive the chatbot (and its tools) on the victim's behalf. Both flags
were removed so Streamlit's defaults apply.

### 3. Cross-session data leakage in the deployed Streamlit apps — **Fixed**
Two separate issues in `TOOLS/app.py`:
- The uploaded PDF's vector store and chunk text lived in `APP_STATE`, a module-level global.
  In a deployed multi-user Streamlit app the module is shared by all visitors, so one user's
  uploaded document was retrievable by every other user. Each browser session now owns its
  document store and the retrieval tool closes over that per-session store (the original
  reason for the global — tools running off the main thread cannot read `st.session_state` —
  is preserved because the store is a plain dict captured in the closure).
- The checkpointer thread id was the constant `"1"` in `TOOLS/app.py` and `FAST-AI/AI.py`, so
  all concurrent users shared one conversation memory. Each session now gets a random UUID
  thread id.

## High

### 4. Vulnerable pinned dependencies — partially **Fixed**
`TOOLS/requirements.txt` (OSV scan of all 172 pins):

| Package | Was | Now | Advisories |
| --- | --- | --- | --- |
| aiohttp | 3.14.1 | 3.14.3 | GHSA-cq5v-8q36-5273 (high, OOB heap read in HTTP parser), GHSA-mfx4-hv73-q22v (request smuggling), GHSA-mq44-7p77-q5h7 |
| GitPython | 3.1.51 | 3.1.59 | GHSA-3f7w-8rr8-f37f, GHSA-wvpp-8hx9-p66j (high, unguarded git option forwarding) |
| pypdf | 6.14.2 | 6.16.1 | GHSA-fp3f-mc75-235c, GHSA-fwg2-594c-jp42 (DoS on malicious PDFs — reachable, the apps parse user-uploaded PDFs) |
| chromadb | 1.5.9 | 1.5.9 (no fix published) | GHSA-f4j7-r4q5-qw2c (critical, pre-auth code injection in the Chroma *server* `create collection` endpoint via `trust_remote_code`) |

The chromadb advisory has no fixed release yet. This code only uses embedded/in-process
Chroma, so the vulnerable HTTP endpoint is not exposed; do **not** run `chroma run` as a
network-reachable server until a fixed version ships.

### 5. No authentication on the deployed app — not fixed (design decision)
The Streamlit app is publicly reachable (see `.github/workflows/keep_alive.yml`, which pings
`https://genniacqcxj6xbjrk9niak.streamlit.app/`) and has no login. Anyone can upload PDFs and
spend the owner's Groq/Serper API quota. If that matters, put the app behind Streamlit
Community Cloud's viewer restrictions or add a shared-secret gate before the chat UI.

## Medium

### 6. SQL agents have unrestricted database write access
`SQL-Agent/Agent.py` and `AAPROJECT/sql_agent.py` hand a `SQLDatabaseToolkit` free-form user
input. There is no classic string-concatenation SQL injection in the repository — no query is
built with f-strings or `%` formatting — but the LLM itself generates arbitrary SQL from
untrusted prompts, so "drop the tasks table" or a prompt-injected instruction inside retrieved
content executes as-is; the system prompt is not a security control. Recommended hardening
(not applied, since it changes intended behaviour):
- connect as a user restricted to the intended tables and, where the app is read-only, grant
  `SELECT` only;
- pass `include_tables=[...]` to `SQLDatabase.from_uri` so the agent cannot touch other tables;
- require a human confirmation step before `INSERT`/`UPDATE`/`DELETE`.

### 7. Committed local databases, vector stores and pickles — **Fixed**
`my_tasks.db`, `chroma_db/`, `hf_vector_db/`, `vectorchroma_db/` and
`LANGGRAPH-MULTI/.langgraph_api/*.pckl` were tracked in git. These hold whatever was ingested
locally (document text, task rows, conversation checkpoints), and the `.pckl` files are
`pickle` data — loading a pickle from an untrusted source executes arbitrary code, so
distributing them via the repository is unsafe. They are now untracked and ignored.
They remain in git history; purge them with `git filter-repo` if any of the content was
sensitive.

### 8. Raw exception text rendered in the UI — **Fixed**
`TOOLS/app.py` and `FAST-AI/AI.py` displayed `str(e)` from the agent call directly to the
user; provider errors can include request URLs, headers or key fragments. Both now log the
traceback server-side and show a generic message.

## Low

### 9. `st.secrets["GROQ_API_KEY"]` with no fallback — **Fixed**
`TOOLS/app.py` raised a `KeyError` (with a stack trace) when secrets were absent. It now falls
back to the `GROQ_API_KEY` environment variable and shows a clear configuration error.

### 10. Debug panel exposes retrieved context
The `TOOLS/app.py` sidebar "Show retrieved context" toggle dumps raw retrieved chunks. It is
now limited to the viewer's own session (see finding 3), so this is informational only;
disable it in production if PDF content is sensitive.

### 11. Personal data in the repository
`Vedant_Kapil_Resume.pdf` is committed and used as demo input by `TOOLS/RAG.PY`. It contains
personal contact details — intentional or not, note that it is public.

## Verified clean
- No hardcoded API keys or tokens in source: every provider key is read via `os.getenv` /
  `load_dotenv` / `st.secrets`, and no `.env` file was ever committed (checked across all
  branches).
- No `eval`, `exec`, `os.system`, `subprocess`, `shell=True`, `pickle.load` on untrusted input
  or `verify=False` anywhere in the Python sources.
- No string-interpolated SQL queries.
