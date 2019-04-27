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
        if len(targ.deps)>100:
            print "inte 100", targ.name

    return ''
