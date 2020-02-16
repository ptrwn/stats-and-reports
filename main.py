import stats
import click
import drawer
from openpyxl import Workbook

@click.command()
@click.option('--begp',
              type=click.DateTime(formats=["%Y-%m-%d %H:%M:%S"]),
              prompt='Enter start datetime of reporting period',
              help='The datetime must be in YYYY-MM-DD HH:MM:SS format.')
@click.option('--endp',
              type=click.DateTime(formats=["%Y-%m-%d %H:%M:%S"]),
              prompt='Enter end datetime of reporting period',
              help='The datetime must be in YYYY-MM-DD HH:MM:SS format.')
def boo(begp, endp):
    """Such docstring wow"""

    df = stats.get_df()
    df_per = stats.get_df_period(df, begp, endp)
    cust_dict = stats.get_list_of_customers(df_per)

    print('There is feedback from the following customers within the selected period:')
    for i in cust_dict:
        print(i, cust_dict[i])

    wb_name = "csat_stat.xlsx"
    wb = Workbook()
    wb.save(filename=wb_name)

    stayin = True
    while stayin:
        print('Enter customer numbers separated by comma, or all for all')
        x = input()
        if x.lower() == 'all':
            cust_names_l = list(cust_dict.values())
            d_cust = stats.get_cust(df_per, *cust_names_l)
            stat = stats.stat_counter(d_cust)
            dis_reas = stats.get_dsat_reason(d_cust)

            wb_name = "csat_stat.xlsx"
            wb = Workbook()
            wb.save(filename=wb_name)

            drawer.draw_csat_doughnut(wb_name, **stat)
            drawer.draw_dsat_reason_bars(wb_name, dis_reas)

            print(stat)
            break
        else:
            cust_l = []
            cust_names_l = []
            err_l = []
            x = x.replace(' ', '')
            for i in x.split(','):
                try:
                    i = int(i)
                except:
                    err_l.append(i)
                    continue

                if i in list(cust_dict.keys()):
                    cust_l.append(i)
                    cust_names_l.append(cust_dict[i])
                else:
                    err_l.append(i)
                    continue

        if err_l: print('these values were not in customer list, omitting them:', err_l)
        if not cust_l:
            print('no one home')
        else:
            print('got these customers:')
            for i in cust_l:
                print(cust_dict[i])

            d_cust = stats.get_cust(df_per, *cust_names_l)
            stat = stats.stat_counter(d_cust)
            print(stat)

        stayin = False



if __name__ == '__main__':
    boo()