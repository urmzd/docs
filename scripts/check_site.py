"""Check HTML links, site assets, search documents and canonical paths in a Pages bundle."""

from html.parser import HTMLParser
import json
from pathlib import Path
import sys
from urllib.parse import unquote, urljoin, urlsplit

PROJECTS = {"orchagent", "saige", "humagen"}
BASE = "https://docs.urmzd.com/"


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.canonical = None
        self.anchors = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "a" and attrs.get("href"):
            self.anchors.append(attrs["href"])
        if tag == "link" and "canonical" in attrs.get("rel", "").split():
            self.canonical = attrs.get("href")
        for key in ("href", "src", "poster"):
            if attrs.get(key):
                self.references.append(attrs[key])


def document_path(path):
    return path.removesuffix("index.html")


def local_target(site, page_url, reference):
    url = urlsplit(urljoin(page_url, reference))
    if url.scheme not in ("http", "https") or url.netloc != urlsplit(BASE).netloc:
        return None
    path = site / unquote(url.path).lstrip("/")
    return path / "index.html" if path.is_dir() else path


def verify(site):
    errors = []
    pages = sorted(site.rglob("*.html"))
    book_homes = {f"{name}/index.html" for name in PROJECTS}
    for relative in ["index.html", "404.html", *book_homes]:
        if not (site / relative).is_file():
            errors.append(f"Missing {relative}")
    for page in pages:
        relative = page.relative_to(site).as_posix()
        url = urljoin(BASE, document_path(relative))
        links = Links()
        links.feed(page.read_text())
        if page.name == "index.html" and links.canonical != url:
            errors.append(f"{relative} has canonical {links.canonical!r}, expected {url}")
        if relative in book_homes:
            if not any(urljoin(url, href) == BASE for href in links.anchors):
                errors.append(f"{relative} is missing a link back to the hub")
        if relative == "index.html":
            for project in PROJECTS:
                if project + "/" not in links.references:
                    errors.append(f"Hub is missing a link to {project}")
        for ref in links.references:
            dest = local_target(site, url, ref)
            if dest is not None and not dest.is_file():
                errors.append(f"{relative} → {ref}")
    for project in sorted(PROJECTS):
        book = site / project
        index = book / "search.json"
        if not index.is_file() or not any(book.glob("*/**/index.html")):
            errors.append(f"{project} is missing its search index or nested pages")
            continue
        items = json.loads(index.read_text())["items"]
        if not items:
            errors.append(f"{project} has an empty search index")
        for item in items:
            dest = local_target(site, BASE + project + "/", item["location"])
            if dest is None or not dest.is_file():
                errors.append(f"{project}/search.json → {item['location']}")
    if errors:
        raise SystemExit("\n".join(dict.fromkeys(errors)))
    print(f"Verified {len(pages)} HTML pages and {len(PROJECTS)} search indexes")


if __name__ == "__main__":
    verify(Path(sys.argv[1] if len(sys.argv) > 1 else "site").resolve())
