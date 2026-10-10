#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Acquire fresh Linux UID+SO_PEERCRED evidence; never modifies permanent accounts.

Prerequisite: an independently controlled Linux host with a working *rootful*
Docker daemon and an already-local debian:trixie-slim image. No network or pulls.
Raw output is PRIVATE by default and is deliberately written outside Git.
"""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import socket
import stat
import subprocess
import tempfile
import time
import uuid

BASE = Path(__file__).resolve().parent
IMAGE = 'postgres:16'
SERVICE = 65534
UNAUTHORIZED = 65533
DAC_OUTSIDER = 65532

def cmd(arguments, timeout=30):
    try:
        p = subprocess.run(arguments, capture_output=True, text=True, timeout=timeout)
        return {'code': p.returncode, 'stdout': p.stdout[:12000], 'stderr': p.stderr[:2500]}
    except subprocess.TimeoutExpired:
        return {'code': None, 'stdout': '', 'stderr': 'COMMAND_TIMEOUT'}

def docker(*args, timeout=30):
    return cmd(['docker', *args], timeout=timeout)

def required(result, label):
    if result['code'] != 0:
        raise RuntimeError(label + ': ' + result['stderr'][-600:])

def host_uid(pid):
    text = Path(f'/proc/{pid}/status').read_text()
    line = next(line for line in text.splitlines() if line.startswith('Uid:'))
    return list(map(int, line.split()[1:]))

def host_client(socket_path):
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
            connection.settimeout(8)
            connection.connect(str(socket_path))
            connection.sendall(b'PING\n')
            return {'code': 0, 'response': connection.recv(128).decode().strip()}
    except OSError as error:
        return {'code': 1, 'error': f'{type(error).__name__}: {error.strerror}'}

def other_client(folder, uid, gid):
    return docker('run', '--rm', '--pull=never', '--network', 'none', '--read-only',
                  '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges',
                  '--pids-limit', '24', '--memory', '96m', '--user', f'{uid}:{gid}',
                  '--mount', f'type=bind,source={folder},target=/lab,readonly',
                  '--entrypoint', 'perl', IMAGE, '/lab/client.pl', '/lab/experiment.sock')

def acquire(output):
    label = 'gnu6-05g-' + uuid.uuid4().hex[:14]
    name = label + '-service'
    uid, gid = os.geteuid(), os.getegid()
    if uid in (SERVICE, UNAUTHORIZED, DAC_OUTSIDER):
        raise RuntimeError('HOST_UID_CONFLICT: fixture IDs must differ from caller')
    if uid == 0:
        raise RuntimeError('ROOT_HOST_CALLER_NOT_ALLOWED: use an ordinary host account')
    record = {'schema': 'gnu6.blobin.replication.raw.v1',
              'experiment_id': 'CUDA-05G-P01',
              'observed_utc': datetime.now(timezone.utc).isoformat(),
              'protocol_commit': '396c36e7aef2271544bb98d025129c6de1a73547',
              'contract_sha256': sha256((BASE / 'CONTRACT.json').read_bytes()).hexdigest(),
              'image': IMAGE, 'identities': {'host_caller': uid, 'host_gid': gid,
                                            'service': SERVICE, 'unauthorized': UNAUTHORIZED,
                                            'dac_outsider': DAC_OUTSIDER},
              'observations': {}, 'commands': {}, 'cleanup': {}}
    image_info = docker('image', 'inspect', IMAGE, '--format', '{{.Id}}')
    required(image_info, 'IMAGE_NOT_IN_LOCAL_CACHE')
    perl_check = docker('run', '--rm', '--pull=never', '--network', 'none',
        '--read-only', '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges',
        '--pids-limit', '16', '--entrypoint', 'perl', IMAGE,
        '-MSocket', '-MIO::Socket::UNIX', '-e', 'print qq(PERL_OK\n)')
    required(perl_check, 'IMAGE_PERL_MODULES_MISSING')
    record['image_digest'] = image_info['stdout'].strip()
    with tempfile.TemporaryDirectory(prefix=label+'-', dir=output) as temp:
        folder = Path(temp)
        for filename in ('server.pl', 'client.pl'):
            shutil.copyfile(BASE / filename, folder / filename)
            (folder / filename).chmod(0o644)
        folder.chmod(0o710) # before CAP_CHOWN and service ownership transfer
        mounted = False
        owner_transferred = False
        try:
            setup = docker('run', '--rm', '--pull=never', '--network', 'none',
                           '--read-only', '--cap-drop', 'ALL', '--cap-add', 'CHOWN',
                           '--security-opt', 'no-new-privileges', '--pids-limit', '24',
                           '--user', '0:0', '--entrypoint', 'chown', '--mount',
                           f'type=bind,source={folder},target=/lab', IMAGE,
                           f'{SERVICE}:{gid}', '/lab')
            record['commands']['setup'] = setup
            required(setup, 'DIRECTORY_OWNER_SETUP')
            owner_transferred = True
            launch = docker('run', '--detach', '--pull=never', '--network', 'none',
                            '--read-only', '--cap-drop', 'ALL',
                            '--security-opt', 'no-new-privileges', '--pids-limit', '32',
                            '--memory', '128m', '--user', f'{SERVICE}:{gid}',
                            '--label', 'org.gnu6.experiment=CUDA-05G',
                            '--name', name, '--entrypoint', 'perl', '--mount',
                            f'type=bind,source={folder},target=/lab',
                            IMAGE, '/lab/server.pl', '/lab/experiment.sock', str(uid))
            record['commands']['server_start'] = launch
            required(launch, 'SERVER_LAUNCH')
            mounted = True
            sock = folder / 'experiment.sock'
            for _ in range(150):
                if sock.is_socket(): break
                time.sleep(.06)
            if not sock.is_socket():
                record['commands']['server_early_log'] = docker('logs', name)
                raise RuntimeError('SERVER_SOCKET_NOT_READY')
            inspection = docker('inspect', '--format',
                                '{{.Config.User}}|{{.HostConfig.UsernsMode}}|'
                                '{{.HostConfig.NetworkMode}}|{{.State.Pid}}', name)
            required(inspection, 'SERVER_INSPECT')
            record['commands']['inspect'] = inspection
            config = inspection['stdout'].strip().split('|')
            if len(config) != 4: raise RuntimeError('UNEXPECTED_INSPECTION_SHAPE')
            record['observations']['host_uid_quad'] = host_uid(int(config[3]))
            record['observations']['dir'] = {'uid': folder.stat().st_uid,
                'gid': folder.stat().st_gid, 'mode': oct(stat.S_IMODE(folder.stat().st_mode))}
            record['observations']['socket'] = {'uid': sock.stat().st_uid,
                'gid': sock.stat().st_gid, 'mode': oct(stat.S_IMODE(sock.stat().st_mode))}
            record['observations']['allowed_before'] = host_client(sock)
            record['observations']['connected_unauthorized'] = other_client(folder, UNAUTHORIZED, gid)
            record['observations']['dac_outsider'] = other_client(folder, DAC_OUTSIDER, DAC_OUTSIDER)
            record['observations']['allowed_after'] = host_client(sock)
            for _ in range(80):
                running = docker('inspect', '--format', '{{.State.Running}}', name)
                if running['stdout'].strip() == 'false': break
                time.sleep(.075)
            record['commands']['server_logs'] = docker('logs', name)
            record['commands']['service_exit'] = docker('inspect', '--format',
                                                       '{{.State.ExitCode}}', name)
        finally:
            if mounted:
                record['cleanup']['container'] = docker('rm', '--force', name)
            if owner_transferred:
                record['cleanup']['ownership'] = docker('run', '--rm', '--pull=never',
                '--network', 'none', '--read-only', '--cap-drop', 'ALL',
                '--cap-add', 'CHOWN', '--security-opt', 'no-new-privileges',
                '--pids-limit', '24', '--user', '0:0', '--entrypoint', 'chown', '--mount',
                f'type=bind,source={folder},target=/lab', IMAGE,
                f'{uid}:{gid}', '/lab')
            # Refuse to mask a failure of the ownership restoration.
                required(record['cleanup']['ownership'], 'CLEANUP_OWNER_RESTORE')
            else:
                record['cleanup']['ownership'] = {'code': 0, 'stdout': 'SKIPPED_NO_OWNERSHIP_CHANGE', 'stderr': ''}
            folder.chmod(0o700)
    return record

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True,
                        help='PRIVATE absolute evidence directory outside the Git repository')
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_absolute() or BASE in output.parents or output == BASE:
        raise SystemExit('RAW_EVIDENCE_MUST_BE_OUTSIDE_PUBLIC_KIT')
    output.mkdir(parents=True, exist_ok=True)
    path = output/'raw.json'
    if path.exists(): raise SystemExit('RAW_ALREADY_EXISTS: never overwrite evidence')
    try:
        record = acquire(output)
    except Exception as error:
        failure = {'schema': 'gnu6.blobin.replication.setup-failure.v1',
                   'utc': datetime.now(timezone.utc).isoformat(),
                   'stage': 'acquisition', 'error': str(error)}
        (output/'failure.json').write_text(json.dumps(failure, indent=2)+'\n')
        raise
    path.write_text(json.dumps(record, indent=2, sort_keys=True)+'\n')
    print('CUDA05G_RAW_ACQUIRED private_path='+str(path)+' scenarios=4')
if __name__ == '__main__':main()
