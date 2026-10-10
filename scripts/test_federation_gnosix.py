"""DOCS-FEDERATION-05 — second genuinely public upstream, frozen source and release boundaries."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import federate_gnosix
import federation_vps_watch
import federation_pages

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"docs/federation/gnosix/manifest.json"

class TestGnosixFederation(unittest.TestCase):
    def test_exact_gnosix_public_revision_and_source_license(self):
        m=federate_gnosix.verify()
        self.assertEqual(m["source_ref"],"d0dfb1c1115db2f9761703b866fb6e316ea6c1cd")
        self.assertEqual(m["repository"],"https://github.com/tension-atoi/gnosix")
        self.assertEqual(m["source_license"],"GPL-3.0-or-later")
        self.assertEqual(len(m["files"]),5)

    def test_modified_blob_refused(self):
        m=federate_gnosix.verify()
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp)
            for rel in m["files"]:
                src=ROOT/"docs/federation/gnosix/content"/rel
                target=tmp/"content"/rel
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(src.read_bytes())
            (tmp/"manifest.json").write_text(json.dumps(m))
            with patch.object(federate_gnosix,"BASE",tmp),patch.object(federate_gnosix,"MANIFEST",tmp/"manifest.json"):
                federate_gnosix.verify()
                (tmp/"content/README.md").write_text("# fake product stable release")
                with self.assertRaisesRegex(ValueError,"snapshot tampered"):
                    federate_gnosix.verify()

    def test_source_links_are_commit_pinned(self):
        m=federate_gnosix.verify()
        url=federation_pages.rewrite_links("[status](docs/status/STATUS.md)","README.md",m)
        self.assertIn("/blob/"+m["source_ref"]+"/docs/status/STATUS.md",url)
        self.assertNotIn("/blob/main/",url)

    def test_source_publication_disclaimer(self):
        m=federate_gnosix.verify()
        for lang in ("fr","en"):
            index=(ROOT/"dist"/lang/"projects/gnosix/index.html").read_text()
            self.assertIn(m["source_ref"],index)
            self.assertIn("EDITORIAL DISCREPANCY",index)
            self.assertIn("R19",index)
            for key in ("overview","status","roadmap","evidence","methodology"):
                body=(ROOT/"dist"/lang/"projects/gnosix"/(key+".html")).read_text()
                self.assertIn(m["source_ref"],body)
                self.assertIn("sha256:",body)
                self.assertNotIn("sk-proj-",body)
                self.assertNotIn("/home/tension_atoi",body)
        self.assertTrue((ROOT/"dist/registry/federation-gnosix.json").is_file())

    def test_both_sources_are_detectable_without_publisher_import(self):
        sources=federation_vps_watch.read_sources(ROOT/"docs/federation/sources.v1.json")
        self.assertEqual([(x["id"],len(x["files"])) for x in sources],
                         [("gnostral",7),("gnosix",5)])

    def test_status_release_gate_is_not_silently_promoted(self):
        raw=(ROOT/"docs/federation/gnosix/content/docs/status/STATUS.md").read_text()
        self.assertIn("OPEN / NOT_PUBLISHABLE",raw)
        self.assertIn("stable",raw)
        # Preserve an upstream editorial inconsistency visibly rather than rewriting it.
        self.assertIn("license has not yet been ratified",raw)
        self.assertIn("GPL-3.0-or-later",(ROOT/"docs/federation/gnosix/content/README.md").read_text())

if __name__=="__main__":
    unittest.main()
