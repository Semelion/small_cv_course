"""Check local links, anchors and image references in the generated textbook."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]

class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name == 'id':
                self.ids.add(value)
            if name in ('href', 'src') and value:
                self.links.append(value)

parser = SiteParser()
parser.feed((ROOT / 'index.html').read_text(encoding='utf-8'))
for link in parser.links:
    url = urlsplit(link)
    if url.scheme or url.netloc:
        continue
    if url.path:
        assert (ROOT / unquote(url.path)).is_file(), f'Missing file: {link}'
    elif url.fragment:
        assert unquote(url.fragment) in parser.ids, f'Missing anchor: {link}'
print(f'OK: checked {len(parser.links)} links and image references')
