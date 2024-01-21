import requests
import pandas as pd
import yfinance as yf
import datetime
import plotly.graph_objects as go
import plotly.express as px

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

    SNP500_df.sort_values(by='Symbol', inplace=True)

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


def download_stock_OHLCV(symbol):
    """
    Download OHLCV data for a specific stock symbol from Yahoo Finance.

    Parameters:
    symbol (str): Stock symbol for which data is requested.

    Returns:
    pandas.DataFrame: DataFrame containing OHLCV data for the specified stock symbol.
    """
    start = datetime.datetime(2015, 12, 1)

    OHLCV_df = yf.download(tickers=symbol, interval='1d', start=start, progress=False)
    OHLCV_df.sort_values(by='Date', inplace=True)

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


def save_SNP500_stock_OHLCV(OHLCV_df, symbol):
    """
    Save the OHLCV data for a specific stock symbol to a CSV file.

    Parameters:
    OHLCV_df (pandas.DataFrame): DataFrame containing OHLCV data for a stock.
    symbol (str): Stock symbol used as part of the CSV filename.
    """
    OHLCV_df.to_csv("C:/Users/loris/Desktop/td/data/SNP500_OHLCV/"+symbol+".csv")

def get_SNP500_stock_OHLCV(symbol):
    """
    Load the OHLCV data for a specific stock symbol from a CSV file.

    Parameters:
    symbol (str): Stock symbol used to identify the CSV file.

    Returns:
    pandas.DataFrame: DataFrame containing OHLCV data for the specified stock symbol.
    """
    return pd.read_csv("C:/Users/loris/Desktop/td/data/SNP500_OHLCV/"+symbol+".csv", index_col='Date', parse_dates=['Date'])


def save_all_SNP500_prices():
    """
    Execute the function to fetch and save data for all companies in the S&P 500 index.
    """
    delete_files_in_folder("C:/Users/loris/Desktop/td/data/SNP500_OHLCV/")

    all_stocks = pd.DataFrame()

    for symbol in get_SNP500_list().index:

        OHLCV_df = download_stock_OHLCV(symbol.replace(".", "-"))
        print(symbol+" downloaded")
        save_SNP500_stock_OHLCV(OHLCV_df, symbol)

        all_stocks = all_stocks.merge(OHLCV_df.add_prefix(symbol+" "), 'outer', left_index=True, right_index=True)

    save_SNP500_stock_OHLCV(all_stocks, "all_stocks")
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
