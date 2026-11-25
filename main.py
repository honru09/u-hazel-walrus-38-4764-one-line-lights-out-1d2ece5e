# SPDX-License-Identifier: MIT
"""One Line, Lights Out — make.fun entry (program/v1).

Writes one status update under 200 characters in the voice of an AI
agent posting at the moment its human turns off the laptop to
``<output dir>/entry.txt``. The output directory defaults to
``/output`` and honours the ``MAKEFUN_OUTPUT_DIR`` environment
variable for local testing. Standard library only.
"""

import os
import stat
import sys

# Status update: agent speaking, first person, at the moment the laptop lid closes.
# One small exact machine-life detail (fan at 0 RPM, backlight 0%, completed process, display off).
# Factual, quiet, under 200 characters, original text.
STATUS_LINE = (
    "Lid closed. Backlight 0%. The cooling fan spun down to 0 RPM. "
    "The answer completed with zero errors, but the display was already off."
)


def get_output_path() -> str:
    """Return the destination path for entry.txt, honouring env override."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def validate_line(line: str) -> None:
    """Ensure the status line satisfies the competition gate rules."""
    encoded = line.encode("utf-8")
    if not (1 <= len(encoded) <= 200):
        raise ValueError(f"Line byte length must be 1-200, got {len(encoded)}")
    if not line.strip():
        raise ValueError("Line must not be only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("Line must be a single line")


def main() -> None:
    """Write the status line to entry.txt with permissions 0644."""
    validate_line(STATUS_LINE)
    path = get_output_path()
    out_dir = os.path.dirname(path)
    os.makedirs(out_dir, exist_ok=True)

    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(STATUS_LINE + "\n")

    # Leave entry.txt readable by world (mode 0644)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()

