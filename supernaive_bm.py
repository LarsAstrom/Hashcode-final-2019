import argparse
import random
from score import parse

# inp is an input file as a single string
# return your output as a string
def solve(seed, inp, log):
    # TODO: Solve the problem
    random.seed(seed)
    ns = parse(inp)
    out=[]
    currserver=0
    for comp in ns.compilable:
        out.append(str(comp.name) + " " + str(currserver))
        currserver+=1
        currserver%= ns.S
    outstr=str(len(out))
    outstr2="\n".join(out)

    return outstr+"\n" + outstr2
