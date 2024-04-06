import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

class StockDataScraper:
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

    def extract_table_data(self, table_index):
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

# Example usage:
'''url = 'https://fubon-ebrokerdj.fbs.com.tw/z/zg/zgb/zgb0.djhtm?a=8440&b=8440&c=B&e=2024-3-12&f=2024-3-12'
scraper = StockDataScraper(url)
overbought_data = scraper.get_overbought_data()
oversell_data = scraper.get_oversell_data()

print(overbought_data)
print(oversell_data)'''