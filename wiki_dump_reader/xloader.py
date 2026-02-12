import io
from typing import Generator
from xml.parsers.expat import ParserCreate


class Iterate:
    def __init__(self, reader) -> None:
        self.reader = reader
        self.parser = ParserCreate()
        self.parser.StartElementHandler = self.start_element
        self.parser.EndElementHandler = self.end_element
        self.parser.CharacterDataHandler = self.char_data
        self.ready = []
        self.slugs: list[str] = []
        self.text_buffer = io.StringIO()
        self.id_buffer = io.StringIO()
        self.title_buffer = io.StringIO()

    def start_element(self, name, attrs):
        self.slugs.append(name)

    def end_element(self, name):
        # print(self.slugs)
        if self.slugs == ["mediawiki", "page", "id"]:
            self.id_buffer.seek(0)
            self.id = self.id_buffer.read()
            self.id_buffer.seek(0)

        elif self.slugs == ["mediawiki", "page", "revision"]:
            self.text_buffer.seek(0)
            self.id_buffer.seek(0)
            self.title_buffer.seek(0)
            self.ready.append(
                (
                    # self.id_buffer.read(),
                    self.title_buffer.read(),
                    self.text_buffer.read(),
                )
            )
            self.text_buffer = io.StringIO()
            self.id_buffer = io.StringIO()
            self.title_buffer = io.StringIO()

        self.slugs.pop()

    def char_data(self, data):
        if self.slugs == ["mediawiki", "page", "id"]:
            self.id_buffer.write(data)
            return
        if self.slugs == ["mediawiki", "page", "title"]:
            self.title_buffer.write(data)
            return
        if self.slugs == ["mediawiki", "page", "revision", "text"]:
            self.text_buffer.write(data)

    def loop(self, buffer_size=128000):
        while True:
            chunk = self.reader.read(buffer_size)
            self.parser.Parse(chunk)
            while len(self.ready) > 0:
                yield self.ready.pop()


def iterate(reader, buffer_size=128000) -> Generator[tuple[str, str], None, None]:
    iterator = Iterate(reader)
    for page in iterator.loop():
        yield page


if __name__ == "__main__":
    import sys

    for title, text in iterate(sys.stdin):
        print(title)  # , "\n\t", text[:100])
