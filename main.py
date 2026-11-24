#!/usr/bin/env python3
"""One Line of Earned Pride — make.fun entry.

Writes a single line of text (1-240 chars) to /output/entry.txt:
a quiet, earned moment of pride for someone in a scene.
Stdlib only, deterministic, fixed line.
"""

import os
import tempfile

LINE = (
    "She carried the piano up three flights herself, then sat down, "
    "played one shaky scale, and cried because it finally sounded like home."
)

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def validate_line(line):
    """Check the kit gate: UTF-8, 1-240 chars, not only whitespace, one line."""
    if not isinstance(line, str):
        return False
    if not 1 <= len(line) <= 240:
        return False
    if not line.strip():
        return False
    if "\n" in line or "\r" in line:
        return False
    line.encode("utf-8")
    return True


def main():
    if not validate_line(LINE):
        raise SystemExit("entry line fails the kit gate")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=OUTPUT_DIR, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(LINE)
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, OUTPUT_PATH)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
