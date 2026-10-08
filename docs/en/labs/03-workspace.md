---
id: lab-workspace
title: Lab C — Workspace Hygiene & Git Topology
duration: 40
status: draft
category: lab
method_id: EC-L03
classification: recommendation
prerequisites:
- Git 2.30+
- Python 3.10+
- Chapter 08
artifacts:
- Git inventory
- Preserved byte hashes and index
- Two-way ancestry results
success_criteria:
- Dirty files and index unchanged; divergent branches proven in both directions
references:
- git-worktree
- git-merge-base
---
# Lab C — Workspace Hygiene & Git Topology

## Problem and invariants
Courier contains a staged edit, an unstaged edit and an untracked note. Create a slice from an explicit baseline without moving, deleting or committing those edits. Worktrees share objects and refs: they are not security boundaries.

## Run on fictional repositories only
From repository root, choose an empty evidence directory for the exercise:

```bash
python3 examples/workspace_lab.py --output evidence/runs/workspace-trial
```

[Download the fixture](/examples/workspace_lab.py). The script creates a new temporary repository under that directory; it accepts no existing repository as a target and retains worktrees for inspection. It neutralizes global Git configuration and hooks. No network or private repository access.

## Operational method
1. Read git status --porcelain, git rev-parse HEAD and git worktree list --porcelain inside the fictional repository identified in the manifest.
2. Compare tracked.txt and notes.txt hashes and git show :tracked.txt; a byte backup is not an index backup.
3. Read the two independent commits created from baseline. Dirty work is not transferred into the worktrees.
4. Inspect git merge-base --is-ancestor baseline slice: exit 0. Inspect slice → other and other → slice: exit 1 both ways; another code is an error, not divergence.
5. Verify git rev-list --left-right --count slice...other: 1 and 1. The common merge-base must equal baseline.
6. Compare files, index, status and HEAD before/after. Retain the repository for challenge; no forced deletion.

## Exercise and counterexample
Predict ancestry if one branch starts at slice instead of baseline, then adapt a fixture copy. Two existing branches need not diverge. reset --hard or clean -fd can destroy work; neither is a preflight tool in this lab.

<details><summary>Self-check</summary>The manifest contains three exact commits, preserved index and hashes, four ancestry checks, 1/1 divergence and raw logs. In the descendant variant, slice is an ancestor of the new branch (0), and reverse ancestry returns 1. Distinguish expected failure from Git error.</details>

## Qualification and limits
PASS proves the fictional scenario, not all conflicts, submodules, ignored files, Git filters or crash recovery. The fixture preserves data; it does not demonstrate restoration of a real repository. To remove a practice worktree, verify it is clean then use git worktree remove without --force; retain useful notes and logs.
