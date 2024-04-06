import pandas as pd
import requests

from Data_Catch import StockDataScraper
from datetime import date, timedelta
from FinMind.data import DataLoader


class BackTest:
    def __init__(self, TOKEN, COID, START_DATE, END_DATE):
        self.Token = TOKEN
        self.COID = COID
        self.START_DATE = START_DATE
        self.END_DATE = END_DATE
        return None

    def Read_Stock_Index(self):
        Stock_Index = pd.read_csv('Stock_Index.csv', header=None)
        Stock_Index = Stock_Index.set_index(0)
        Stock_Index = Stock_Index.drop(['1101B', '1312A', '1522A', '2002A', '2348A', '2836A', '2838A', '2881A', '2881B', '2881C', '2882A', '2882B', '2883B', '2887E', '2887F', '2887Z1', '2888A', '2888B', '2891B', '2891C', '2897A', '3036A', '3702A', '5871A', '6592A', '8112A', '9941A'])
        Stock_Index = Stock_Index.reset_index()
        return Stock_Index
    def Price_Catch(self, COID, USER_ID, PASSWORD):
        api = DataLoader()
        api.login(user_id=USER_ID, password=PASSWORD)
        data = api.taiwan_stock_daily(
            stock_id=COID,
            start_date="2000-01-01",
            end_date="2020-12-31"
        )
        df = pd.DataFrame(
            data
        )
        print("資料寫入成功")
        return None



