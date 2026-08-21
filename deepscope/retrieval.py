"""Local document grounding: PDF chunking plus a dependency-free BM25 index.

BM25 keeps uploads instant (no embedding model download, no vector server) which
matters when the whole flow has to run live in front of judges.
"""

import math
import re
from collections import Counter
from dataclasses import dataclass, field

_TOKEN = re.compile(r"[a-z0-9]+")
_K1 = 1.5
_B = 0.75


def tokenize(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


@dataclass
class Chunk:
    text: str
    document: str
    page: int
    score: float = 0.0


@dataclass
class DocumentIndex:
    """Small in-memory BM25 index over PDF chunks."""

    chunks: list[Chunk] = field(default_factory=list)
    _tokens: list[list[str]] = field(default_factory=list)
    _df: Counter[str] = field(default_factory=Counter)

    @property
    def is_empty(self) -> bool:
        return not self.chunks

    @property
    def documents(self) -> list[str]:
        seen: list[str] = []
        for chunk in self.chunks:
            if chunk.document not in seen:
                seen.append(chunk.document)
        return seen

    def add_pdf(self, path: str, name: str, chunk_size: int = 1100, overlap: int = 150) -> int:
        from pypdf import PdfReader

        reader = PdfReader(path)
        added = 0
        for page_number, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or "").strip()
            if not text:
                continue
            for piece in _split(text, chunk_size, overlap):
                self._add_chunk(Chunk(text=piece, document=name, page=page_number))
                added += 1
        return added

    def add_text(self, text: str, name: str, page: int = 1) -> None:
        self._add_chunk(Chunk(text=text, document=name, page=page))

    def _add_chunk(self, chunk: Chunk) -> None:
        tokens = tokenize(chunk.text)
        self.chunks.append(chunk)
        self._tokens.append(tokens)
        self._df.update(set(tokens))

    def search(self, query: str, k: int = 3) -> list[Chunk]:
        """Return the k best-matching chunks for a natural language query."""
        if self.is_empty:
            return []
        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        total = len(self._tokens)
        avg_len = sum(len(tokens) for tokens in self._tokens) / total
        scored: list[Chunk] = []
        for chunk, tokens in zip(self.chunks, self._tokens):
            counts = Counter(tokens)
            length = len(tokens) or 1
            score = 0.0
            for term in query_tokens:
                frequency = counts.get(term, 0)
                if not frequency:
                    continue
                idf = math.log(1 + (total - self._df[term] + 0.5) / (self._df[term] + 0.5))
                norm = frequency * (_K1 + 1)
                denom = frequency + _K1 * (1 - _B + _B * length / avg_len)
                score += idf * norm / denom
            if score > 0:
                scored.append(
                    Chunk(text=chunk.text, document=chunk.document, page=chunk.page, score=score)
                )

        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:k]


def _split(text: str, chunk_size: int, overlap: int) -> list[str]:
    pieces: list[str] = []
    start = 0
    step = max(chunk_size - overlap, 1)
    while start < len(text):
        pieces.append(text[start : start + chunk_size].strip())
        start += step
    return [piece for piece in pieces if piece]
