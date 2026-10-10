"""CORPUS-EXPORT-01: exact provenance, determinism and unsafe HTML denial."""
import hashlib
import json
from export_shell_documents import OUT, ROOT, UnsafeDocument, export_documents, parse_semantic

def main():
    manifest = export_documents()
    persisted = json.loads(OUT.read_text())
    # The export is immutable and records its originating commit. After a Git
    # merge, HEAD changes while the original editorial bytes remain identical.
    # Never rewrite source_commit merely to satisfy a later checkout.
    import subprocess
    original_commit = persisted["source_commit"]
    assert len(original_commit) == 40
    subprocess.check_call(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", original_commit, "HEAD"])
    assert {k: v for k, v in manifest.items() if k != "source_commit"} == {
        k: v for k, v in persisted.items() if k != "source_commit"
    }
    assert manifest["schema"] == "gnu6.corpus.semantic.v1"
    assert len(manifest["documents"]) == 18
    assert len({item["route"] for item in manifest["documents"]}) == 18
    for document in manifest["documents"]:
        assert document["anchors"][0] == "section-1"
        raw = (ROOT/document["source"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == document["source_sha256"]
        assert document["status"] in ("draft","reviewed","adopted")
    for danger in ('<script>alert(1)</script>',
                   '<a href="javascript:alert(1)">X</a>',
                   '<img src="x" onerror="alert(1)">',
                   '<a href="https://example.com" onclick="x()">X</a>'):
        try:
            parse_semantic(danger)
        except UnsafeDocument:
            pass
        else:
            raise AssertionError("Unsafe markup accepted")
    assert parse_semantic('<p><strong>good</strong><a href="#section-1">link</a></p>')
    print("CORPUS_EXPORT_TEST_PASS", len(manifest["documents"]))

if __name__ == "__main__":
    main()
