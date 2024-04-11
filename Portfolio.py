import os
import pandas as pd

class Portfolio:
    def __init__(self,capital):
        # 初始化表格
        self.df = pd.DataFrame(columns=['Symbol', 'Name', 'Shares', 'Purchase_Price', 'Purchase_Date', 'Current_Price', 'Total_Value', 'Current_Value', 'Profit'])
        self.capital = capital

    def display_structure(self):
        # 顯示DataFrame結構
        print(self.df)
        print(self.capital)

    def price_scraper(self, DATE, COID, TYPE): #　('2000-03-27', '1101', [_open,_max,_min,_close])
        os.chdir('Price_Data') # 切換至 price_data 資料夾
        df = pd.read_csv( COID + '.csv')
        price = df.loc[df['date'] == DATE, TYPE].values[0]
        os.chdir(os.pardir)
        return price
    def update_current_price(self, now_date):
        # 更新current_price
        print(None)

    def buy(self, symbol, name, shares, purchase_price, purchase_date, current_price):
        # 購買股票
        total_value = shares * purchase_price
        if self.capital >= total_value: # 餘額足夠才能買
            print("{} 目前價格{} 購買 {}股 花費{}元".format(name, current_price, shares, total_value))
            current_value = shares * current_price
            profit = round((current_value - total_value) / total_value, 2)
            new_row = {'Symbol': symbol, 'Name': name, 'Shares': shares, 'Purchase_Price': purchase_price,
                       'Purchase_Date': purchase_date, 'Current_Price': current_price, 'Total_Value': total_value,
                       'Current_Value': current_value, 'Profit': profit}
            self.df = self.df._append(new_row, ignore_index=True)
            self.capital = self.capital - total_value
        else:
            print("餘額不足")

    def sell(self, symbol, shares_to_sell, current_price):
        # 出售股票
        idx = self.df.index[self.df['Symbol'] == symbol].tolist()
        if not idx:
            print("Stock symbol not found in portfolio.")
            return
        idx = idx[0]
        if shares_to_sell > self.df.at[idx, 'Shares']:
            print("Not enough shares to sell.")
            return
        current_value = shares_to_sell * current_price
        print("售出 {} {}股 賣出價格為{} 獲利{}".format(symbol, current_price, shares_to_sell, current_value))
        self.df.at[idx, 'Shares'] -= shares_to_sell
        self.df.at[idx, 'Total_Value'] = self.df.at[idx, 'Shares'] * self.df.at[idx, 'Purchase_Price']
        self.df.at[idx, 'Current_Value'] = self.df.at[idx, 'Shares'] * current_price
        self.df.at[idx, 'Profit'] = self.df.at[idx, 'Current_Value'] - self.df.at[idx, 'Total_Value']
        self.capital = self.capital + current_value

        # Shares為0則從組合中替除
        if self.df.at[idx, 'Shares'] == 0:
            self.df.drop(idx, inplace=True)



'''# Portfolio example
capital = 1000000
portfolio = Portfolio(capital)

# 價格抓取
price = portfolio.price_scraper('2000-03-27', '1101', 'open')
print(price)

# 買入 symbol, name, shares, purchase_price, purchase_date, current_price
portfolio.buy('AAPL', 'Apple Inc.', 100, 150.25, '2022-01-01', 151.50)
portfolio.buy('GOOG', 'Alphabet Inc.', 50, 1200.50, '2022-02-15', 1400.75)
portfolio.display_structure()

# 賣出 symbol, shares_to_sell, current_price
portfolio.sell('GOOG', 50, 180.75)
portfolio.display_structure()'''
