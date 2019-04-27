import argparse
import random
from score import *

# inp is an input file as a single string
# return your output as a string

def get_partition(deps):
    target = 333334
    
    DP = [[-1]*target for _ in range(len(deps)+1)]
    DP[0][0] = 0
    for i in range(1, len(deps)+1):
        w = deps[i-1][0]
        for g in range(target):
            if DP[i-1][g] != -1:
                DP[i][g] = g
                if g + w < target:
                    DP[i][g+w] = g
    used = []
    X = target-1
    i = len(deps)
    print(DP[-1][-1])
    while i >= 0:
        X2 = DP[i][X]
        i-= 1
        assert X2 != -1
        if X2 != X:
            used.append(i)
        X = X2
    return used


def solve(seed, inp, log):
    # TODO: Solve the problem
    random.seed(seed)
    ns = parse(inp)
    targets = list(ns.targets)
    targets.sort(key = lambda t: -t.g)
    Srvs = [Server(i) for i in range(ns.S)]
    out = []
    for i, t in enumerate(targets):
        if i != 0: continue
        F = t.get_comp(ns)
        deps = []
        for dep in F.deps:
            deps.append((ns.compilable[dep].c, dep))
        deps.sort(reverse=True)
        print(deps)
        DEPS = [[deps[dp_id] for dp_id in get_partition(deps)]]
        deps = [d for d in deps if d not in DEPS[0]]
        DEPS.append([deps[dp_id] for dp_id in get_partition(deps)])
        DEPS.append([d for d in deps if d not in DEPS[1]])
        for s in Srvs:
            for c, dep in DEPS[s.id]:
                s.add_compilation(dep, ns)
                out.append('{} {}'.format(ns.compilable[dep].name, s.id))
        Srvs[0].add_compilation(F.i, ns)
        print(" ".join(str(s.t) for s in Srvs))
        out.append('{} {}'.format(F.name, 0))

    return '\n'.join([str(len(out))] + out)
