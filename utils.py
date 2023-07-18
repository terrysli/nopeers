def clean_text(text):
    """
    Remove whitespace before and after in a string.

    >>> clean_text("  cat")
    "cat"

    >>> clean_text("dog  ")
    "dog"

    >>> clean_text(" longer sentence ")
    "longer sentence"
    """
    stripped_str = text.strip()
    return stripped_str

def save_html(html, path):
    """Store html in a local file at path."""
    with open(path, 'wb') as f:
        f.write(html)

def open_html(path):
    """Read html from a local file."""
    with open(path, 'rb') as f:
        return f.read()