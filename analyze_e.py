import argparse
import random
from score import parse

# inp is an input file as a single string
# return your output as a string
def solve(seed, inp, log):
    # TODO: Solve the problem
    random.seed(seed)
    ns = parse(inp)
    takeable = []
    for targ in ns.targets:
        comp = targ.get_comp(ns)
        tottime=0
        for depid in comp.deps:
            dep = ns.compilable[depid]
            tottime+=dep.c
        if comp.c + tottime//ns.S <= targ.d:
            print "kan ta", tottime, comp.c, targ.d
            takeable.append(targ)

    return '0'
