
ALLOWED_CHARS = "abcdefghijklmnopqrstuvwxyz"
ALLOWED_CHARS += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALLOWED_CHARS += " -_"


def to_filename(title):
    """Given a title, convert it to a valid filename."""

    filename = "".join(c for c in title if c in ALLOWED_CHARS)
    filename = filename.replace(" ", "_")
    filename = filename.replace("-", "_")

    return filename.lower()
