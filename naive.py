import argparse
import random
from collections import defaultdict
from score import parse

# inp is an input file as a single string
# return your output as a string
def solve(seed, inp, log):
    # TODO: Solve the problem
    random.seed(seed)
    ns = parse(inp)
    cur_comp = 0
    comp_files = [[False]*ns.C for _ in range(ns.S)]
    repl = defaultdict(list)
    nxt_avail_time = [0]*ns.S
    MAX_T = max([t.d for t in ns.targets])
    cur_comp_on_server = [-1]*ns.S
    out = []
    def is_compable(comp,s):
        for dep in comp.deps:
            if not comp_files[s][dep]: return False
        return True
    for t in range(MAX_T+1):
        for rep in repl[t]:
            for s in range(ns.S):
                comp_files[s][rep] = True
        for s in range(ns.S):
            if t==nxt_avail_time[s]: comp_files[s][cur_comp_on_server[s]] = True
            if t>=nxt_avail_time[s] and is_compable(ns.compilable[cur_comp],s):
                comp = ns.compilable[cur_comp]
                cur_comp += 1
                nxt_avail_time[s] = t + comp.c
                repl[t+comp.c+comp.r].append(comp.i)
                out.append((comp.name,s))
    print len(out)
    out2 = [str(len(out))] + [' '.join(map(str,o)) for o in out]
    return '\n'.join(out2)
