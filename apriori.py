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
        _p_ = p
#        print(_p_)
        for q in L.copy():
            _q_ = q
#            print('\t', _q_)
            if _p_[:-1] == _q_[:-1] and _p_[len(_p_)-1] < _q_[len(_q_)-1]:
                _p_.append(_q_[len(_q_)-1])
                C_k.append(_p_)
    return C_k
        
def prune(candidates):
    pass

def eliminate_rules(itemsets, data):
    rules = []
    for i in range(len(itemsets)):
        count = 0
        for j in data:
            if set(itemsets[i]).issubset(set(j)):
                count += 1
        if float(count/len(data)) >= minsup:
            rules.append(sorted(itemsets[i]))
    return rules

def apriori(data, epsilon):
    C_k = []
    #1-length candidates (every unique value in the data)
    values, counts = np.unique(data, return_counts=True)
    for i in range(len(values)):
        if float(counts[i]/len(data)) > minsup:
            C_k.append(values[i])
    #2-length candidates
    itemset = eliminate_rules(list(combinations(C_k, 2)), data)
    
    candidates = candidate_itemset_generation(itemset)
    for i in candidates:
        print(i)

if __name__ == '__main__':
    train_file = 'yelp5.csv'#sys.argv[1]
    minsup = 0#float(sys.argv[2])
    minconf = 0.75#float(sys.argv[3])

    data = pd.read_csv(train_file, delimiter=',', index_col=None, engine='python')
    data = data.head(5)
    pre_process(data)
    data = data.values
    
        
#    for item in f_items:
#        print('FREQUENT-ITEMS ', item.size, ' ', item.count)
#    for item in a_rules:
#        print('ASSOCIATION-RULES ', item.size, ' ', item.count)
