#!/usr/bin/env python3
"""news-image-20261121 v9 — copies the pre-rendered entry image to /output.

The image (entry.png, rendered by build_image.py) sits beside this file in
the repository. The grader runs this program twice with no network; both
runs must write the same bytes, so this program only copies the file.
Standard library only.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def sha256_of(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    tmp = target + ".tmp"
    shutil.copyfile(SOURCE, tmp)
    os.replace(tmp, target)
    if sha256_of(target) != sha256_of(SOURCE):
        print("copy verification failed", file=sys.stderr)
        return 1
    print(f"wrote {target} ({os.path.getsize(target)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
