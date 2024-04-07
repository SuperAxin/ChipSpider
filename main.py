from Data_Catch import ChipDataScraper
from Data_Catch import PriceDataScraper

'''# Example usage:
url = 'https://fubon-ebrokerdj.fbs.com.tw/z/zg/zgb/zgb0.djhtm'
# 定義變數, 列表點選
params = {
    'a': '8440', # 券商代號
    'b': '8440', # 券商分點, 無分點則與a相同
    'c': 'B', # B 金額單位, E 張數單位
    'e': '2024-3-12', # 起始日期
    'f': '2024-3-12'  # 結束日期
}

# 將參數加入 URL
url= url + '?' + '&'.join([f'{key}={value}' for key, value in params.items()])
print(url)
scraper = ChipDataScraper(url)
overbought_data = scraper.get_overbought_data() # 買超資料
oversell_data = scraper.get_oversell_data() # 賣超資料

print('----------買超----------')
print(overbought_data[:5])
print(' ')
print('----------賣超----------')
print(oversell_data[:5])'''

'''USER_ID = ""
PASSWORD = ""
COID = "2330"
START_DATE = "2022-03-24"
END_DATE = "2022-03-30"

Scraper = PriceDataScraper(USER_ID, PASSWORD, COID, START_DATE, END_DATE)
print_df = Scraper.price_catch()
print(print_df)'''





'''
options_list = [
    ("8890", "大和國泰"),
    ("9800", "元大"),
    ("8150", "台新"),
    ("1470", "台灣摩根士丹利"),
    ("9A00", "永豐金"),
    ("7000", "兆豐"),
    ("1020", "合庫"),
    ("5260", "美好"),
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
]
'''