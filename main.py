#!/usr/bin/env python3
"""Copy the competition entry image into the output directory.

The finished image ships in this repository as ``entry.png`` next to
this file.  This program writes an exact byte-for-byte copy of it to
``/output/entry.png``, the artifact the competition grades.

Standard library only, no network access.  The output is deterministic:
the same input bytes always produce the same output bytes.

The output directory can be overridden with the MAKEFUN_OUTPUT_DIR
environment variable (the kit's own convention); it defaults to /output.
"""

import hashlib
import os
import pathlib
import sys

SOURCE_NAME = "entry.png"
OUTPUT_DIR = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> int:
    repo_root = pathlib.Path(__file__).resolve().parent
    source = repo_root / SOURCE_NAME
    target = OUTPUT_DIR / SOURCE_NAME

    target.parent.mkdir(parents=True, exist_ok=True)

    image = source.read_bytes()
    target.write_bytes(image)

    digest = hashlib.sha256(image).hexdigest()
    print(f"wrote {target} ({len(image)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
