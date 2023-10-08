import pandas as pd


def stat_counter(d):

    all_scores_num = len(d)

    def weight(num):
        return num / all_scores_num

    if all_scores_num == 0:
        print("EMPTY FRAME")
        return "EMPTY FRAME"

    mixed_set = d.loc[d['Primary reason'] == 'Mixed feedback']
    mixed_num = len(mixed_set)

    duplicates_set = d.loc[d['Primary reason'] == 'Duplicate']
    duplicates_num = len(duplicates_set)

    d = d[d['Primary reason'] != 'Mixed feedback']
    d = d[d['Primary reason'] != 'Duplicate']

    vsat_set = d.loc[d['Rating'] == 'VSAT']
    vsat_num = len(vsat_set)

    sat_set = d.loc[d['Rating'] == 'SAT']
    sat_num = len(sat_set)

    neu_set = d.loc[d['Rating'] == 'Neutral']
    neu_num = len(neu_set)

    dsat_set = d.loc[d['Rating'] == 'DSAT']
    dsat_num = len(dsat_set)

    vdsat_set = d.loc[d['Rating'] == 'VDSAT']
    vdsat_num = len(vdsat_set)

    csat = weight(vsat_num + sat_num)
    irrelev_part = weight(mixed_num + duplicates_num)
    num_actual_surveys = all_scores_num - mixed_num - duplicates_num

    res = {
        'CSAT score': csat,
        'All scores': all_scores_num,
        'Relevant': num_actual_surveys,
        'Irrelevant': mixed_num + duplicates_num,
        'Mixed': mixed_num,
        'Duplicate': duplicates_num,
        'VSAT': vsat_num,
        'SAT': sat_num,
        'Neutral': neu_num,
        'DSAT': dsat_num,
        'VDSAT': vdsat_num
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
        '''Get numbered list of customers present in a df'''
        custs = d['Company'].value_counts().to_frame().reset_index()
        res = {}
        for item in list(enumerate(custs.iloc[0:]['index'], 1)):
            res[item[0]] = item[1]
        return res


def get_dsat_reason(d):
    '''Get primary reasons for negative feedback'''
    negative = d.loc[d['Rating'].isin(['Neutral', 'DSAT', 'VDSAT'])]
    dsat_reasons = negative['Primary reason'].value_counts().to_frame().reset_index()
    dsat_reasons['reas_pct'] = dsat_reasons['count'] / dsat_reasons['count'].sum()

    return dsat_reasons