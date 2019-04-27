#!/usr/bin/env pypy
from glob import glob
import argparse
import re
from util import path, update_config, get_function, process, clean_max
try:
    from ConfigParser import ConfigParser
except:
    from configparser import ConfigParser

from collections import *


def show(out):
    # TODO: Print the solution here
    print(out)

def ni(itr):
    return int(next(itr))

# parses the next string of itr as a list of integers
def nl(itr):
    return [int(v) for v in next(itr).split()]

class Compilable:
    def __init__(self, i, name, c, r, deps, ns):
        self.i = i
        self.name = name
        self.c = c
        self.r = r
        self.orig_deps = set(deps)
        self.deps = set(deps)
        for d in deps:
            self.deps |= ns.compilable[d].deps


class Target:
    def __init__(self, i, name, d, g):
        self.name = name
        self.d = d
        self.g = g
        self.i = i
    def get_comp(self, ns):
        return ns.compilable[ns.name2id[self.name]]

def parse(inp):
    itr = (line for line in inp.split('\n'))
    ns = argparse.Namespace()
    ns.C, ns.T, ns.S = nl(itr)
    ns.compilable = []
    ns.name2id = {}
    for i in range(ns.C):
        name, c, r = next(itr).split()
        ns.name2id[name] = i
        deps = [ns.name2id[n] for n in next(itr).split()[1:]]
        ns.compilable.append(Compilable(i, name, int(c), int(r), deps, ns))
    ns.targets = []
    for i in range(ns.T):
        name, d, g = next(itr).split()
        ns.targets.append(Target(i, name, int(d), int(g)))

    ns.avil = {}

    return ns

class Server:
    def __init__(self):
        self.t = 0
        self.compiled = set()
    def add_compilation(self, i, ns):
        ok = True
        start = self.t
        File = ns.compilable[i]
        for dep in File.deps:
            if dep in self.compiled: continue
            else:
                assert dep in ns.avil, "file {} not ready".format(dep)
                start = max(start, ns.avil[dep])
        self.compiled.add(i)
        self.t = start + File.c
        if i in ns.avil:
            ns.avil[i] = min(ns.avil[i], self.t + File.r)
        else:
            ns.avil[i] = self.t + File.r



# inp: the input file as a single string
# out: the answer file produced by your solver, as a single string
# return the score of the output as an integer
def score(inp, out):
    ns = parse(inp)
    itr = (line for line in out.split('\n'))
    Srvs = [Server() for _ in range(ns.S)]
    E = ni(itr)
    for _ in range(E):
        name, s_id = next(itr).split()
        s_id = int(s_id)
        f_id = ns.name2id[name]
        Srvs[s_id].add_compilation(f_id, ns)
    tot = 0
    for targ in ns.targets:
        targ_id = ns.name2id[targ.name] 
        if targ_id in ns.avil:
            time = ns.avil[targ_id] - ns.compilable[targ_id].r
            if time <= targ.d:
                tot += targ.g - time + targ.d 
    return tot


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('inp', nargs='?')
    parser.add_argument('ans', nargs='?')
    parser.add_argument('-s', action='store_true', help="show")
    parser.add_argument('--rescore', action='store_true', help="Rescore all ans files in ans/ and copy the best to submission")
    parser.add_argument('-c', '--config', action='store', default='', help="config file")
    parser.add_argument('--score', action='store', default='', help="set scoring config, format: key1=value1,key2=value2")
    return parser.parse_args()


def ans2in(ans):
    pth = path(ans)
    m = fname_re.match(pth.name)

    return (m.group(1) if m else path(ans).name).join(in_f)


sub_f = ('submission/', '.ans')
ans_f = ('ans/', '.ans')
in_f = ('in/', '.in')
fname_re = re.compile(r'([A-Za-z0-9_]+)_(\d+)_(\d+|None)')

if __name__ == '__main__':
    args = get_args()
    if args.rescore:
        clean_max()
    config = ConfigParser()
    config.read(['default.cfg', 'main.cfg', args.config])
    update_config(config, 'score', args.score)

    sc_fn = get_function('score', config)

    if not (args and (args.inp or args.ans)):
        file_lst = glob('*'.join(ans_f if args.rescore else sub_f))
        files = [(ans2in(ans), ans) for ans in file_lst]
    else:
        if not args.ans:
            pth = path(args.inp)
            args.inp = pth.name.join(in_f)
            args.ans = pth.name.join(sub_f)
        files = [(args.inp, args.ans)]

    for inpf, ansf in files:
        ipth, apth = path(inpf), path(ansf)

        inp = ipth.read()
        ans = apth.read()
        case, seed = ipth.name, None
        m = fname_re.match(apth.name)
        if m:
            seed = m.group(3)

        process(inp, ans, seed, sc_fn, case)
