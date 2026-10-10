"""DOCS-FEDERATION-03: draft-only publisher and refusal gates, no network."""
import pathlib
import unittest
from unittest.mock import patch
import federation_draft_pr as pr

SHA0="a"*40
SHA1="b"*40

class TestDraftPublisher(unittest.TestCase):
    def report(self):
        return {"requires_review":True, "branch":"docs/gnostral-refresh-"+SHA1[:12],
                "docs_base_sha":SHA0,
                "candidate":{"status":"DOC_UPDATE_CANDIDATE",
                    "docs_main_source_ref":SHA0, "source_head":SHA1,
                    "changed_documents":[{"path":"README.md",
                        "before_sha256":"0"*64,"after_sha256":"1"*64}]}}

    def test_body_discloses_exact_sha_and_review_gates(self):
        text=pr.body(self.report(),["dist/fr/projects/gnostral/index.html"])
        self.assertIn(SHA1,text)
        self.assertIn("README.md",text)
        self.assertIn("draft-only",text)
        self.assertIn("Coolify",text)
        self.assertNotIn("auto-merge: true",text)

    def test_dry_run_does_not_call_gh_or_git_write(self):
        with patch.object(pr,"audit_worktree",return_value=["dist/fr/projects/gnostral/index.html"]),patch.object(pr,"invoke") as shell:
            status=pr.publish(pathlib.Path("/unused"),self.report(),pathlib.Path("/unused"),perform=False)
            self.assertTrue(status.startswith("DRAFT_PR_DRY_RUN_PASS"))
            shell.assert_not_called()

    def test_draft_publish_writes_no_merge_or_deploy(self):
        calls=[]
        def emulate(*args,**_):
            calls.append(args)
            if args[:3]==("gh","pr","list"):return "[]"
            if args[:3]==("gh","pr","create"):return "https://github.com/tension-atoi/engineering-corpus/pull/999"
            return ""
        with patch.object(pr,"audit_worktree",return_value=["dist/fr/projects/gnostral/index.html"]),patch.object(pr,"invoke",side_effect=emulate):
            status=pr.publish(pathlib.Path("/unused"),self.report(),pathlib.Path("/unused"),perform=True)
        self.assertIn("DRAFT_PR_CREATED",status)
        self.assertEqual(sum(x[:3]==("gh","pr","create") for x in calls),1)
        self.assertTrue(any("--draft" in x for x in calls))
        self.assertFalse(any("merge" in x or "deploy" in x for x in calls))

    def test_no_proposal_refuses_before_pub(self):
        with patch.object(pr,"audit_worktree",side_effect=pr.PublicationRefused("no proposal")),patch.object(pr,"invoke") as shell:
            with self.assertRaisesRegex(pr.PublicationRefused,"no proposal"):
                pr.publish(pathlib.Path("/unused"),self.report(),pathlib.Path("/unused"),perform=True)
            shell.assert_not_called()

    def test_staging_allowlist_is_strict(self):
        self.assertTrue("dist/" in pr.ALLOWED)
        self.assertFalse("src/engine.rs".startswith(pr.ALLOWED[:2]))
        self.assertTrue("docs/source-registry.json" in pr.ALLOWED)

if __name__=="__main__":unittest.main()
