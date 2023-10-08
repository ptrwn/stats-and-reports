# generates a test file similar to export from ticket processing tool
import pandas as pd
import numpy as np


def random_timestamp(start, end):
    '''Returns a random timestamp between start and end'''

    startp = pd.Timestamp(start)
    endp = pd.Timestamp(end)
    dts = (endp - startp).total_seconds()
    return startp + pd.Timedelta(np.random.uniform(0, dts), 's')


def make_sample_df(startp, endp, size):
    '''Returns a df filled in with test data'''

    lipsum = 'Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua Ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur Excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum'
    c_names = list(set(lipsum.lower().split(' ')))

    df = pd.DataFrame(columns=['Survey Received Time', 'Ticket Id', 'Rating', 'Company', 'Group', 'Primary reason', 'QA score'])

    dsat_reasons = ['resolution delay', 'resolution quality', 'follow-up adherence', 'product bug', 'product usability',
                    'support resources', 'other', 'unmanaged expectations', 'Mixed feedback', 'Duplicate']

    names = {
        'Primary reason': dsat_reasons,
        'Customer_region': ['AMER', 'EMEA', 'APAC', 'EUR'],
        'Group': ['A', 'B', 'C', 'D'],
        'Company':  c_names,
        'Rating': ['VSAT', 'SAT', 'VDSAT', 'Neutral', 'DSAT'],
    }

    df['Ticket Id'] = np.random.randint(200, 9000, size=size)
    df['QA score'] = np.random.randint(80, 110, size=size)
    
    for item in df.index:
        df.at[item, 'Survey Received Time'] = random_timestamp(startp, endp)

    for key in names.keys():
        df[key] = np.random.choice(names[key], size=size)

    return df

