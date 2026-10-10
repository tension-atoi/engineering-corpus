#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Independent CPU oracle for frozen integer quadratic CSG proxy scene."""
import argparse
from pathlib import Path
import struct
import sys

WIDTH, HEIGHT = 96, 64
PRIMITIVES = 16

def evaluate(scene):
    if len(scene) != PRIMITIVES * 16:
        raise ValueError('SCENE_BYTE_COUNT_INVALID')
    prims = list(struct.iter_unpack('<iiii', scene))
    if prims[0][3] != 0 or any(not (0<=cx<WIDTH and 0<=cy<HEIGHT and
                      3<=r<=19 and 0<=op<=2) for cx,cy,r,op in prims):
        raise ValueError('SCENE_BOUNDS_OR_OP_INVALID')
    pixels = []
    for y in range(HEIGHT):
        for x in range(WIDTH):
            acc = None
            for cx, cy, r, op in prims:
                q = (x-cx)**2 + (y-cy)**2-r*r
                if acc is None or op == 0:
                    acc = q if acc is None else min(acc,q)
                elif op == 1:
                    acc = max(acc,q)
                else:
                    acc = max(acc,-q)
            if not -2**31 <= acc < 2**31:
                raise ValueError('INT32_OVERFLOW')
            pixels.append(acc)
    return struct.pack('<'+'i'*len(pixels),*pixels)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--scene',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    a=parser.parse_args()
    a.out.write_bytes(evaluate(a.scene.read_bytes()))
    print('CPU_ORACLE_WRITTEN samples=6144 format=int32le')
if __name__=='__main__':
    try:main()
    except (OSError, ValueError) as err:sys.exit('CPU_ORACLE_FAIL '+str(err))
