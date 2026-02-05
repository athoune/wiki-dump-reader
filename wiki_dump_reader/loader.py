from typing import Generator
from xml.etree import ElementTree
from xml.etree.ElementTree import Element


def iterate(reader) -> Generator[tuple[str, str], None, None]:
    content: list[str] = []
    for line in reader:
        line: str = line.strip()
        if line == "<page>":
            content = [line]
        elif line == "</page>":
            content.append(line)
            content_txt: str = "\n".join(content)
            tree: Element = ElementTree.fromstring(content_txt)
            content_txt = ""
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
            if type(content) is list:
                content.append(line)
