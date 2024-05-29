import requests
import re
import pandas as pd
import os

from bs4 import BeautifulSoup
from FinMind.data import DataLoader


options_list = [
    ("8890", "大和國泰"),
    ("9800", "元大"),
    ("8150", "台新"),
    ("1470", "台灣摩根士丹利"),
    ("9A00", "永豐金"),
    ("7000", "兆豐"),
    ("1020", "合庫"),

]
'''("5260", "美好"),
    ("1440", "美林"),
    ("1480", "美商高盛"),
    ("8960", "香港上海匯豐"),
    ("8880", "國泰"),
    ("5380", "第一金"),
    ("5850", "統一"),
    ("9200", "凱基"),
    ("9600", "富邦"),
    ("1650", "新加坡商瑞銀"),
    ("8440", "摩根大通"),
]'''


class ChipDataScraper:
    def __init__(self, SEL_BROKER, TYPE, DATE):
        url = 'https://fubon-ebrokerdj.fbs.com.tw/z/zg/zgb/zgb0.djhtm'
        # 定義變數, 列表點選
        params = {
            'a': SEL_BROKER,  # 券商代號
            'b': SEL_BROKER,  # 券商分點, 無分點則與a相同
            'c': TYPE,  # B 金額單位, E 張數單位
            'e': DATE,  # 起始日期
            'f': DATE  # 結束日期
        }
        # 將參數加入 URL
        url = url + '?' + '&'.join([f'{key}={value}' for key, value in params.items()])
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
        df = None
        try:
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

            df[['買入', '賣出', '差額']] = df[['買入', '賣出', '差額']].apply(lambda x: x.str.replace(',', '').astype(int))
        except:
            print("本日無開盤")
        return df

    def get_overbought_data(self):
        return self.extract_table_data(3)

    def get_oversell_data(self):
        return self.extract_table_data(4)

class PriceDataScraper: # 直接在本地建立資料庫, 再調用價格資料
    def __init__(self, USER_ID, PASSWORD, START_DATE, END_DATE):
        self.USER_ID = USER_ID
        self.PASSWORD = PASSWORD
        self.START_DATE = START_DATE
        self.END_DATE = END_DATE
        return None

    def read_stock_index(self):
        Stock_Index = pd.read_csv('Stock_Index.csv', header=None)
        Stock_Index = Stock_Index.set_index(0)
        Stock_Index = Stock_Index.drop(['1101B', '1312A', '1522A', '2002A', '2348A', '2836A', '2838A', '2881A', '2881B', '2881C', '2882A', '2882B', '2883B', '2887E', '2887F', '2887Z1', '2888A', '2888B', '2891B', '2891C', '2897A', '3036A', '3702A', '5871A', '6592A', '8112A', '9941A'])
        Stock_Index = Stock_Index.reset_index()
        return Stock_Index

    def create_folder(self): #　檢查 Price_Data 資料夾是否已建立
        current_directory = os.getcwd()
        folder_name = "Price_Data"
        folder_path = os.path.join(current_directory, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder '{folder_path}' created.")
        else:
            print(f"Folder '{folder_path}' already exists.")
        os.chdir('Price_Data')
        current_directory = os.getcwd()
        print("Current working directory:", current_directory)
        return None

    def price_catch(self):
        _ = self.create_folder()
        CO_TABLE = self.read_stock_index()
        os.chdir('Price_Data')  # 進入 Price_Data Folder
        api = DataLoader()  # 一般帳戶api請求上限為600
        api.login(user_id=self.USER_ID, password=self.PASSWORD)
        for COID in CO_TABLE[0]:
            if not os.path.exists(COID + '.csv'):
                print(COID)
                data = api.taiwan_stock_daily(
                    stock_id=COID,
                    start_date=self.START_DATE,
                    end_date=self.END_DATE
                )
                df = pd.DataFrame(
                    data
                )
                df.to_csv(COID + '.csv')
            else:
                print(COID + "已存在")
        os.chdir(os.pardir) # 返回上一層資料夾
        return None

class Market_Value:
    def __init__(self, COID):
        self.url = 'https://fubon-ebrokerdj.fbs.com.tw/Z/ZC/ZCX/ZCXFUBON_{}.djhtm'.format(COID)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
        }

    def fetch_data(self):
        # print(self.url)
        response = requests.get(self.url, headers=self.headers)
        response.encoding = 'big5'
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def value(self):
        soup = self.fetch_data()
        # print(soup)
        table = soup.find_all('table')[1].find_all('tr')[8]
        value = table.find_all('td')[4].text
        value = (int(value.replace(',', '')) * 1000000 ) / 100000000 #　轉換成億
        return value

class Financial_Institutions_Scraper: # 投信買超
    def __init__(self, date):
        self.url = "https://www.twse.com.tw/rwd/zh/fund/TWT44U?date={}&response=json&_=1713172650296".format(date) # 20240321

    def get(self):
        response = requests.get(self.url)
        date = response.json()
        # print(date['data']) # 1 "證券代號" 2 "證券名稱" 3 "買進股數" 4 "賣出股數" 5 "買賣超股數"
        return date['data']

'''
Spyder = Financial_Institutions_Scraper('20240318')
data = Spyder.get()
for i in data:
    print(i)
'''

'''
USER_ID = -
PASSWORD = -
COID = "2330"
START_DATE = "2000-03-24"
END_DATE = "2024-03-29"

Scraper = PriceDataScraper(USER_ID, PASSWORD, START_DATE, END_DATE)
folder = Scraper.create_folder()
folder = Scraper.price_catch()
'''



# Example usage:
'''url = 'https://fubon-ebrokerdj.fbs.com.tw/z/zg/zgb/zgb0.djhtm?a=8440&b=8440&c=B&e=2024-3-12&f=2024-3-12'
scraper = StockDataScraper(url)
overbought_data = scraper.get_overbought_data()
oversell_data = scraper.get_oversell_data()

print(overbought_data)
print(oversell_data)'''