def hit_rate_at_k(recommended_list, bought_list, k):
    """calculating hit rate@k"""
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)[:k]
    flags = np.isin(bought_list, recommended_list)

    return (flags.sum() > 0) * 1


def precision_at_k(recommended_list, bought_list, k):
    """calculating precision@k"""
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)[:k]
    flags = np.isin(bought_list, recommended_list)
    return flags.sum() / len(recommended_list)

def money_precision_at_k_(recommended_list, bought_list, prices_recommended, k=5):
    
    recommend_list = np.array(recommended_list)[:k]
    prices_recommended = np.array(prices_recommended)[:k]
    
    flags = np.isin(recommend_list, bought_list)
    
    precision = np.dot(flags, prices_recommended).sum() / prices_recommended.sum()
    
    return precision


def recall(recommended_list, bought_list):
    
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)
    flags = np.isin(bought_list, recommended_list)
    return flags.sum() / len(bought_list)
    

def recall_at_k(recommended_list, bought_list, k):
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)[:k]
    flags = np.isin(bought_list, recommended_list)
    return flags.sum() / len(bought_list)
    

def money_recall_at_k(recommended_list, bought_list, prices_recommended, prices_bought, k):

    recommend_list = np.array(recommended_list)[:k]
    prices_recommended = np.array(prices_recommended)[:k]

    flags = np.isin(bought_list, recommend_list) # что купили
    print('Реальная прибыль:', np.dot(flags, prices_bought).sum())
    print('Потенциальная прибыль:', prices_recommended.sum()) 
    
    # сколько купили / сколько могли купить, если бы все товары были релеванныт
    money_recall = np.dot(flags, prices_bought).sum() / prices_recommended.sum() 
    return money_recall



def map_k(recommended_list, bought_list, k=5):
    U = len(bought_list_3_users) # кол-во юзеров
    mapk = 0

    for rec_list, bought_list in zip(recommended_list, bought_list_3_users):
        bought_list = np.array(bought_list)
        rec_list = np.array(rec_list)[:k]
        # индексы рекомендованного релевантного товара
        relevant_indexes = np.nonzero(np.isin(rec_list, bought_list))[0]
        
        # precision_at_k для каждого юзера
        sum_ = sum([precision_at_k(rec_list, bought_list, k=index_relevant+1) for index_relevant in relevant_indexes])
        
        if len(relevant_indexes) == 0:
            ap_k = 0
        else:
            ap_k = sum_/len(relevant_indexes)
        mapk += ap_k

    return round(mapk/U, 2)



def reciprocal_rank(recommended_list, bought_list, k=5):
    """calculating MRR - finding reciprocal rank 
            through the rank of first relevant recommendation for each user and taking its mean """
    n = len(bought_list_3_users) # кол-во юзеров
    rr_sum = 0

    for rec_list, bought_list in zip(recommended_list, bought_list_3_users):
        bought_list = np.array(bought_list)
        rec_list = np.array(rec_list)[:k]
        # индекс первого релевантного товара
        relevant_indexes = np.nonzero(np.isin(rec_list, bought_list))[0]
        
        # находим первое релевантное предсказание и вычисляем reciprocal rank для каждого юзера
        k_rank = relevant_indexes[True][0]
        if k_rank.size == 0:
            rr = 0
        else:
            rr = 1/(k_rank[0]+1)
            
        rr_sum +=rr

    return round(rr_sum/n, 2)