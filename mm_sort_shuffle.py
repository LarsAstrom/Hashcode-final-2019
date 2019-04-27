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
    #cur_comp = 0
    INF = 10**18
    out_ish = {s:{} for s in range(ns.S)}
    comp_files = [[INF]*ns.C for _ in range(ns.S)] #comp_files[server][file] = time_for_avail
    used = [[] for _ in range(ns.S)] #used[server] = [(intervals when used)]
    ns.targets.sort(key=lambda x:-x.d)
    sz = 17
    v = ns.targets[:sz]
    random.shuffle(v)
    ns.targets = v + ns.targets[sz:]
    def is_compable(comp,s,t):
        for dep in comp.orig_deps:
            if cur_comp_files[s][dep]>t: return False
        return True
    def get_first_time(comp,server_id,last_t):
        st = 0
        for sti,eni in used[server_id]:
            for x in range(st,sti-comp.c+1):
                if is_compable(comp,server_id,x):
                    #return x current best
                    return sti-comp.c
            st = eni
        for x in range(st,last_t-comp.c+1):
            if is_compable(comp,server_id,x):
                return x
        return None
    def reset(cur_used):
        for server,int,_ in cur_used:
            used[server].remove(int)
    for targ_ii,target in enumerate(ns.targets):
        if ((targ_ii+1)*100/ns.T)%5 == 0 and ((targ_ii)*100/ns.T)%5 != 0:
            pass #print '{} % of targets done'.format(((targ_ii+1)*100/ns.T))
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
            for server,int,dep_comp in cur_used:
                out_ish[server][int] = dep_comp
    out = []
    for server in range(ns.S):
        for int in out_ish[server]:
            out.append((int[0],out_ish[server][int].name,server))
    out.sort()
    out2 = [(o[1],o[2]) for o in out]
    out = out2
    #print out
    out2 = [str(len(out))] + [' '.join(map(str,o)) for o in out]
    #print '\n'.join(out2)
    return '\n'.join(out2)
