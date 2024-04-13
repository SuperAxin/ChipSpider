import datetime
import time
import pandas as pd

from Data_Catch import options_list
from Data_Catch import ChipDataScraper
from Data_Catch import PriceDataScraper


if __name__ == '__main__':
    # 籌碼抓取日期設定
    start_date = datetime.date(2024, 1, 3)
    end_date = datetime.date(2024, 12, 31)
    current_date = start_date
    merged_data = pd.DataFrame()

    while current_date <= end_date:
        #今天日期
        formatted_date = current_date.strftime('%Y-%#m-%#d') # 2022-01-01 > 2022-1-1
        print('今天是' + formatted_date)
        keys_list = [key for key, _ in options_list]
        for SEL_BROKER in keys_list:
            scraper = ChipDataScraper(SEL_BROKER, 'B', formatted_date) # ('8440', ['B', 'C'], 2022-1-1) 第二格中: B 金額單位, E 張數單位
            overbought_data = scraper.get_overbought_data()  # 獲得買超資料
            merged_data = pd.concat([merged_data, overbought_data])
            if not overbought_data.empty:
                print('----------' + SEL_BROKER + '買超----------')
                print(overbought_data)
                print(' ')
            time.sleep(3)
        merged_data = merged_data.groupby('公司名稱').sum() # 同公司資料合併
        merged_data = merged_data.sort_values(by='差額', ascending=False) # 排序多到少
        merged_data.to_csv("Test.csv")
        print("合併之後的數據")
        print(merged_data)
        # 下一天
        time.sleep(10)
        current_date += datetime.timedelta(days=1)


'''USER_ID = ""
PASSWORD = ""
COID = "2330"
START_DATE = "2022-03-24"
END_DATE = "2022-03-30"

Scraper = PriceDataScraper(USER_ID, PASSWORD, COID, START_DATE, END_DATE)
print_df = Scraper.price_catch()
print(print_df)'''





