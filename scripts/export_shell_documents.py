#!/usr/bin/env python3
"""CORPUS-EXPORT-01: fail-closed semantic export, no executable HTML."""
from __future__ import annotations
import hashlib
import json
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from build import CATALOG, ROOT, unpack, render_markdown

OUT = ROOT / "exports" / "gnu6-shell-documents.v1.json"
TAGS = set("h1 h2 h3 h4 h5 h6 p blockquote pre code strong em del ul ol li table thead tbody tr th td a details summary span hr br".split())
VOID = {"br", "hr"}
ATTRS = {"id", "href", "title", "colspan", "rowspan", "scope", "start", "open", "tabindex", "class"}

class UnsafeDocument(ValueError):
    pass

class SemanticParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.nodes = []
        self.stack = []

    def handle_starttag(self, tag, attrs):
        if tag not in TAGS:
            raise UnsafeDocument("Unsupported HTML tag: " + tag)
        safe = {}
        for key, value in attrs:
            if key not in ATTRS or key in safe:
                raise UnsafeDocument("Unsupported or duplicate attr: " + tag + "." + key)
            if key == "href":
                if not value or any(ord(c) < 32 for c in value):
                    raise UnsafeDocument("Invalid hyperlink")
                url = urlsplit(value)
                if url.scheme not in ("", "https", "http") or url.netloc and not url.scheme:
                    raise UnsafeDocument("Disallowed URL scheme")
            safe[key] = value if value is not None else ""
        node = {"tag": tag}
        if safe:
            node["attrs"] = safe
        if tag not in VOID:
            node["children"] = []
        (self.stack[-1]["children"] if self.stack else self.nodes).append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1]["tag"] != tag:
            raise UnsafeDocument("Unbalanced closing tag: " + tag)
        self.stack.pop()

    def handle_data(self, text):
        if text:
            (self.stack[-1]["children"] if self.stack else self.nodes).append({"text": text})

    def close(self):
        super().close()
        if self.stack:
            raise UnsafeDocument("Unclosed HTML element")

def parse_semantic(html):
    parser = SemanticParser()
    parser.feed(html)
    parser.close()
    return parser.nodes

def export_documents():
    pages = []
    chapters = [row["id"] for row in CATALOG["chapters"]]
    for locale in ("fr", "en"):
        for kind, slug in [("home", "index"), *[("chapter", slug) for slug in chapters]]:
            relative = f"docs/{locale}/index.md" if kind == "home" else f"docs/{locale}/chapters/{slug}.md"
            raw = (ROOT / relative).read_bytes()
            metadata, body = unpack(ROOT / relative)
            if metadata.get("status") not in {"draft", "reviewed", "adopted"}:
                raise UnsafeDocument("Unsupported editorial status in " + relative)
            if metadata.get("id") != ("home" if kind == "home" else slug):
                raise UnsafeDocument("Source id mismatch in " + relative)
            nodes = parse_semantic(render_markdown(body))
            if sum(node.get("tag") == "h1" for node in nodes) != 1:
                raise UnsafeDocument("Expected one heading in " + relative)
            anchors = []
            def collect(items):
                for item in items:
                    if "id" in item.get("attrs", {}):
                        anchors.append(item["attrs"]["id"])
                    collect(item.get("children", []))
            collect(nodes)
            if len(set(anchors)) != len(anchors):
                raise UnsafeDocument("Duplicate anchor in " + relative)
            pages.append({
                "id": metadata["id"], "kind": kind, "locale": locale,
                "route": f"/docs/{locale}" if kind == "home" else f"/docs/{locale}/chapters/{slug}",
                "legacy_route": f"/{locale}/index.html" if kind == "home" else f"/{locale}/chapters/{slug}.html",
                "title": metadata["title"], "status": metadata["status"],
                "duration": metadata.get("duration"), "source": relative,
                "source_sha256": hashlib.sha256(raw).hexdigest(),
                "anchors": anchors, "nodes": nodes,
            })
    return {
        "schema": "gnu6.corpus.semantic.v1",
        "source_commit": subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip(),
        "edition": CATALOG["edition"], "product": CATALOG["product"]["name"],
        "locales": ["fr", "en"], "documents": pages,
    }

def main():
    data = export_documents()
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n")
    print("CORPUS_EXPORT_PASS", len(data["documents"]), hashlib.sha256(OUT.read_bytes()).hexdigest())

if __name__ == "__main__":
    main()
