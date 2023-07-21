from bs4 import BeautifulSoup

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
    soup = BeautifulSoup(html, 'html.parser')
    file = open(path, mode='w', encoding='utf-8')
    file.write(soup.prettify())

def open_html(path):
    """Read and return html from a local file."""
    with open(path, 'rb') as f:
        return f.read()