import requests
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from utilities import delete_files_in_folder


def scrape_SNP500_list():
    """
    Retrieve the list of S&P 500 companies from Wikipedia.

    Returns:
    pandas.DataFrame: DataFrame containing S&P 500 company information.
    """
    URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    html = requests.get(URL).content
    SNP500_df = pd.read_html(html, index_col=0)[0]

    SNP500_df.index = SNP500_df.index.str.replace('\.','-', regex=True)

    SNP500_df.sort_index(inplace=True)

    return SNP500_df


def save_SNP500_list(SNP500_df):
    """
    Save the S&P 500 company list to a CSV file.

    Parameters:
    SNP500_df (pandas.DataFrame): DataFrame containing S&P 500 company information.
    """
    SNP500_df.to_csv("C:/Users/loris/Desktop/td/data/SNP500_List/SNP500_List.csv")


def get_SNP500_list():
    """
    Load the S&P 500 company list from a CSV file.

    Returns:
    pandas.DataFrame: DataFrame containing S&P 500 company information loaded from a CSV file.
    """
    SNP500_df = pd.read_csv("C:/Users/loris/Desktop/td/data/SNP500_List/SNP500_List.csv", index_col='Symbol')

    return SNP500_df


def download_stock_OHLCV(symbol, interval, start):

    OHLCV_df = yf.download(tickers=symbol, interval=interval, start=start, progress=False)
    OHLCV_df.sort_index(inplace=True)

    return OHLCV_df


def plot_OHLC(stock_daily_data, symbol, type="OHLC"):
    """
    Generate a financial chart or line plot for a specific stock symbol.

    Parameters:
    stock_daily_data (pandas.DataFrame): DataFrame containing daily OHLC.
    symbol (str): Stock symbol used as the plot title.
    type (str, default="OHLC"): Specifies the type of plot.
    """
    if type == "OHLC":
        fig = go.FigureWidget(data=go.Ohlc(x=stock_daily_data.index,
                                     open=stock_daily_data['Open'],
                                     high=stock_daily_data['High'],
                                     low=stock_daily_data['Low'],
                                     close=stock_daily_data['Close']))
    else:
        fig = px.line(stock_daily_data, x=stock_daily_data.index, y=stock_daily_data.columns)

    fig.update_layout(title=symbol)
    fig.update_xaxes(
        rangeslider_visible=False,
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
    fig.show()


def save_SNP500_stock_daily_OHLCV(OHLCV_df, symbol):
    
    OHLCV_df.to_csv("C:/Users/loris/Desktop/td/data/SNP500_daily_OHLCV/"+symbol+".csv")

def get_SNP500_stock_daily_OHLCV(symbol):
    
    return pd.read_csv("C:/Users/loris/Desktop/td/data/SNP500_daily_OHLCV/"+symbol+".csv", index_col='Date', parse_dates=['Date'])

def save_SNP500_stock_minuts_OHLCV(OHLCV_df, symbol):
    
    OHLCV_df.to_csv("C:/Users/loris/Desktop/td/data/SNP500_minuts_OHLCV/"+symbol+".csv")

def get_SNP500_stock_minuts_OHLCV(symbol):
    
    return pd.read_csv("C:/Users/loris/Desktop/td/data/SNP500_minuts_OHLCV/"+symbol+".csv", index_col='Datetime', parse_dates=['Datetime'])


def save_all_SNP500_prices():
    """
    Execute the function to fetch and save data for all companies in the S&P 500 index.
    """
    delete_files_in_folder("C:/Users/loris/Desktop/td/data/SNP500_daily_OHLCV/")
    delete_files_in_folder("C:/Users/loris/Desktop/td/data/SNP500_minuts_OHLCV/")

    all_daily_stocks = pd.DataFrame()
    all_minuts_stocks = pd.DataFrame()

    for symbol in get_SNP500_list().index:

        OHLCV_daily = download_stock_OHLCV(symbol, '1d', datetime.now() - relativedelta(years=7))
        OHLCV_minuts = download_stock_OHLCV(symbol, '1m', datetime.now() - timedelta(days=7))

        save_SNP500_stock_daily_OHLCV(OHLCV_daily, symbol)
        save_SNP500_stock_minuts_OHLCV(OHLCV_minuts, symbol)
        print(symbol+" downloaded")

        all_daily_stocks = all_daily_stocks.merge(OHLCV_daily.add_prefix(symbol+" "), 'outer', left_index=True, right_index=True)
        all_minuts_stocks = all_minuts_stocks.merge(OHLCV_minuts.add_prefix(symbol+" "), 'outer', left_index=True, right_index=True)

    save_SNP500_stock_daily_OHLCV(all_daily_stocks, "all_stocks")
    save_SNP500_stock_minuts_OHLCV(all_minuts_stocks, "all_stocks")
    print("All OHLCV downloaded")



def main():
    """
    Perform scraping of the S&P 500 list and save historical market data for all companies in the list.
    """
    SNP500_df = scrape_SNP500_list()
    save_SNP500_list(SNP500_df)
    save_all_SNP500_prices()


if __name__ == "__main__":
    main()
