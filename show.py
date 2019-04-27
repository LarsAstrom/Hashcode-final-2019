import argparse
import random
from score import parse, nl, ni
import sys

# ns is the namespace.
# If needed write a simple parser which returns ns.
# If simple parser should be used run the program with extra argument ('sp')
def test(inp):
    sumg = 0
    for s,d,g in itr[2*ns.C+1:2*ns.C+1+ns.T]:
        sumq+=int(g)
    print "C: {}, T: {}, S: {}, sumG: {}".format(ns.C,ns.T,ns.S,sumg)
    # TODO: Write the tests to print given inp.
    # Use parse from score, or write your own (simple_parse)

def simple_parse(inp):
    itr = inp.split('\n')
    ns = argparse.Namespace()
    ns.C, ns.T, ns.S = map(int,itr[0].split())
    return ns

if __name__=='__main__':
    args = sys.argv
    inp = open(args[-1]).read()

    test(inp)
