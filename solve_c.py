import argparse
import random
from score import *

# inp is an input file as a single string
# return your output as a string
def solve(seed, inp, log):

    def build_partition(deps, DP, X):
        used = []
        i = len(deps)
        while i >= 0:
            X2 = DP[i][X]
            i-= 1
            assert X2 != -1
            if X2 != X:
                used.append(i)
            X = X2
        return used
    def get_partition(deps, no):
        target = 3335

        DP = [[-1]*target for _ in range(len(deps)+1)]
        DP[0][0] = 0
        for i in range(1, len(deps)+1):
            w = deps[i-1][0]
            for g in range(target):
                if DP[i-1][g] != -1:
                    DP[i][g] = g
                    if g + w < target:
                        if DP[i][g+w] == -1:
                            DP[i][g+w] = g
        i=3334 if no < 10 else 3333
        while DP[-1][i]==-1:
            i-=1
        return build_partition(deps,DP,i)
    # TODO: Solve the problem
    random.seed(seed)
    ns = parse(inp)
    outpre=[]
    Srvs = [Server(i) for i in range(ns.S)]
    rm=-1
    for targ in ns.targets:
        comp = targ.get_comp(ns)
        t = targ
        F = t.get_comp(ns)
        if len(comp.deps)==len(comp.orig_deps)==100:
            print "--------"
            print len(comp.deps), len(comp.orig_deps), targ.d, targ.g
            tottime=0
            deps=[]
            for dep in comp.deps:
                deps.append((ns.compilable[dep].c, dep))
            deps.sort(key=lambda x: -x[0])
            DEPS = []
            sums = []
            for _ in range(ns.S):
                DEPS.append([deps[dp_id] for dp_id in get_partition(deps, _)])
                sums.append(sum(c for c, _ in DEPS[-1]))
                deps = [d for d in deps if d not in DEPS[-1]]
            if deps:
                print deps
                print sums
                continue
            for s in Srvs:
                for c, dep in DEPS[s.id]:
                    s.add_compilation(dep, ns)
                    outpre.append('{} {}'.format(ns.compilable[dep].name, s.id))
            Srvs[0].add_compilation(F.i, ns)
            print(" ".join(str(s.t) for s in Srvs))
            outpre.append('{} {}'.format(F.name, 0))
            rm=targ
            break

    return '\n'.join([str(len(outpre))] + outpre)
