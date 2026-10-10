#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Run CPU, true CUDA and true Vulkan in a fresh external directory, no GPU reset."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

BASE=Path(__file__).resolve().parent
PROTOCOL='b89b266829b396d5b9569e0cbb2cd38a04f603bb'
FIXTURE='77759079523ca127a4c24617b42a05a08c5a7c03ebdeb36b092b9ed91387fc86'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def step(args,timeout=90):
    try:
        completed=subprocess.run(args,text=True,capture_output=True,timeout=timeout)
        return {'exit':completed.returncode,'stdout':completed.stdout[:1600],
            'stderr':completed.stderr[:2200],'command_argv':args}
    except subprocess.TimeoutExpired:
        return {'exit':None,'stdout':'','stderr':'TIMEOUT','command_argv':args}
def must(record,label):
    if record['exit']!=0:raise RuntimeError(label+' '+str(record))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output-root',type=Path,required=True)
    args=ap.parse_args()
    root=args.output_root.resolve()
    if BASE==root or BASE in root.parents:
        raise SystemExit('REFUSE_RAW_OUTPUT_IN_PUBLIC_SOURCE')
    root.mkdir(parents=True,exist_ok=True)
    out=root/('trial-'+uuid.uuid4().hex[:12])
    out.mkdir(mode=0o700)
    record={'schema':'gnu6.blobin.gpu.raw.v1','experiment_id':'CUDA-05H-P01',
      'protocol_commit':PROTOCOL,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'fixture_sha256':sha(BASE/'primitives.bin'),
      'contract_sha256':sha(BASE/'CONTRACT.json'),'steps':{},'tool_versions':{},'source_hashes':{},
      'outputs':{},'environment':{}}
    (out/'raw.json').write_text(json.dumps(record,indent=2)+'\n')
    try:
        if record['fixture_sha256']!=FIXTURE:raise RuntimeError('FIXTURE_HASH_CHANGED')
        files=['primitives.bin','oracle.py','cuda.cu','compute.comp','vulkan.c','CONTRACT.json']
        record['source_hashes']={name:sha(BASE/name) for name in files}
        for tool,args0 in [('nvcc',['nvcc','--version']),('cc',['cc','--version']),
                            ('glslang',['glslangValidator','--version']),
                            ('python',['python3','--version']),
                            ('nvidia',['nvidia-smi','--query-gpu=name,driver_version','--format=csv,noheader'])]:
            value=step(args0,10);must(value,'PREFLIGHT_'+tool)
            record['tool_versions'][tool]={'stdout':value['stdout'][-950:],'exit':value['exit']}
        record['environment']={'platform':step(['uname','-sr'],10)['stdout'].strip(),
             'observed_hardware':'RTX 3070 (see backend stderr in private raw)',
             'outcome_scope':'one host, CPU + CUDA + Vulkan, deterministic integer proxy'}
        bin_cuda=out/'cuda';bin_vk=out/'vulkan';spirv=out/'compute.spv'
        commands={
         'compile_cuda':['nvcc','-std=c++17','-O2','-o',str(bin_cuda),str(BASE/'cuda.cu')],
         'compile_spirv':['glslangValidator','-V',str(BASE/'compute.comp'),'-o',str(spirv)],
         'compile_vulkan':['cc','-std=c11','-O2','-Wall','-Wextra','-Werror',str(BASE/'vulkan.c'),'-o',str(bin_vk),'-lvulkan'],
         'cpu':['python3',str(BASE/'oracle.py'),'--scene',str(BASE/'primitives.bin'),'--out',str(out/'cpu.bin')],
         'cuda':[str(bin_cuda),str(BASE/'primitives.bin'),str(out/'cuda.bin')],
         'vulkan':[str(bin_vk),str(BASE/'primitives.bin'),str(spirv),str(out/'vulkan.bin')],
        }
        for name,command in commands.items():
            receipt=step(command,120 if name.startswith('compile') else 45)
            record['steps'][name]=receipt
            must(receipt,name)
        for name in ('cpu','cuda','vulkan'):
            target=out/(name+'.bin')
            record['outputs'][name]={'size':target.stat().st_size,'sha256':sha(target)}
        record['status']='ACQUIRED'
    except Exception as exc:
        record['status']='FAILED_OR_BLOCKED';record['error']=str(exc)[:1400]
        raise
    finally:
        (out/'raw.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
        print('CUDA05H_PRIVATE_ACQUISITION '+str(out/'raw.json')+' status='+record.get('status','UNKNOWN'),flush=True)
if __name__=='__main__':main()
