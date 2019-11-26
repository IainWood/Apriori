import pandas as pd
import numpy as np
import sys
from itertools import combinations

def pre_process(data):
    data['open'] = ['open' if row == 1 else 'closed' for row in data['open']]
    data['goodForGroups'] = ['good' if row == 1 else 'bad' for row in data['goodForGroups']]
    data['priceRange'] = [str(row) for row in data['priceRange']]
    data['delivery'] = ['delivery' if row == True else 'dine_in' for row in data['delivery']]
    data['waiterService'] = ['waiter' if row == True else 'self_serve' for row in data['waiterService']]
    data['caters'] = ['caters' if row == True else 'no_caters' for row in data['caters']]

def candidate_itemset_generation(L):
    '''
    self-join
    insert into C_k
    select p.item1, ..., p.item_m, q.item_m
    from L_k-1 as p, L_k-1 as q
    where p.item_1=q.item_1, ..., p.item_m-1=qitem_m-1, p.item_m < q.item_m
    '''
    C_k = []
    for p in L.copy():
        for q in L.copy():
            if p[:-1] == q[:-1] and p[len(p)-1] < q[len(q)-1]:
                p.append(q[len(q)-1])
                C_k.append(p)
    return prune(C_k, L)

def prune(C_k, L):
    '''
    For all itemsets c in C_k
        For all (k-1) subsets s of c
            If s not in L_k-1 then delete c from C_k
    '''
    for c in C_k:
        #subsets = list(itertools.combinations(c, len(c) - 1))
        for s in list(itertools.combinations(c, len(c) - 1)):
            if s not in L:
                C_k.remove(c)
    return C_k

def frequent_itemset_generation(D, minsup):
    #C_k = []
    L_k = []
    L_union = []
    values, counts = np.unique(D, return_counts=True)
    for i in range(len(values)):
        if float(counts[i]/len(D)) > minsup:
            L_k.append(values[i])

    print(L_k)
    while not L_k.empty():
        L_union.append(L_k)
        C_k1 = candidate_itemset_generation(L_k, minsup)
        L_k = []

        for c in C_k1:
            count = 0
            for t in D:
                if set(c).issubset(set(t)):
                    count += 1
            if float(count/len(D)) >= minsup:
                L_k.append(sorted(c))

    print(L_union)
    return L_union


def rule_generation(L, minconf):
    k = 1
    while not L.empty():
        H = L[0]
        m = 1
        while not H.empty():
            if k > m + 1:
                H = #generate rules from R_m
                R = #select candidates in H with minconf
            m += 1
        k += 1

def apriori(data, minsup, minconf):
    L = frequent_itemset_generation(data, minsup)
    R = rule_generation(L, minconf)
    return R

if __name__ == '__main__':
    train_file = 'yelp5.csv'#sys.argv[1]
    minsup = 0.25#float(sys.argv[2])
    minconf = 0.75#float(sys.argv[3])

    data = pd.read_csv(train_file, delimiter=',', index_col=None, engine='python')
    data = data.head(5)
    pre_process(data)
    data = data.values
    apriori(data, minsup, minconf)

#    for item in f_items:
#        print('FREQUENT-ITEMS ', item.size, ' ', item.count)
#    for item in a_rules:
#        print('ASSOCIATION-RULES ', item.size, ' ', item.count)
