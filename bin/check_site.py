#!/usr/bin/env python3
"""Check a built Jekyll site (_site/) for broken internal links and missing images.

Usage: python3 bin/check_site.py _site
Only checks links that point inside the site; external links (http://...) are skipped.
Exit code 1 if anything is broken.
"""
import os
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlparse

SITE_HOSTS = {"yiksiu-chan.github.io"}


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for attr in ("href", "src"):
            if attrs.get(attr) and tag in ("a", "img", "link", "script", "source", "iframe"):
                self.links.append((tag, attrs[attr]))
        if attrs.get("srcset"):
            for part in attrs["srcset"].split(","):
                if part.strip():
                    self.links.append((tag, part.strip().split()[0]))


def target_exists(root, path):
    full = os.path.join(root, path.lstrip("/"))
    if path.endswith("/"):
        return os.path.isfile(os.path.join(full, "index.html"))
    return (
        os.path.isfile(full)
        or os.path.isfile(full + ".html")
        or os.path.isfile(os.path.join(full, "index.html"))
    )


def main(root):
    broken = []
    pages = 0
    for dirpath, _, files in os.walk(root):
        for name in files:
            if not name.endswith(".html"):
                continue
            page = os.path.join(dirpath, name)
            pages += 1
            parser = LinkParser()
            with open(page, encoding="utf-8", errors="replace") as f:
                parser.feed(f.read())
            for tag, link in parser.links:
                url = urlparse(link)
                if url.scheme in ("mailto", "tel", "javascript", "data"):
                    continue
                if url.netloc and url.netloc not in SITE_HOSTS:
                    continue  # external link
                if url.scheme and url.scheme not in ("http", "https"):
                    continue
                path = unquote(url.path)
                if not path:
                    continue  # pure "#anchor" link
                if not path.startswith("/"):
                    base = "/" + os.path.relpath(dirpath, root).replace(os.sep, "/")
                    path = os.path.normpath(os.path.join(base, path)).replace(os.sep, "/")
                if not target_exists(root, path):
                    broken.append((os.path.relpath(page, root), tag, link))

    for page, tag, link in sorted(set(broken)):
        print(f"BROKEN  {page}: <{tag}> {link}")
    print(f"Checked {pages} pages: {len(set(broken))} broken internal link(s)/image(s).")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "_site"))
