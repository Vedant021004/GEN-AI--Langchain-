"""Terminal runner: python -m deepscope.cli "your question" [--pdf file.pdf]"""

import argparse
import sys

from deepscope.config import load_settings
from deepscope.graph import stream_research
from deepscope.retrieval import DocumentIndex


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="DeepScope research agent")
    parser.add_argument("question")
    parser.add_argument("--pdf", action="append", default=[], help="PDF to research against")
    parser.add_argument("--rounds", type=int, default=2)
    args = parser.parse_args(argv)

    settings = load_settings()
    if settings.missing:
        print(f"Missing environment variables: {', '.join(settings.missing)}", file=sys.stderr)
        return 1
    settings.max_rounds = args.rounds

    index = DocumentIndex()
    for path in args.pdf:
        chunks = index.add_pdf(path, path.split("/")[-1])
        print(f"[index] {path}: {chunks} chunks")

    report = ""
    for node, payload in stream_research(args.question, settings, index):
        for entry in payload.get("log", []):
            print(f"[{node}] {entry}")
        if payload.get("report"):
            report = payload["report"]

    print("\n" + report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
