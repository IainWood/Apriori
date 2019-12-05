import pandas as pd
import numpy as np
import sys
import copy
from itertools import combinations, chain

def pre_process(data):
    data['open'] = ['open' if row == 1 else 'closed' for row in data['open']]
    data['goodForGroups'] = ['good' if row == 1 else 'bad' for row in data['goodForGroups']]
    data['priceRange'] = [str(row) for row in data['priceRange']]
    data['delivery'] = ['delivery' if row == True else 'dine_in' for row in data['delivery']]
    data['waiterService'] = ['waiter' if row == True else 'self_serve' for row in data['waiterService']]
    data['caters'] = ['caters' if row == True else 'no_caters' for row in data['caters']]

def candidate_itemset_generation(L):
#    insert into C_k
#    select p.item1, ..., p.item_m, q.item_m
#    from L_k-1 as p, L_k-1 as q
#    where p.item_1=q.item_1, ..., p.item_m-1=qitem_m-1, p.item_m < q.item_m
    L_copy = copy.deepcopy(L)
    p_L_copy = sorted(copy.deepcopy(L))
    q_L_copy = sorted(copy.deepcopy(L))
    C_k = []
    for p in p_L_copy:
        for q in q_L_copy:
            if p[:-1] == q[:-1] and p[len(p)-1] < q[len(q)-1]:
                C_k.append(p + list([q[len(q)-1]]))
    return prune(C_k, L_copy)

def prune(candidates, L):
#    For all itemsets c in C_k
#        For all (k-1) subsets s of c
#            If s not in L_k-1 then delete c from C_k
    for c in candidates:
        for s in list(combinations(c, len(c) - 1)):
            if list(s) not in L:
                try:
                    candidates.remove(c)
                    break
                except:pass
    return candidates

def frequent_itemset_generation(D, minsup):
    #F_k, and F_union are to record the actual frequencies of each frequent itemset
    L_k, F_k = [], []
    L_union, F_union = [], []
    values, counts = np.unique(D, return_counts=True)
    for i in range(len(values)):
        if float(counts[i]/len(D)) >= minsup:
            L_k.append(values[i])

    #get just 2-length candidates
    candidates = list(combinations(L_k, 2))
    L_k = []
    for c in candidates:
        count = 0
        for t in D:
            if set(c).issubset(set(t)):
                count += 1
        if float(count/len(data)) >= minsup:
            L_k.append(sorted(c))
            F_k.append(float(count/len(data)))

    #apriori part
    while L_k:
        L_union.append(L_k)
        F_union.append(F_k)
        C_k = candidate_itemset_generation(L_k)
        L_k = []

        for c in C_k:
            count = 0
            for t in D:
                if set(c).issubset(set(t)):
                    count += 1
            if float(count/len(D)) >= minsup:
                L_k.append(sorted(c))
                F_k.append(float(count/len(D)))
    return L_union, F_union

def get_freq(item):
    count = 0
    for t in data:
        if set(item).issubset(set(t)):
            count += 1
    return float(count/len(data))

def rule_generation(L, freqs, minconf):
    rules, rules_union, counts = [], [], []

    for itemset, freqset in zip(L, freqs):
        rules = []
        for item, freq in zip(itemset, freqset):
            #create antecedents from all of the subsets
            for ante in chain.from_iterable(combinations(list(item), len) for len in range(1, len(list(item)))):
                #compute the consequents
                conseq = set(item) - set(ante)
                #select those above minimum confidence
                if freq/get_freq(ante) >= minconf:
                    rules.append(len(ante) + len(conseq))
        rules_union.append(rules)

    values = np.unique(rules_union)
    for i in range(len(values) - 1):
        counts.append([values[i][0], len(values[i])])
    return counts

def apriori(data, minsup, minconf):
    L, freqs = frequent_itemset_generation(data, minsup)
    R = rule_generation(L, freqs, minconf)
    #print results
    for item in L:
        print('FREQUENT-ITEMS ' + str(len(item[0])) + ' ' + str(len(item)))
    for item in R:
        print('ASSOCIATION-RULES ' + str(item[0]) + ' ' + str(item[1]))

if __name__ == '__main__':
    train_file = sys.argv[1]
    minsup = float(sys.argv[2])
    minconf = float(sys.argv[3])
    
    data = pd.read_csv(train_file, delimiter=',', index_col=None, engine='python')
    data = data['goodForGroups']
    pre_process(data)
    data = data.values
    apriori(data, minsup, minconf)
