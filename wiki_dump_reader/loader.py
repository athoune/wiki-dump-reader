from io import StringIO
from typing import Generator
from xml.etree import ElementTree
from xml.etree.ElementTree import Element


def iterate(reader) -> Generator[tuple[str, str], None, None]:
    content = None
    for line in reader:
        stripped: str = line.strip()
        if stripped == "<page>":
            content = StringIO()
            content.write(line)
        elif stripped == "</page>":
            content.write(stripped)
            content.seek(0)
            tree: Element = ElementTree.fromstring(content.read())
            content = None
            ns_elem: Element[str] | None = tree.find("ns")
            if ns_elem is None:
                continue
            if ns_elem.text is not None and ns_elem.text.strip() != "0":
                continue
            title_elem: Element[str] | None = tree.find("title")
            if title_elem is None or title_elem.text is None:
                continue
            title: str = title_elem.text
            text_elem: Element[str] | None = tree.find("revision/text")
            if text_elem is None:
                continue
            text: str | None = text_elem.text
            if text is None:
                continue
            yield title, text
        else:
            if content is not None:
                content.write(line)

if __name__ == "__main__":
    import sys

    for title, text in iterate(sys.stdin):
        print(title)  # , "\n\t", text[:100])
