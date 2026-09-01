from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from urllib.parse import urljoin

@dataclass(frozen=True)
class Headline:
    title: str
    url: str

    def as_dict(self) -> dict[str, str]: return asdict(self)

class HeadlineParser(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__(); self.base_url=base_url; self.items=[]; self._href=None; self._text=[]; self._heading_depth=0
    def handle_starttag(self, tag, attrs):
        if tag in {"h1","h2","h3"}: self._heading_depth += 1
        if tag == "a" and self._heading_depth: self._href=dict(attrs).get("href"); self._text=[]
    def handle_data(self, data):
        if self._href is not None: self._text.append(data)
    def handle_endtag(self, tag):
        if tag == "a" and self._href is not None:
            title=" ".join("".join(self._text).split())
            if title: self.items.append(Headline(title,urljoin(self.base_url,self._href)))
            self._href=None; self._text=[]
        if tag in {"h1","h2","h3"}: self._heading_depth=max(0,self._heading_depth-1)

def parse_headlines(html: str, base_url: str) -> list[Headline]:
    parser=HeadlineParser(base_url); parser.feed(html)
    return list(dict.fromkeys(parser.items))

