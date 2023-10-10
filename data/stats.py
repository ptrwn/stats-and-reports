from typing import List
import pandas as pd
from pandas.errors import EmptyDataError


def stat_counter(df: pd.DataFrame) -> pd.DataFrame:
    '''Gets summary of satisfaction scores from stats df'''
        
    if df.empty:
        raise EmptyDataError('Empty dataframe')

    all_scores_num = len(df)
    mixed_num = df.loc[df['Primary reason'] == 'Mixed feedback'].shape[0]
    duplicates_num = df.loc[df['Primary reason'] == 'Duplicate'].shape[0]
    df_relevant = df.loc[~df['Primary reason'].isin(['Mixed feedback', 'Duplicate'])]
    df_count = df_relevant['Rating'].value_counts().reset_index()
    counter = dict(zip(df_count['Rating'], df_count['count']))
    csat = (counter['VSAT'] + counter['SAT']) / all_scores_num
    num_relevant_surveys = all_scores_num - mixed_num - duplicates_num

    return {
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


def get_data_per_customers(df: pd.DataFrame, cust_names: List[str]) -> pd.DataFrame:
    '''Gets data for specific customer(s) only'''

    return df.loc[df['Company'].isin(cust_names)]


def get_dsat_reasons(df: pd.DataFrame) -> pd.DataFrame:
    '''Gets primary reasons for negative feedback'''

    negative = df.loc[df['Rating'].isin(['Neutral', 'DSAT', 'VDSAT'])]
    dsat_reasons = negative['Primary reason'].value_counts().to_frame().reset_index()
    dsat_reasons['reas_pct'] = 100 * dsat_reasons['count'] / dsat_reasons['count'].sum()

    return dsat_reasons