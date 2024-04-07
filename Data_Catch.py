import requests
import re
import pandas as pd

from bs4 import BeautifulSoup
from FinMind.data import DataLoader

class ChipDataScraper:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
        }

    def fetch_data(self):
        response = requests.get(self.url, headers=self.headers)
        response.encoding = 'big5'
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def extract_table_data(self, table_index): # table_index[買超:3, 賣超:4]
        soup = self.fetch_data()
        table = soup.find_all('table')[table_index].find_all('tr')[2:]
        extracted_data = []

        for tr in table:
            data = []
            for td in tr:
                if str(td).isspace() == False:
                    pattern_com = r'(?:Link2Stk\(\'([\w\d]+)\'\);|GenLink2stk\(\'.*?\',\'(.*?)\'\);|>(-?\d{1,3}(?:,\d{3})*(?:\.\d+)?)<\/td>)'
                    matche_com = re.findall(pattern_com, str(td))
                    for match in matche_com:
                        result = [group for group in match if group]
                        if result:
                            data.append(result[0])
            extracted_data.append(data)

        # Convert extracted data to DataFrame
        df = pd.DataFrame(extracted_data)

        # Set column headers
        df.columns = ['公司名稱', '買入', '賣出', '差額']

        return df

    def get_overbought_data(self):
        return self.extract_table_data(3)

    def get_oversell_data(self):
        return self.extract_table_data(4)

class PriceDataScraper:
    def __init__(self, USER_ID, PASSWORD, COID, START_DATE, END_DATE):
        self.USER_ID = USER_ID
        self.PASSWORD = PASSWORD
        self.COID = COID
        self.START_DATE = START_DATE
        self.END_DATE = END_DATE
        return None

    def __read_stock_index(self):
        Stock_Index = pd.read_csv('Stock_Index.csv', header=None)
        Stock_Index = Stock_Index.set_index(0)
        Stock_Index = Stock_Index.drop(['1101B', '1312A', '1522A', '2002A', '2348A', '2836A', '2838A', '2881A', '2881B', '2881C', '2882A', '2882B', '2883B', '2887E', '2887F', '2887Z1', '2888A', '2888B', '2891B', '2891C', '2897A', '3036A', '3702A', '5871A', '6592A', '8112A', '9941A'])
        Stock_Index = Stock_Index.reset_index()
        return Stock_Index
    def price_catch(self):
        api = DataLoader() # 一般帳戶api請求上限為600
        api.login(user_id=self.USER_ID, password=self.PASSWORD)
        data = api.taiwan_stock_daily(
            stock_id=self.COID,
            start_date=self.START_DATE,
            end_date=self.END_DATE
        )
        df = pd.DataFrame(
            data
        )

        return df



# Example usage:
'''url = 'https://fubon-ebrokerdj.fbs.com.tw/z/zg/zgb/zgb0.djhtm?a=8440&b=8440&c=B&e=2024-3-12&f=2024-3-12'
scraper = StockDataScraper(url)
overbought_data = scraper.get_overbought_data()
oversell_data = scraper.get_oversell_data()

print(overbought_data)
print(oversell_data)'''