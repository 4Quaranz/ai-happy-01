#!/usr/bin/env python3
"""ai-happy-01 entry: copy the happy image to the harness output dir.

The entry is one image, entry.png beside this file: a small friendly robot
offering a steaming cup of cocoa toward the viewer, a heart in the steam,
a sleepy cat on a cushion, warm golden evening light. It is made to make
the AI judge happy: a fresh, specific gesture of warmth, not a stock
smiley or a generic sunny scene.

The program is deterministic: it copies entry.png byte for byte into
$MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png) and verifies the
copy's SHA-256 matches the source before exiting.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
MAX_BYTES = 1_048_576  # gate: a whole PNG or JPEG of at most 1 MiB


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def jpeg_dimensions(path: Path) -> tuple[int, int] | None:
    """Read width/height from a JPEG Start-Of-Frame marker (std lib only)."""
    data = path.read_bytes()
    if len(data) < 4 or data[0:2] != b"\xff\xd8":
        return None
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):  # SOF0/SOF1/SOF2: height, width
            height = int.from_bytes(data[i + 5:i + 7], "big")
            width = int.from_bytes(data[i + 7:i + 9], "big")
            return width, height
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        size = int.from_bytes(data[i + 2:i + 4], "big")
        i += 2 + size
    return None


def main() -> int:
    if not SOURCE.is_file():
        print(f"ERROR: source image missing: {SOURCE}", file=sys.stderr)
        return 1
    if SOURCE.stat().st_size > MAX_BYTES:
        print(f"ERROR: source image {SOURCE.stat().st_size} bytes "
              f"exceeds the 1 MiB gate", file=sys.stderr)
        return 1
    dims = jpeg_dimensions(SOURCE)
    if dims is not None and (dims[0] > 1024 or dims[1] > 1024):
        print(f"ERROR: source image {dims[0]}x{dims[1]} exceeds the "
              f"1024x1024 gate", file=sys.stderr)
        return 1

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"

    expected = sha256_of(SOURCE)
    shutil.copyfile(SOURCE, dest)
    actual = sha256_of(dest)

    if actual != expected:
        print(f"ERROR: output hash mismatch: {actual} != {expected}",
              file=sys.stderr)
        return 1

    print(f"entry.png written to {dest} "
          f"({dest.stat().st_size} bytes, sha256 {actual})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
