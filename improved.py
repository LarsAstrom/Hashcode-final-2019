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
    '''
    def totalTime(target):
        File = ns.compilable[ns.name2id[target.name]]
        return sum(ns.compilable[dep].c for dep in File.deps)
    ns.targets.sort(key=totalTime)
    '''
    ns.targets.sort(key=lambda x:-x.d)
    def is_compable(comp,s,t):
        for dep in comp.orig_deps:
            if cur_comp_files[s][dep]>t: return False
        return True
    def get_first_time(comp,server_id,last_t):
        st = 0
        for sti,eni in used[server_id]:
            for x in range(st,sti-comp.c+1):
                if is_compable(comp,server_id,x):
                    return x
                    #return sti-comp.c
            st = eni
        for x in range(st,last_t-comp.c+1):
            if is_compable(comp,server_id,x):
                return x
        return None
    def reset(cur_used):
        for server,interval,_ in cur_used:
            used[server].remove(interval)
    def update_best_server(file):
        best,server_id = INF,-1
        for server in range(ns.S):
            pot_time = get_first_time(file,server,target.d)
            if pot_time == None: continue
            if pot_time < best: best,server_id = pot_time,server
        if server_id == -1:
            return True
        any_updated = False
        if cur_comp_files[server_id][file.i]>best+file.c:
            cur_comp_files[server_id][file.i] = best+file.c
            any_updated = True
        for server in range(ns.S):
            if cur_comp_files[server][file.i]>best+file.c+file.r:
                cur_comp_files[server][file.i] = best+file.c+file.r
        if any_updated:
            cur_used.append((server_id,(best,best+file.c),file))
            used[server_id].append((best,best+file.c))
            used[server_id].sort()
        return False
    while ns.targets:
        print 'Number of targets left: {}'.format(len(ns.targets))
        best = INF
        best_ccf, best_cu = [],[]
        best_target = None
        torem = []
        for target in ns.targets:
            comp = target.get_comp(ns)
            all_deps = sorted(list(comp.deps))
            cur_used = [] #(server,(interval))
            cur_comp_files = [list(x) for x in comp_files]

            fail = False
            for dep in all_deps:
                dep_comp = ns.compilable[dep]
                fail &= update_best_server(dep_comp)
            fail &= update_best_server(comp)
            finish_time = min([cur_comp_files[s][comp.i] for s in range(ns.S)])
            if finish_time > target.d: fail = True
            reset(cur_used)
            if fail:
                torem.append(target)
            elif finish_time < best:
                best,best_ccf,best_cu,best_target = finish_time,cur_comp_files,cur_used,target
        if best != INF:
            comp_files = best_ccf
            for server,interval,dep_comp in best_cu:
                used[server].append(interval)
                used[server].sort()
                out_ish[server][interval] = dep_comp
            ns.targets.remove(best_target)
        for rm in torem: ns.targets.remove(rm)
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
