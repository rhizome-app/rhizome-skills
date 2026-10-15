#!/usr/bin/env python3
"""Print the text of a Word file, one line per paragraph.

    docx_text.py minutes.docx

A `.docx` is a zip of XML; this reads `word/document.xml` and prints each
paragraph's text runs. Text a tracked change deleted sits in other elements
and is left out. Reads only the file given and writes nothing.
"""

import sys
import zipfile
import xml.etree.ElementTree as ElementTree

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def paragraphs(path: str) -> list[str]:
    """Read a Word file's paragraphs.

    :param path: The `.docx` file.
    :return: Each paragraph's text, empty paragraphs included.
    """
    with zipfile.ZipFile(path) as archive:
        document = ElementTree.fromstring(archive.read('word/document.xml'))
    return [
        ''.join(text.text or '' for text in paragraph.iter(f'{W}t'))
        for paragraph in document.iter(f'{W}p')
    ]


def main() -> None:
    """Print the paragraphs of the file given on the command line."""
    if len(sys.argv) != 2:
        sys.exit('usage: docx_text.py <file.docx>')
    for line in paragraphs(sys.argv[1]):
        print(line)


if __name__ == '__main__':
    main()
