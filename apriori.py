import pandas as pd
import numpy as np
import sys
import copy
from itertools import combinations, chain, groupby

def pre_process(data):
    data['open'] = ['open' if row == 1 else 'closed' for row in data['open']]
    data['goodForGroups'] = ['good' if row == 1 else 'bad' for row in data['goodForGroups']]
    data['priceRange'] = [str(row) for row in data['priceRange']]
    data['delivery'] = ['delivery' if row == True else 'dine_in' for row in data['delivery']]
    data['waiterService'] = ['waiter' if row == True else 'self_serve' for row in data['waiterService']]
    data['caters'] = ['caters' if row == True else 'no_caters' for row in data['caters']]

def candidate_itemset_generation(L):
    '''
    insert into C_k
    select p.item1, ..., p.item_m, q.item_m
    from L_k-1 as p, L_k-1 as q
    where p.item_1=q.item_1, ..., p.item_m-1=qitem_m-1, p.item_m < q.item_m
    '''
    
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
    '''
    For all itemsets c in C_k
        For all (k-1) subsets s of c
            If s not in L_k-1 then delete c from C_k
    '''
    for c in candidates:
        for s in list(combinations(c, len(c) - 1)):
            if list(s) not in L:
                try:
                    candidates.remove(c)
                    break
                except:
                    pass
    return candidates

def eliminate_cand(itemsets, data):
    rules = []
    for i in range(len(itemsets)):
        count = 0
        for j in data:
            if set(itemsets[i]).issubset(set(j)):
                count += 1
        if float(count/len(data)) >= minsup:
            rules.append(sorted(itemsets[i]))
    return rules

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
    return count

def rule_generation(L, freqs, minconf):
    rules, rules_union = [], []
    
    for itemset, freqset in zip(L, freqs):
        for item, freq in zip(itemset, freqset):
#            print(item)
#            subsets = list(combinations(item, len(item) - 1))
#            print(subsets)
#            print(freq)
            
            subsets = chain.from_iterable(combinations(list(item), r) for r in range(2, len(list(item))))
#            for sub in subsets:
#                print(sub)
#            print(list(subsets))
            for X in subsets:
                
#                print('item type: ', type(item))
#                print('X type: ', type(X))
#                print(X)
                Y = set(item) - set(X)
#                print(X, ' -> ', Y, '\tconf: ', get_freq(X)/freq)
#                print(freq/get_freq(X))
                if get_freq(item)/get_freq(X)>= minconf:
                    rules.append((X, Y, len(X) + len(Y)))
#                    print(X, ' -> ', Y, '\tlength: ', str(len(X) + len(Y)))
#            rules_union.append(rules)
    print(rules)
    a_rules = []
    for key, group in groupby():
        a_rules.append(group)
    return a_rules
#    k = 1
#    while L:
#        H = L[0]
#        m = 1
#        while H:
#            if k > m + 1:
#                pass
#                H = #generate rules from R_m
#                R = #select candidates in H with minconf
#            m += 1
#        k += 1

def apriori(data, minsup, minconf):
    L, freqs = frequent_itemset_generation(data, minsup)
        
    R = rule_generation(L, freqs, minconf)
    return L, R

if __name__ == '__main__':
    train_file = 'yelp5.csv'#sys.argv[1]
    minsup = 0.25#float(sys.argv[2])
    minconf = 0.75#float(sys.argv[3])

    data = pd.read_csv(train_file, delimiter=',', index_col=None, engine='python')
    data = data.head(10)
    pre_process(data)
#    print(data)
    data = data.values
    f_items, a_rules = apriori(data, minsup, minconf)

    for item in f_items:
        print('FREQUENT-ITEMS ' + str(len(item[0])) + ' ' + str(len(item)))
    for item in a_rules:
        print('ASSOCIATION-RULES ' + str(len(item[0])) + ' ' + str(len(item)))
