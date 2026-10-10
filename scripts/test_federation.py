"""DOCS-FEDERATION-02: pinned sources, tracked drift, static pages and rejection tests."""
from __future__ import annotations
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import federate_gnostral as core
import federation_pages as pages

ROOT=Path(__file__).resolve().parents[1]

class TestFederation(unittest.TestCase):
    def test_real_source_is_pinned_and_covered(self):
        manifest=core.verify()
        self.assertEqual(manifest["source_ref"],"b23923a110608b565deec56e6360041f56a59c0b")
        self.assertEqual(len(manifest["files"]),7)
        self.assertIn("docs/CAPABILITY_MATRIX.md",manifest["files"])

    def test_invalid_repo_owner_or_mutable_ref_rejected(self):
        original=core.verify()
        for key,value in (("source_ref","main"),("repository","https://example.org/private")):
            corrupt={**original,key:value}
            with self.subTest(key=key),self.assertRaises(ValueError):
                core.validate_schema(corrupt)

    def test_tampered_snapshot_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            target=Path(folder)
            (target/"content"/"docs").mkdir(parents=True)
            manifest=core.verify()
            for key in core.PATHS:
                dest=target/"content"/key
                dest.parent.mkdir(parents=True,exist_ok=True)
                dest.write_bytes((core.BASE/"content"/key).read_bytes())
            (target/"manifest.json").write_text(json.dumps(manifest))
            (target/"content"/"README.md").write_bytes(b"# modified")
            with patch.object(core,"BASE",target),patch.object(core,"MANIFEST",target/"manifest.json"):
                with self.assertRaisesRegex(ValueError,"snapshot content drift"):
                    core.verify()

    def test_source_links_are_pinned_not_live_main(self):
        m=core.verify()
        text="[Read roadmap](docs/ROADMAP.md) and [Engine](https://github.com/tension-atoi/gnostral.rs)"
        result=pages.rewrite_links(text,"README.md",m)
        self.assertIn("/blob/"+m["source_ref"]+"/docs/ROADMAP.md",result)
        self.assertNotIn("/blob/main/",result)
        self.assertIn("https://github.com/tension-atoi/gnostral.rs",result)

    def test_escape_and_absolute_source_links_rejected(self):
        m=core.verify()
        for link in ("[secret](../../../secret.txt)","[private](/home/test/.ssh/id_rsa)"):
            with self.subTest(link=link),self.assertRaises(ValueError):
                pages.rewrite_links(link,"README.md",m)

    def test_public_pages_and_manifest_exist(self):
        dist=ROOT/"dist"
        m=core.verify()
        self.assertEqual(json.loads((dist/"registry/federation-gnostral.json").read_text()),m)
        for lang in ("fr","en"):
            for key in ("index","overview","capabilities","questlog","roadmap","architecture","reproducibility"):
                page=dist/lang/"projects/gnostral"/(key+".html")
                html=page.read_text()
                self.assertEqual(html.count("<h1"),1,(lang,key))
                self.assertIn(m["source_ref"],html,(lang,key))
                self.assertIn("g6-spine-shell",html)
                self.assertNotIn("/home/tension_atoi/",html)
                self.assertNotIn("sk-proj-",html)

if __name__=="__main__":
    unittest.main()
