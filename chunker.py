"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks

import re

def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents into chunks using a structure-aware strategy.

    Design choices, based on the campus_life corpus:
      - Documents are short posts, so a post that fits within CHUNK_SIZE
        stays whole as a single chunk.
      - The first line of a post is a title that states its topic, so for
        posts that do get split, the title is prepended to every chunk.
      - Splitting on paragraph breaks (then sentences, then a hard cut as a
        last resort) keeps more complete thoughts intact than cutting at a
        character count.

    CHUNK_SIZE is a hard ceiling on the whole chunk, title included, so no
    chunk is ever longer than CHUNK_SIZE. Chunks may be shorter. Each new
    chunk starts with up to CHUNK_OVERLAP characters of whole units carried
    over from the end of the previous chunk.

    Every chunk is tagged produced_by="chunker.py::split_documents" so the
    README's Sample Chunks section names the right function.
    `app.py chunks` prints that string.
    """
    max_chars = config.CHUNK_SIZE
    overlap = config.CHUNK_OVERLAP
    chunks: list[Chunk] = []

    def size(parts: list[str]) -> int:
        return len("\n".join(parts))

    for doc in documents:
        text = doc.text.strip()
        if not text:
            continue

        if len(text) <= max_chars:
            pieces = [text]
        else:
            first_line, _, rest = text.partition("\n")
            title = first_line.strip()
            body = rest.strip()

            if not body:
                # Only a title, nothing to split: plain windows.
                step = max(max_chars - overlap, 1)
                pieces = [title[i : i + max_chars] for i in range(0, len(title), step)]
            else:
                # Room for body text once "title\n\n" is added back.
                budget = max_chars - (len(title) + 2)

                # Overlap must stay below the budget or chunks can't advance.
                ov = min(overlap, budget // 4)

                # 1. Break the body into units: paragraphs, then sentences,
                #    then a hard cut if a single sentence is still too long.
                units: list[str] = []
                for para in re.split(r"\n\s*\n", body):
                    para = para.strip()
                    if not para:
                        continue
                    if len(para) <= budget:
                        units.append(para)
                        continue
                    for sent in re.split(r"(?<=[.!?])\s+", para):
                        if len(sent) <= budget:
                            units.append(sent)
                        else:
                            step = max(budget - ov, 1)
                            units.extend(
                                sent[i : i + budget] for i in range(0, len(sent), step)
                            )

                # 2. Pack units up to budget, seeding each new chunk with
                #    trailing units from the previous one (the overlap).
                bodies: list[str] = []
                current: list[str] = []
                for unit in units:
                    if current and size(current + [unit]) > budget:
                        bodies.append("\n".join(current))

                        tail: list[str] = []
                        for u in reversed(current):
                            if size([u] + tail) > ov:
                                break
                            tail.insert(0, u)

                        current = tail
                        if size(current + [unit]) > budget:
                            current = []
                    current.append(unit)
                if current:
                    bodies.append("\n".join(current))

                pieces = [f"{title}\n\n{b}" for b in bodies]

        for i, piece in enumerate(pieces):
            chunks.append(
                Chunk(
                    text=piece,
                    source=doc.source,
                    index=i,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
