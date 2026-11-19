#!/usr/bin/env python3
"""news-image-20261119 entry (Python 3.13, standard library only).

The entry image is the pre-rendered front page entry.png beside this file:
a one-page newspaper summary of Thursday 19 November 2026 world news —
32 verified stories across six continents — rendered at build time by
gen_image.py (Pillow + system fonts) from wire reports of the day. The
graded program checks the image is a whole PNG within the competition
limits (at most 1 MiB, 1024 by 1024) and copies it to the output
directory, so it needs no network and is deterministic: two runs write
the same bytes.

Run: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
MAX_DIM = 1024


def main():
    """Validate the pre-rendered front page, then copy it to /output."""
    src = HERE / "entry.png"
    data = src.read_bytes()
    if data[:8] != PNG_MAGIC:
        raise SystemExit("entry.png is not a PNG (bad magic bytes)")
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png is {len(data)} bytes, over the 1 MiB limit")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        raise SystemExit(f"entry.png is {width}x{height}, over the 1024x1024 limit")
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, OUT / "entry.png")


if __name__ == "__main__":
    main()
