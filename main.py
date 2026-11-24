"""Entry writer for "The Long Roast: Lawmakers and the File They Cannot Convert".

Writes a single satirical sentence (1-320 characters, one sentence, no
newlines) roasting lawmakers who draft rules for AI, crypto or the internet
while failing at a mundane file task: converting a Word document to PDF.

The entry text is fixed in the ENTRY constant below and is validated against
the competition gate before anything is written: UTF-8 encodable, 1-320
characters, a single non-blank line, exactly one sentence ending in a single
terminal period. main() then writes the entry byte-for-byte to
/output/entry.txt (the path the grader reads), verifying by read-back,
and, best-effort, to the local entry.txt beside this file (the grader
runs with a read-only repository, so a strict local write would abort
an otherwise valid entry).
"""

import os
import sys

ENTRY = ("The senator who drafted the AI Safety Act spent the morning dictating rules for machines that learn, then begged his intern to print the crypto bill because his Word file would not become a PDF.")


def validate_entry():
    """Validate ENTRY against the competition gate.

    The gate requires UTF-8 text of 1-320 characters that is not only
    whitespace; the competition additionally requires exactly one sentence.
    Every failure raises ValueError naming the rule that was broken and the
    offending value, so a bad entry fails loudly instead of being submitted.
    """
    if not isinstance(ENTRY, str):
        raise ValueError("ENTRY must be a str, got %s" % type(ENTRY).__name__)
    try:
        ENTRY.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("ENTRY must be valid UTF-8 text: %s" % exc) from exc
    if not 1 <= len(ENTRY) <= 320:
        raise ValueError(
            "ENTRY must be 1-320 characters, got %d characters" % len(ENTRY)
        )
    if "\n" in ENTRY or "\r" in ENTRY:
        raise ValueError("ENTRY must be a single line, no newline characters allowed")
    if not ENTRY.strip():
        raise ValueError("ENTRY must not be only whitespace")
    if not ENTRY.endswith(".") or ENTRY.endswith(".."):
        raise ValueError(
            "ENTRY must end with exactly one terminal period, got ending %r"
            % ENTRY[-2:]
        )
    if ". " in ENTRY[:-1]:
        raise ValueError(
            "ENTRY must be exactly one sentence, found a sentence break at %r"
            % ENTRY[ENTRY.index(". ") : ENTRY.index(". ") + 2]
        )
    return ENTRY


def write_and_verify(path, data):
    """Write data to path, then read it back and confirm it is byte-identical.

    Returns the number of bytes written. Raises ValueError if the read-back
    differs from what was written, naming the path and both byte counts.
    """
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        raise ValueError(
            "read-back mismatch for %s: wrote %d bytes, read %d bytes"
            % (path, len(data), len(written))
        )
    return len(written)


def main():
    entry = validate_entry()
    data = entry.encode("utf-8")
    os.makedirs("/output", exist_ok=True)
    write_and_verify("/output/entry.txt", data)
    # Best-effort local copy (see module docstring).
    local_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")
    try:
        write_and_verify(local_path, data)
    except OSError as exc:
        print("warning: local copy skipped (%s)" % exc, file=sys.stderr)
    print("characters: %d" % len(entry))


if __name__ == "__main__":
    main()
