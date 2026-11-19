"""Check the links shipped by the account site's two static pages."""

from html.parser import HTMLParser
from pathlib import Path

PUBLIC = Path(__file__).resolve().parents[1] / "public"
BOOKS = {"/saige/", "/orchagent/", "/humagen/"}


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.anchors = set()
        self.stylesheets = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "a" and attrs.get("href"):
            self.anchors.add(attrs["href"])
        if tag == "link" and "stylesheet" in attrs.get("rel", "").split():
            self.stylesheets.append(attrs["href"])


for name, required in [("index.html", BOOKS), ("404.html", {"/"})]:
    links = Links()
    links.feed((PUBLIC / name).read_text())
    missing = required - links.anchors
    if missing:
        raise SystemExit(f"{name} is missing links to {sorted(missing)}")
    if not links.stylesheets:
        raise SystemExit(f"{name} is missing its stylesheet")
    for href in links.stylesheets:
        if name == "404.html" and not href.startswith("/"):
            raise SystemExit(f"The 404 stylesheet must resolve from a missing nested URL: {href}")
        if not (PUBLIC / href.lstrip("/")).is_file():
            raise SystemExit(f"{name} references missing stylesheet {href}")
print("Verified project links, 404 recovery and stylesheets")
