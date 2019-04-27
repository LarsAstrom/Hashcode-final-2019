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
    ns.targets.remove(rm)
    INF = 10**18
    out_ish = {s:{} for s in range(ns.S)}
    comp_files = [[INF]*ns.C for _ in range(ns.S)] #comp_files[server][file] = time_for_avail
    used = [[] for _ in range(ns.S)] #used[server] = [(intervals when used)]
    def is_compable2(comp,s,t):
        for dep in comp.orig_deps:
            if comp_files[s][dep]>t: return False
        return True
    def get_first_time(comp,server_id,last_t):
        st = 0
        for sti,eni in used[server_id]:
            for x in range(st,sti-comp.c+1):
                if is_compable(comp,server_id,x):
                    return x
            st = eni
        for x in range(st,last_t-comp.c+1):
            if is_compable(comp,server_id,x):
                return x
        return None
    def get_first_time2(comp,server_id,last_t):
        st = 0
        for sti,eni in used[server_id]:
            for x in range(st,sti-comp.c+1):
                if is_compable2(comp,server_id,x):
                    return x
            st = eni
        for x in range(st,last_t-comp.c+1):
            if is_compable2(comp,server_id,x):
                return x
        return None
    def is_compable(comp,s,t):
        for dep in comp.orig_deps:
            if cur_comp_files[s][dep]>t: return False
        return True
    for o in outpre:
        name, server = o.split()
        server = int(server)
        file = ns.compilable[ns.name2id[name]]
        start = get_first_time2(file,server,INF)
        interval = (start,start+file.c)
        comp_files[server][file.i] = min(start+file.c, comp_files[server][file.i])
        for s in range(ns.S):
            comp_files[s][file.i] = min(start+file.c+file.r, comp_files[s][file.i])
        used[server].append(interval)
        out_ish[server][interval] = file

    ns.targets.sort(key=lambda x:x.d)

    def reset(cur_used):
        for server,interval,_ in cur_used:
            used[server].remove(interval)
    for targ_ii,target in enumerate(ns.targets):
        if ((targ_ii+1)*100/ns.T)%5 == 0 and ((targ_ii)*100/ns.T)%5 != 0:
            print '{} % of targets done'.format(((targ_ii+1)*100/ns.T))
        comp = target.get_comp(ns)
        all_deps = sorted(list(comp.deps))
        cur_used = [] #(server,(interval))
        cur_comp_files = [list(x) for x in comp_files]
        fail = False
        for dep_ii,dep in enumerate(all_deps):
            best,server_id = INF,-1
            dep_comp = ns.compilable[dep]
            for server in range(ns.S):
                pot_time = get_first_time(dep_comp,server,target.d)
                if pot_time == None: continue
                if pot_time < best: best,server_id = pot_time,server
            if server_id == -1:
                fail = True
                break
            any_updated = False
            if cur_comp_files[server_id][dep]>best+dep_comp.c:
                cur_comp_files[server_id][dep] = best+dep_comp.c
                any_updated = True
            for server in range(ns.S):
                if cur_comp_files[server][dep]>best+dep_comp.c+dep_comp.r:
                    cur_comp_files[server][dep] = best+dep_comp.c+dep_comp.r
                    any_updated = True
            if any_updated:
                cur_used.append((server_id,(best,best+dep_comp.c),dep_comp))
                used[server_id].append((best,best+dep_comp.c))
                used[server_id].sort()
        best,server_id = INF,-1
        #FIXA S} vi inte g;r saker vi inte hinner.
        for server in range(ns.S):
            pot_time = get_first_time(comp,server,target.d)
            if pot_time == None: continue
            if pot_time < best: best,server_id = pot_time,server
        if server_id == -1:
            fail = True
        else:
            any_updated = False
            if cur_comp_files[server_id][comp.i]>best+comp.c:
                cur_comp_files[server_id][comp.i] = best+comp.c
                any_updated = True
            for server in range(ns.S):
                if cur_comp_files[server][comp.i]>best+comp.c+comp.r:
                    cur_comp_files[server][comp.i] = best+comp.c+comp.r
                    any_updated = True
            if any_updated:
                cur_used.append((server_id,(best,best+comp.c),comp))
                used[server_id].append((best,best+comp.c))
                used[server_id].sort()
        if cur_comp_files[server_id][comp.i] > target.d: fail = True
        if fail:
            reset(cur_used)
        else:
            comp_files = cur_comp_files
            for server,interval,dep_comp in cur_used:
                out_ish[server][interval] = dep_comp
    out = []
    for server in range(ns.S):
        for interval in out_ish[server]:
            out.append((interval[0],out_ish[server][interval].name,server))
    out.sort()
    out2 = [(o[1],o[2]) for o in out]
    out = out2
    #print out
    print len(out)
    out2 = [str(len(out))] + [' '.join(map(str,o)) for o in out]
    #print '\n'.join(out2)
    return '\n'.join(out2)
