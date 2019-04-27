import argparse
import random
from score import parse

# inp is an input file as a single string
# return your output as a string
def solve(seed, inp, log):
    # TODO: Solve the problem
    random.seed(seed)
    ns = parse(inp)
    sourcefiles=set()
    targetfiles=set()
    for targ in ns.targets:
        comp = targ.get_comp(ns)

        if len(comp.deps)==len(comp.orig_deps)==100:
            print "--------"
            print len(comp.deps), len(comp.orig_deps), targ.d, targ.g
            tottime=0
            for depid in comp.deps:
                dep = ns.compilable[depid]
                print dep.c, dep.r, len(dep.deps)
                tottime+=dep.c
            print tottime, comp.c, targ.d
            print str(sorted(list(comp.deps))[:10]) +  str(sorted(list(comp.deps))[-10:])
    return '0'
