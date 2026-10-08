"""Only mutates a newly created fictional repository. Retains it for inspection."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile


def run(output):
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    sandbox = Path(tempfile.mkdtemp(prefix='corpus-fictional-', dir=output))
    repo = sandbox / 'courier'
    repo.mkdir()
    commands = []
    # Do not inherit Git index, worktree, hooks, configuration or author variables.
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update({'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull,
                'GIT_AUTHOR_NAME': 'Fictional learner', 'GIT_AUTHOR_EMAIL': 'learner@example.invalid',
                'GIT_COMMITTER_NAME': 'Fictional learner', 'GIT_COMMITTER_EMAIL': 'learner@example.invalid'})

    def git(*args, cwd=repo, expected=0):
        cmd = ['git', '-c', 'core.hooksPath=/dev/null', '-c', 'commit.gpgsign=false', *args]
        result = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
        commands.append({'command': cmd, 'cwd': str(cwd.relative_to(sandbox)),
                         'expected_exit': expected, 'exit_code': result.returncode,
                         'stdout': result.stdout, 'stderr': result.stderr})
        if result.returncode != expected:
            raise AssertionError(commands[-1])
        return result.stdout.strip()

    def fingerprint():
        return {name: hashlib.sha256((repo/name).read_bytes()).hexdigest()
                for name in ['tracked.txt', 'notes.txt']}

    git('init', '-b', 'main')
    (repo/'tracked.txt').write_text('baseline\n')
    git('add', 'tracked.txt'); git('commit', '-m', 'fictional baseline')
    baseline = git('rev-parse', 'HEAD')
    (repo/'tracked.txt').write_text('staged work\n'); git('add', 'tracked.txt')
    (repo/'tracked.txt').write_text('staged work\nunstaged work\n')
    (repo/'notes.txt').write_text('untracked work\n')
    before = fingerprint()
    index_before = git('show', ':tracked.txt')
    status_before = git('status', '--porcelain')
    assert 'MM tracked.txt' in status_before and '?? notes.txt' in status_before
    (sandbox/'backup').mkdir()
    for name in before:
        (sandbox/'backup'/name).write_bytes((repo/name).read_bytes())
    wt = sandbox/'slice'
    git('worktree', 'add', '-b', 'slice', str(wt), baseline)
    (wt/'slice.txt').write_text('slice change\n')
    git('add', 'slice.txt', cwd=wt); git('commit', '-m', 'fictional slice', cwd=wt)
    slice_head = git('rev-parse', 'HEAD', cwd=wt)
    other = sandbox/'other'
    git('worktree', 'add', '-b', 'other', str(other), baseline)
    (other/'other.txt').write_text('independent change\n')
    git('add', 'other.txt', cwd=other); git('commit', '-m', 'fictional divergence', cwd=other)
    other_head = git('rev-parse', 'HEAD', cwd=other)
    git('merge-base', '--is-ancestor', baseline, slice_head)
    git('merge-base', '--is-ancestor', baseline, other_head)
    git('merge-base', '--is-ancestor', slice_head, other_head, expected=1)
    git('merge-base', '--is-ancestor', other_head, slice_head, expected=1)
    counts = git('rev-list', '--left-right', '--count', f'{slice_head}...{other_head}')
    assert counts.split() == ['1', '1']
    assert git('merge-base', slice_head, other_head) == baseline
    assert before == fingerprint()
    assert index_before == git('show', ':tracked.txt')
    assert status_before == git('status', '--porcelain')
    assert git('rev-parse', 'HEAD') == baseline
    git('worktree', 'list', '--porcelain')
    git('log', '--all', '--graph', '--oneline')
    report = {'lab': 'EC-L03', 'result': 'PASS', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'sandbox': str(sandbox), 'baseline': baseline, 'slice_head': slice_head, 'other_head': other_head,
              'preserved_hashes': before, 'preserved_index': index_before, 'divergence': [1, 1],
              'commands': commands, 'limits': ['Fictional repository only', 'No merge/rebase/conflict/submodule coverage',
                                              'Backups and worktrees retained; no destructive cleanup']}
    (output/'workspace-run.json').write_text(json.dumps(report, indent=2)+'\n')
    (output/'workspace.log').write_text('\n'.join(json.dumps(x) for x in commands)+'\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path('evidence/runs/workspace-lab'))
    print(json.dumps(run(parser.parse_args().output), indent=2))
