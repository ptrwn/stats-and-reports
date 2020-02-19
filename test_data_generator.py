# generates a test file similar to export from Freshdesk

import pandas as pd
import numpy as np

def random_timestamp(start, end):
    startp = pd.Timestamp(start)
    endp = pd.Timestamp(end)
    dts = (endp - startp).total_seconds()
    return startp + pd.Timedelta(np.random.uniform(0, dts), 's')


def make_test_df(sd_size):

    sz = sd_size

    lipsum = 'Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua Ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur Excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum'
    c_names = lipsum.split(' ')
    dsat_reasons = ['resolution delay', 'resolution quality', 'follow-up adherence', 'product bug', 'product usability',
                    'support resources', 'other', 'unmanaged expectations', 'Mixed feedback', 'Duplicate']

    df = pd.DataFrame(columns=['Survey Received Time', 'Ticket Id', 'Rating', 'Comment', 'Company',
       'Group', 'Agent', 'Primary reason', 'Secondary reason', 'Action',
       'Comment DSAT analysis'])

    df['Ticket Id'] = np.random.randint(200, 9000, size=sz)
    df['Rating'] = np.random.choice(['VSAT', 'SAT', 'VDSAT', 'Neutral', 'DSAT'], size=sz)

    for item in df.index:
        df.at[item, 'Survey Received Time'] = random_timestamp('2019-07-01 00:00:00', '2019-07-31 23:59:59')

    df['Primary reason'] = np.random.choice(dsat_reasons, size=sz)
    df['Company'] = np.random.choice(c_names, size=sz)
    df['Group'] = np.random.choice(['A', 'B', 'C', 'D'], size=sz)

    return df


