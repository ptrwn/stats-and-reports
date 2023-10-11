import pandas as pd
import numpy as np
from typing import List
from datetime import datetime

def random_timestamps(start: datetime, end: datetime, size: int) -> List[datetime]:
    '''Returns a list of random timestamps between start and end dates.'''

    startp = pd.Timestamp(start)
    endp = pd.Timestamp(end)
    dts = (endp - startp).total_seconds()
    return [startp + pd.Timedelta(np.random.uniform(0, dts), 's') for _ in range(size)]


def make_sample_df(startp: datetime, endp: datetime, size: int) -> pd.DataFrame:
    '''Generates a df that mimics export from ticket processing tool.'''

    lipsum = 'Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua Ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur Excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum'
    c_names = list(set(lipsum.lower().split(' ')))

    df = pd.DataFrame(columns=['Survey Received Time', 'Ticket Id', 'Rating', 'Company', 'Group', 'Primary reason', 'QA score'])

    dsat_reasons = ['resolution delay', 'resolution quality', 'follow-up adherence', 'product bug', 'product usability',
                    'support resources', 'other', 'unmanaged expectations', 'Mixed feedback', 'Duplicate']

    columns_to_fill = {
        'Primary reason': dsat_reasons,
        'Customer_region': ['AMER', 'EMEA', 'APAC', 'EUR'],
        'Group': ['A', 'B', 'C', 'D'],
        'Company':  c_names,
        'Rating': ['VSAT', 'SAT', 'Neutral', 'DSAT', 'VDSAT'],
    }

    df['Ticket Id'] = np.random.randint(200, 9000, size=size)
    df['QA score'] = np.random.randint(80, 110, size=size)
    df['Survey Received Time'] = random_timestamps(startp, endp, size)
    
    for key in ['Customer_region', 'Group', 'Company', 'Rating']:
        df[key] = np.random.choice(columns_to_fill[key], size=size)

    # dissatisfaction reasons make sense only for negative surveys
    negatives = ['Neutral', 'DSAT', 'VDSAT']
    size_negative = df[df['Rating'].isin(negatives)].shape[0]
    df.loc[df['Rating'].isin(negatives), 'Primary reason'] = np.random.choice(dsat_reasons, size=size_negative)
    
    return df

