import pandas as pd


def stat_counter(d):
        
    if d.empty:
        return "EMPTY FRAME"

    all_scores_num = len(d)
    mixed_num = d.loc[d['Primary reason'] == 'Mixed feedback'].shape[0]
    duplicates_num = d.loc[d['Primary reason'] == 'Duplicate'].shape[0]
    d_relevant = d.loc[~d['Primary reason'].isin(['Mixed feedback', 'Duplicate'])]
    df_count = d_relevant['Rating'].value_counts().reset_index()
    counter = dict(zip(df_count['Rating'], df_count['count']))
    csat = (counter['VSAT'] + counter['SAT']) / all_scores_num
    num_relevant_surveys = all_scores_num - mixed_num - duplicates_num

    res = {
        'CSAT score': csat,
        'All scores': all_scores_num,
        'Relevant': num_relevant_surveys,
        'Irrelevant': mixed_num + duplicates_num,
        'Mixed': mixed_num,
        'Duplicate': duplicates_num,
        'VSAT': counter['VSAT'],
        'SAT': counter['SAT'],
        'Neutral': counter['Neutral'],
        'DSAT': counter['DSAT'],
        'VDSAT': counter['VDSAT']
    }

    return res


def get_cust(d, *cust_names):
    '''Get data for specific customer(s) only'''
    res = pd.DataFrame()
    for name in cust_names:
        d_cust = d.loc[d['Company'] == name]
        res = pd.concat([res, d_cust])
    return res


def get_list_of_customers(d):
        '''Get numbered list of customers present in the df'''
        custs = d['Company'].value_counts().to_frame().reset_index()
        res = {}
        for item in list(enumerate(custs.iloc[0:]['index'], 1)):
            res[item[0]] = item[1]
        return res


def get_dsat_reason(d):
    '''Get primary reasons for negative feedback'''
    negative = d.loc[d['Rating'].isin(['Neutral', 'DSAT', 'VDSAT'])]
    dsat_reasons = negative['Primary reason'].value_counts().to_frame().reset_index()
    dsat_reasons['reas_pct'] = 100 * dsat_reasons['count'] / dsat_reasons['count'].sum()

    return dsat_reasons