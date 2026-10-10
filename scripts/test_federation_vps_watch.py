"""VPS read-only federation watch: safe public-registry and drift negatives."""
from __future__ import annotations
import base64
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import federation_vps_watch as w

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/federation/sources.v1.json"
OLD = "a" * 40
NEW = "b" * 40

class WatchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.state = Path(self.tmp.name) / "state"
        self.source = {"id":"gnostral","repository":"tension-atoi/gnostral.rs",
                       "branch":"main","pinned_sha":OLD,
                       "files":{"README.md":"0"*64}}

    def test_real_registry_has_one_public_upstream_no_publisher_loop(self):
        results = w.read_sources(REGISTRY)
        self.assertEqual(len(results),1)
        self.assertEqual(results[0]["id"],"gnostral")
        public=json.loads(REGISTRY.read_text())
        self.assertEqual(public["sources"][1]["kind"],"publisher")
        self.assertFalse(public["sources"][1]["enabled"])

    def test_current_requires_no_document_download(self):
        with patch.object(w,"get_head",return_value=OLD),patch.object(w,"get_blob") as blob:
            result=w.inspect(self.source)
        self.assertEqual(result["status"],"CURRENT")
        blob.assert_not_called()

    def test_changed_sha_requires_document_bytes_and_double_head_check(self):
        with patch.object(w,"get_head",side_effect=[NEW,NEW]),patch.object(w,"get_blob",return_value=b"# Updated\n"):
            result=w.inspect(self.source)
        self.assertEqual(result["status"],"DOC_UPDATE_CANDIDATE")
        self.assertEqual(result["changed_documents"][0]["path"],"README.md")
        self.assertFalse(result.get("auto_deploy",False))

    def test_no_relevant_diff_is_not_a_candidate(self):
        correct=w.sha256(b"# Same\n")
        source={**self.source,"files":{"README.md":correct}}
        with patch.object(w,"get_head",side_effect=[NEW,NEW]),patch.object(w,"get_blob",return_value=b"# Same\n"):
            result=w.inspect(source)
        self.assertEqual(result["status"],"SOURCE_AHEAD_NO_DOC_CHANGE")

    def test_racing_branch_tip_refused(self):
        with patch.object(w,"get_head",side_effect=[NEW,OLD]),patch.object(w,"get_blob",return_value=b"# Changed\n"):
            with self.assertRaisesRegex(w.WatchRefused,"moved during"):
                w.inspect(self.source)

    def write_registry(self, registry):
        fake=Path(self.tmp.name)/"sources.json"
        fake.write_text(json.dumps(registry))
        source=REGISTRY.parent/"gnostral/manifest.json"
        target=fake.parent/"gnostral/manifest.json"
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(source.read_bytes())
        return fake

    def test_unknown_registry_schema_denied(self):
        registry=json.loads(REGISTRY.read_text())
        registry["schema"]="unknown"
        fake=self.write_registry(registry)
        with self.assertRaisesRegex(w.WatchRefused,"schema"):
            w.read_sources(fake)

    def test_circular_publisher_cannot_be_enabled(self):
        registry=json.loads(REGISTRY.read_text())
        registry["sources"][1]["enabled"]=True
        fake=self.write_registry(registry)
        with self.assertRaisesRegex(w.WatchRefused,"self-ingestion"):
            w.read_sources(fake)

    def test_noncanonical_private_owner_rejected(self):
        registry=json.loads(REGISTRY.read_text())
        registry["sources"][1]["repository"]="other/private"
        fake=self.write_registry(registry)
        with self.assertRaisesRegex(w.WatchRefused,"public owner"):
            w.read_sources(fake)

    def test_path_escape_not_allowed(self):
        with self.assertRaisesRegex(w.WatchRefused,"allowlist"):
            w.get_blob("tension-atoi/gnostral.rs",NEW,"../secret.md")

    def test_github_blob_integrity_tamper_denied(self):
        fake={"type":"file","encoding":"base64","content":base64.b64encode(b"# Hello\n").decode(),
              "size":8,"sha":"0"*40}
        with patch.object(w,"fetch_json",return_value=fake):
            with self.assertRaisesRegex(w.WatchRefused,"integrity"):
                w.get_blob("tension-atoi/gnostral.rs",NEW,"README.md")

    def test_valid_github_blob_accepted(self):
        raw=b"# Hello\n"
        import hashlib
        blobsha=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
        fake={"type":"file","encoding":"base64","content":base64.b64encode(raw).decode(),
              "size":len(raw),"sha":blobsha}
        with patch.object(w,"fetch_json",return_value=fake):
            self.assertEqual(w.get_blob("tension-atoi/gnostral.rs",NEW,"README.md"),raw)

    def test_symlink_api_response_denied(self):
        with patch.object(w,"fetch_json",return_value={"type":"symlink","encoding":"base64","size":8}):
            with self.assertRaisesRegex(w.WatchRefused,"regular blob"):
                w.get_blob("tension-atoi/gnostral.rs",NEW,"README.md")

    def test_write_atomic_private_and_candidate_cleanup(self):
        normal={"id":"gnostral","repository":"tension-atoi/gnostral.rs","pinned_ref":OLD,
                "observed_ref":NEW,"status":"DOC_UPDATE_CANDIDATE","changed_documents":[{"path":"README.md"}],
                "changed_count":1}
        current={**normal,"observed_ref":OLD,"status":"CURRENT","changed_documents":[],"changed_count":0}
        with patch.object(w,"read_sources",return_value=[self.source]),patch.object(w,"inspect",side_effect=[normal,current]):
            first=w.watch(REGISTRY,self.state)
            self.assertEqual(first["verdict"],"DOC_UPDATE_CANDIDATE")
            candidate=self.state/"candidate.json"
            self.assertTrue(candidate.exists())
            self.assertEqual(candidate.stat().st_mode & 0o777,0o600)
            second=w.watch(REGISTRY,self.state)
            self.assertEqual(second["verdict"],"CURRENT")
            self.assertFalse(candidate.exists())
            self.assertEqual((self.state/"latest.json").stat().st_mode & 0o777,0o600)

if __name__=="__main__":
    unittest.main()
