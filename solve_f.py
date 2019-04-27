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
        if len(comp.deps)!=len(comp.orig_deps):
            print "inte samma", comp.name, len(comp.deps)
    #Alla targets har bara djup 1 av dependencies.
    takeable = []
    for targ in ns.targets:
        comp = targ.get_comp(ns)
        tottime=0
        for depid in comp.deps:
            dep = ns.compilable[depid]
            tottime+=dep.c
        if comp.c <= targ.d:
            print "kan ta", tottime, comp.c, targ.d
            takeable.append(targ)

    print len(takeable)
    out = []
    for i in range(75):
        targ = takeable[i]
        comp = targ.get_comp(ns)
        tottime=0
        for depid in comp.deps:
            dep = ns.compilable[depid]
            out.append(dep.name + " " + str(i))
        out.append(comp.name + " " + str(i))
    outstr=str(len(out))
    outstr2="\n".join(out)

    return outstr+"\n" + outstr2
