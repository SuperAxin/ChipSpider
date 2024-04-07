import pandas as pd

class Portfolio:
    def __init__(self):
        # 初始化空的DataFrame
        self.df = pd.DataFrame(columns=['Symbol', 'Name', 'Shares', 'Purchase_Price', 'Purchase_Date', 'Current_Price', 'Total_Value', 'Current_Value', 'Profit'])

    def display_structure(self):
        # 顯示DataFrame結構
        print(self.df)

    def buy(self, symbol, name, shares, purchase_price, purchase_date, current_price):
        # 購買股票
        total_value = shares * purchase_price
        current_value = shares * current_price
        profit = current_value - total_value
        new_row = {'Symbol': symbol, 'Name': name, 'Shares': shares, 'Purchase_Price': purchase_price,
                   'Purchase_Date': purchase_date, 'Current_Price': current_price, 'Total_Value': total_value,
                   'Current_Value': current_value, 'Profit': profit}
        self.df = self.df._append(new_row, ignore_index=True)

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
        self.df.at[idx, 'Shares'] -= shares_to_sell
        self.df.at[idx, 'Total_Value'] = self.df.at[idx, 'Shares'] * self.df.at[idx, 'Purchase_Price']
        self.df.at[idx, 'Current_Value'] = self.df.at[idx, 'Shares'] * current_price
        self.df.at[idx, 'Profit'] = self.df.at[idx, 'Current_Value'] - self.df.at[idx, 'Total_Value']

# 創建Portfolio的實例
portfolio = Portfolio()

# 顯示DataFrame結構
portfolio.display_structure()

# 進行一些購買和出售操作的示例
portfolio.buy('AAPL', 'Apple Inc.', 100, 150.25, '2022-01-01', 175.50)
portfolio.buy('GOOG', 'Alphabet Inc.', 50, 1200.50, '2022-02-15', 1400.75)
portfolio.display_structure()

portfolio.sell('AAPL', 20, 180.75)
portfolio.display_structure()