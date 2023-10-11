import pytest
from io import StringIO
import pandas as pd
from data.stats import stat_counter
from pandas.errors import EmptyDataError


@pytest.fixture(scope='module')
def df():
    input_df = '''
    2019-07-30 23:15:00.124314088,4850,Neutral,duis,B,Duplicate,96,APAC\n
    2019-07-09 22:47:26.539010655,3959,VDSAT,eiusmod,A,other,90,EMEA\n 
    2019-07-05 22:58:20.252717755,1498,VDSAT,occaecat,A,resolution delay,80,EUR\n
    2019-07-20 07:34:47.324367866,4923,SAT,aute,C,,98,EMEA\n
    2019-07-07 19:07:06.682781190,212,SAT,voluptate,C,,83,AMER\n
    2019-07-08 22:48:19.942978919,8540,Neutral,minim,D,other,92,APAC\n
    2019-07-09 02:33:54.804640797,3772,VSAT,ad,B,,84,AMER\n
    2019-07-19 13:16:49.382459539,7977,Neutral,ullamco,C,Mixed feedback,109,AMER\n
    2019-07-19 03:37:40.145909140,6760,SAT,anim,D,,109,APAC\n
    2019-07-29 02:15:53.560788779,8995,VDSAT,aliquip,A,product bug,106,AMER\n
    '''
    columns = ['Survey Received Time', 'Ticket Id', 'Rating', 'Company', 'Group', 'Primary reason', 'QA score', 'Customer_region']

    df = pd.read_csv(StringIO(input_df), header=None)
    df.columns = columns

    yield df


def test_stat_counter_happy(df):
    res = stat_counter(df)
    assert res == {'CSAT score': 0.4, 
                    'All scores': 10, 
                    'Relevant': 8, 
                    'Irrelevant': 2, 
                    'Mixed': 1, 
                    'Duplicate': 1, 
                    'VSAT': 1, 
                    'SAT': 3, 
                    'Neutral': 1, 
                    'DSAT': 0, 
                    'VDSAT': 3}



def test_stats_counter_raises_for_empty_df():
    with pytest.raises(Exception, match="Empty dataframe") as ex:
        df = pd.DataFrame()
        stat_counter(df)
    assert type(ex.value) is EmptyDataError
    assert ex.value.args[0] == 'Empty dataframe'

