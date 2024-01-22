import pandas as pd
import numpy as np
import plotly.express as px

from download_SNP500_OHLCV import get_SNP500_stock_daily_OHLCV, get_SNP500_stock_minuts_OHLCV, get_SNP500_list
from utilities import delete_files_in_folder


def compute_return(prices):
    """
    Compute daily returns and log returns from a series of prices.

    Parameters:
    prices (pandas.Series or pandas.DataFrame): Series or DataFrame containing price data.

    Returns:
    pandas.DataFrame: DataFrame containing columns for daily returns and log returns.
    """
    ret = prices.pct_change()
    log_ret = np.log(1 + ret)
    RL_df = pd.DataFrame({'Return' :ret, 'Log Return': log_ret}, index=prices.index)

    return RL_df


def plot_returns(stock_daily_returns, symbol):
    """
    Generate a bar plot displaying daily returns for a specific stock symbol.

    Parameters:
    stock_daily_returns (pandas.DataFrame): DataFrame containing daily returns for the stock symbol.
    symbol (str): Stock symbol used as the plot title.
    """
    fig = px.bar(stock_daily_returns,
                 x=stock_daily_returns.index,
                 y=stock_daily_returns.columns,
                 barmode="group",
                 title=symbol)    

    fig.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    fig.update_traces(visible="legendonly")
    fig.data[0].visible=True
    
    fig.show()


def save_SNP500_stock_daily_Return(ret_df, symbol):
    
    ret_df.to_csv("C:/Users/loris/Desktop/td/data/SNP500_daily_Return/"+symbol+".csv")

def get_SNP500_stock_daily_Return(symbol):
    
    return pd.read_csv("C:/Users/loris/Desktop/td/data/SNP500_daily_Return/"+symbol+".csv", index_col='Date', parse_dates=['Date'])

def save_SNP500_stock_minuts_Return(ret_df, symbol):
    
    ret_df.to_csv("C:/Users/loris/Desktop/td/data/SNP500_minuts_Return/"+symbol+".csv")

def get_SNP500_stock_minuts_Return(symbol):
    
    return pd.read_csv("C:/Users/loris/Desktop/td/data/SNP500_minuts_Return/"+symbol+".csv", index_col='Datetime', parse_dates=['Datetime'])


def save_all_SNP500_returns():
    """
    Computation and saving of returns for all stocks listed in the S&P 500 index.
    """
    delete_files_in_folder("C:/Users/loris/Desktop/td/data/SNP500_daily_Return/")
    delete_files_in_folder("C:/Users/loris/Desktop/td/data/SNP500_minuts_Return/")

    all_daily_stocks = pd.DataFrame()
    all_minuts_stocks = pd.DataFrame()

    for symbol in get_SNP500_list().index:

        daily_close_values = get_SNP500_stock_daily_OHLCV(symbol)['Close']
        minuts_close_values = get_SNP500_stock_minuts_OHLCV(symbol)['Close']

        return_daily = compute_return(daily_close_values)
        return_minuts = compute_return(minuts_close_values)

        
        save_SNP500_stock_daily_Return(return_daily, symbol)
        save_SNP500_stock_minuts_Return(return_minuts, symbol)

        print(symbol+" return computed")

        all_daily_stocks = all_daily_stocks.merge(return_daily.add_prefix(symbol+" "), 'outer', left_index=True, right_index=True)
        all_minuts_stocks = all_minuts_stocks.merge(return_minuts.add_prefix(symbol+" "), 'outer', left_index=True, right_index=True)

    save_SNP500_stock_daily_Return(all_daily_stocks, "all_stocks")
    save_SNP500_stock_minuts_Return(all_minuts_stocks, "all_stocks")
    print("All returns computed")


def main():
    """
    Computation and saving of returns for all stocks listed in the S&P 500 index.
    """
    save_all_SNP500_returns()


if __name__ == "__main__":
    main()
