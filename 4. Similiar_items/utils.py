# положила в отдельный файл, тут оставила для проверки

def prefilter_items(data):
    # Уберем самые популярные товары (их и так купят)
    popularity = data.groupby('item_id')['user_id'].nunique().reset_index() / data['user_id'].nunique()
    popularity.rename(columns={'user_id': 'share_unique_users'}, inplace=True)
    
    top_popular = popularity[popularity['share_unique_users'] > 0.5].item_id.tolist()
    data = data[~data['item_id'].isin(top_popular)]
    
    # Уберем самые НЕ популярные товары (их и так НЕ купят)
    top_notpopular = popularity[popularity['share_unique_users'] < 0.01].item_id.tolist()
    data = data[~data['item_id'].isin(top_notpopular)]
    
    # Уберем товары, которые не продавались за последние 12 месяцев
    # берем самую последнюю покупку каждого айтема
    old_items = data.groupby(by=['item_id'])['item_id', 'week_no'].max()
    # получаем айтемы, которые были куплены последний раз больше года назад
    old_items = list(old_items[old_items['week_no'] <= (data['week_no'].max() - 52)].index)
    data = data[~data['item_id'].isin(old_items)]

    # Уберем не интересные для рекоммендаций категории (department), уберем товары купленные менее 1000 раз
    top_departments = data['department'].value_counts()[lambda x: x > 1000].index
    data = data[data['department'].isin(top_departments)]
    
    # Уберем слишком дешевые товары (на них не заработаем). 1 покупка из рассылок стоит 60 руб.
    # полагаем, что цены на товары в долларах, переведем в рубли по курсу 74.1, чтобы потом отфильтровать все товары ниже стоимости привлечения
    data['price'] = data['sales_value'] / (np.maximum(data['quantity'], 1))
    data['price_rub'] = data['price'] * 74.1
    data = data[data['price_rub'] > 60]
    
    # Уберем слишком дорогие товары
    data = data[data['price'] < data['price'].quantile(0.99995)]
    
    return data 
    
def postfilter_items(user_id, recommednations):
    pass