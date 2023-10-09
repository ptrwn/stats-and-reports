from click.testing import CliRunner
from unittest import mock 
import datetime
from main import main


@mock.patch('main.make_sample_df')
def test_empty_console_input_defaults(mock_sample_df):
    runner = CliRunner()
    runner.invoke(main, input="")
    mock_sample_df.assert_called_with(datetime.datetime(2019, 7, 1, 0, 0), datetime.datetime(2019, 7, 31, 23, 59, 59), 100)


@mock.patch('main.make_sample_df')
def test_console_input(mock_sample_df):
    runner = CliRunner()
    l_par = ["--startp", "2019-07-01 00:00:00", "--endp", "2019-07-21 00:00:00", "--num", "500", "--file_name", "res_report"]
    runner.invoke(main, args=l_par)
    mock_sample_df.assert_called_with(datetime.datetime(2019, 7, 1, 0, 0), datetime.datetime(2019, 7, 21, 0, 0), 500)








