import click
from openpyxl import Workbook
import data.drawer as drawer
import data.stats as stats
from data.data_generator import make_sample_df


@click.command()
@click.option('--startp', '--start_of_reporting_period',
              prompt='Enter start datetime of reporting period',
              default='2019-07-01 00:00:00',
              type=click.DateTime(formats=["%Y-%m-%d %H:%M:%S"]),
              show_default=True,
              help='The datetime must be in YYYY-MM-DD HH:MM:SS format')
@click.option('--endp', '--end_of_reporting_period',
              prompt='Enter end datetime of reporting period',
              default='2019-07-31 23:59:59',
              type=click.DateTime(formats=["%Y-%m-%d %H:%M:%S"]),
              show_default=True,
              help='The datetime must be in YYYY-MM-DD HH:MM:SS format.')
@click.option('--num',
              prompt='Enter number of tickets in report',
              default=100,
              show_default=True)
@click.option('--file_name',
              prompt='Enter the name of the resulting file',
              default='csat_stat',
              show_default=True)
def main(startp: click.DateTime, endp: click.DateTime, num: int, file_name: str) -> None:
    
    if not file_name.endswith('.xlsx'):
        file_name+='.xlsx'

    df = make_sample_df(startp, endp, num)
    stat = stats.stat_counter(df)
    dis_reas = stats.get_dsat_reasons(df)
   
    wb = Workbook()
    wb = drawer.draw_csat_doughnut(wb, **stat)
    wb = drawer.draw_dsat_reason_bars(wb, dis_reas)
    del wb['Sheet'] # remove the default empty first sheet

    wb.save(filename=file_name)


if __name__ == '__main__':
    main()




