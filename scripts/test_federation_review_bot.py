"""DOCS-FEDERATION-03: deterministic real-git drift detection, no network/PR."""
from __future__ import annotations
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import federation_review_bot as bot

def git(path, *args):
    return subprocess.run(["git", "-C", str(path), *args], check=True,
                          capture_output=True,text=True).stdout.strip()

class TestDriftDetector(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix="gnostral-drift-")
        self.addCleanup(self.tmp.cleanup)
        self.repo=Path(self.tmp.name)
        git(self.repo,"init","-b","main")
        git(self.repo,"remote","add","origin",bot.CANONICAL+".git")
        self.files={}
        for name in bot.federation.PATHS:
            p=self.repo/name
            p.parent.mkdir(parents=True,exist_ok=True)
            content=("# "+name+"\nPinned original content.\n").encode()
            p.write_bytes(content)
            self.files[name]=hashlib.sha256(content).hexdigest()
        git(self.repo,"add",".")
        self.commit("initial")
        self.base=git(self.repo,"rev-parse","HEAD")
        git(self.repo,"update-ref","refs/remotes/origin/main",self.base)
        self.patch=patch.object(bot.federation,"verify",return_value={
            "source_ref":self.base, "files":self.files})
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def commit(self,msg):
        subprocess.run(["git","-C",str(self.repo),"-c","user.name=Fixture",
                        "-c","user.email=fixture@example.invalid",
                        "commit","--allow-empty","-m",msg],check=True,capture_output=True)

    def update(self,path,contents):
        p=self.repo/path
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(contents)
        git(self.repo,"add",path)
        self.commit("local only: fixture edit")
        git(self.repo,"update-ref","refs/remotes/origin/main",git(self.repo,"rev-parse","HEAD"))

    def test_current_gives_no_update_or_mutation(self):
        report=bot.inspect(self.repo)
        self.assertEqual(report["status"],"CURRENT")
        self.assertEqual(report["changed_documents"],[])
        self.assertFalse(report["auto_deploy"])

    def test_doc_change_produces_exact_sha_and_review_only(self):
        self.update("README.md","# README\nProposed docs update.\n")
        report=bot.inspect(self.repo)
        self.assertEqual(report["status"],"DOC_UPDATE_CANDIDATE")
        self.assertEqual(report["changed_count"],1)
        self.assertEqual(report["changed_documents"][0]["path"],"README.md")
        self.assertEqual(report["changed_documents"][0]["before_sha256"],self.files["README.md"])
        self.assertFalse(report["auto_merge"])
        self.assertFalse(report["auto_deploy"])
        self.assertTrue(report["requires_review"])

    def test_non_doc_commit_does_not_create_pr(self):
        self.update("examples/demo.txt","Not a documentation source.")
        report=bot.inspect(self.repo)
        self.assertEqual(report["status"],"SOURCE_AHEAD_NO_DOC_CHANGE")
        self.assertFalse(report["requires_review"])

    def test_rewritten_source_history_fails_closed(self):
        # A new orphan commit cannot replace the public source's pinned ancestor.
        git(self.repo,"checkout","--orphan","other")
        for rel in bot.federation.PATHS:
            git(self.repo,"add",rel)
        self.commit("history rewrite")
        other=git(self.repo,"rev-parse","HEAD")
        with self.assertRaisesRegex(bot.Refused,"non-fast-forward"):
            bot.inspect(self.repo,target=other)

    def test_unknown_source_remote_rejected(self):
        git(self.repo,"remote","set-url","origin","https://example.invalid/private")
        with self.assertRaisesRegex(bot.Refused,"canonical public"):
            bot.inspect(self.repo)

    def test_active_markup_is_denied_before_renderer(self):
        self.update("README.md","# README\n<script>alert(1)</script>\n")
        with self.assertRaisesRegex(bot.Refused,"active HTML"):
            bot.inspect(self.repo)

    def test_script_scheme_markdown_is_denied(self):
        self.update("README.md","# README\n[click](javascript:alert(1))\n")
        with self.assertRaisesRegex(bot.Refused,"unsafe Markdown"):
            bot.inspect(self.repo)

    def test_symlink_source_is_refused(self):
        path=self.repo/"README.md"
        path.unlink()
        path.symlink_to("QUESTLOG.md")
        git(self.repo,"add","README.md")
        self.commit("symlink swap")
        git(self.repo,"update-ref","refs/remotes/origin/main",git(self.repo,"rev-parse","HEAD"))
        with self.assertRaisesRegex(bot.Refused,"regular, non-executable"):
            bot.inspect(self.repo)

    def test_no_proposal_if_current(self):
        report=bot.inspect(self.repo)
        with self.assertRaisesRegex(bot.Refused,"no relevant changed"):
            bot.prepare(self.repo,destination=self.repo/"candidate",candidate=report,docs_repo=self.repo)

if __name__=="__main__":
    unittest.main()
