import datetime
import time
import pandas as pd
from Data_Catch import options_list
from Data_Catch import ChipDataScraper
from Data_Catch import PriceDataScraper


if __name__ == '__main__':
    # Example usage:
    start_date = datetime.date(2022, 1, 3)
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
            merged_data = pd.concat([merged_data, overbought_data[0:6]])
            if not overbought_data.empty:
                print('----------' + SEL_BROKER + '買超----------')
                #print(overbought_data[:5])
                #print(' ')
            time.sleep(3)
        merged_data.to_csv("Test.csv")
        print("合併之後的數據")
        print(merged_data)
        # 下一天
        time.sleep(5)
        current_date += datetime.timedelta(days=1)


'''USER_ID = ""
PASSWORD = ""
COID = "2330"
START_DATE = "2022-03-24"
END_DATE = "2022-03-30"

Scraper = PriceDataScraper(USER_ID, PASSWORD, COID, START_DATE, END_DATE)
print_df = Scraper.price_catch()
print(print_df)'''





