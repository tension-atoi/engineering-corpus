"""Fictional action oracle; no graphics, subprocesses or network."""
import argparse
import json


def run(broken=False):
    requests = [('r1', 'left', True), ('r1', 'right', True), ('r2', 'left', False)]
    actions = []
    target = None
    for identity, position, allowed in requests:
        target = position
        if allowed and (broken or identity not in actions):
            actions.append(identity)
    assert actions == ['r1'], f'expected one r1 action, got {actions}'
    assert target == 'left'
    return {'actions': actions, 'target': target, 'denied_action_count': actions.count('r2')}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--broken', action='store_true')
    args = parser.parse_args()
    print(json.dumps(run(args.broken), sort_keys=True))
