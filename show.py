import argparse
import random
from score import parse, nl, ni
import sys

# ns is the namespace.
# If needed write a simple parser which returns ns.
# If simple parser should be used run the program with extra argument ('sp')
def test(inp):
    ns = parse(inp)
    sumg=0
    maxd=0
    min_dep = (10**10, -1)
    max_dep = (0, -1)
    deps = []
    for t in ns.targets:
        sumg+=t.g
        maxd=max(maxd,t.d)
        F = t.get_comp(ns)
        deps.append((len(F.deps), t.i, t.g, t.d))
    print "C: {}, T: {}, S: {}, sumG: {}, maxD: {}".format(ns.C,ns.T,ns.S,sumg, maxd)
    deps.sort()
    for d in deps[:20]:
        print(d)
    # TODO: Write the tests to print given inp.
    # Use parse from score, or write your own (simple_parse)

def simple_parse(inp):
    itr = inp.split('\n')
    ns = argparse.Namespace()
    ns.C, ns.T, ns.S = map(int,itr[0].split())
    ns.sumg = 0

    for line in itr[2*ns.C+1:2*ns.C+1+ns.T]:
        s,d,g = line.split()
        ns.sumg+=int(g)
    return ns

if __name__=='__main__':
    args = sys.argv
    inp = open(args[-1]).read()

    test(inp)
