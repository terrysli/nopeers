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