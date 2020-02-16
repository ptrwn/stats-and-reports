import pandas as pd
import numpy as np
from pathlib import Path


def get_df():

    data_folder = Path("C:/Users/1/prg/py/jupy and tresh/DSATs/")

    file_to_open = data_folder / "CSAT ALL.csv"

    # reading the .csv
    # the .csv is prepared manually, updated with DSAT analysis
    df = pd.read_csv(file_to_open, keep_default_na=False, na_values=np.nan)

    # replace empty strings with NaN
    df.replace('', np.nan, inplace=True)

    # convert timestamps from string to datetime
    df[['Survey Received Time']] = pd.to_datetime(df['Survey Received Time'], format='%m/%d/%Y %H:%M')

    # convert Ticket Id from string to int64
    df[['Ticket Id']] = pd.to_numeric(df['Ticket Id'])

    return df


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


# cut data for a period
def get_df_period(df, beg, end):
    # begp = pd.Timestamp('2019-07-01 00:00:00')
    # endp = pd.Timestamp('2019-07-31 23:59:59')
    begp = pd.Timestamp(beg)
    endp = pd.Timestamp(end)
    df_per = df.loc[(df['Survey Received Time'] > begp) & (df['Survey Received Time'] < endp)]
    df_per.sort_values(by='Survey Received Time')
    return df_per


# cut data for specific customer(s) only
def get_cust(d, *cust_names):
    res = pd.DataFrame()
    for name in cust_names:
        d_cust = d.loc[d['Company'] == name]
        res = pd.concat([res, d_cust])
    return res

# get numbered list of customers present in a df
def get_list_of_customers(d):
        custs = d['Company'].value_counts().to_frame().reset_index()

        res = {}
        for item in list(enumerate(custs.iloc[0:]['index'], 1)):
            res[item[0]] = item[1]

        return res


def get_dsat_reason(d):
    # get primary reasons for negative feedback
    negative = d.loc[d['Rating'].isin(['Neutral', 'DSAT', 'VDSAT'])]
    dsat_reasons = negative['Primary reason'].value_counts().to_frame().reset_index()
    dsat_reasons['reas_pct'] = dsat_reasons['Primary reason'] / dsat_reasons['Primary reason'].sum()

    return dsat_reasons