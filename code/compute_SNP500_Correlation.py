import pandas as pd
import datetime
from sklearn.manifold import TSNE
import plotly.express as px

from compute_SNP500_Return import get_SNP500_stock_Return, get_SNP500_list


def compute_SNP500_correlation_matrix(start_return=datetime.datetime(1800, 1, 1)):
    """
    Computes the correlation matrix of daily stock returns for S&P 500 index components.

    Parameters:
    - start_return (datetime.datetime, optional): Start date for computing returns.

    Returns:
    - pandas.DataFrame: Correlation matrix where each entry (i, j) represents the correlation
      between daily returns of stocks with symbols i and j.
    """
    stocks_return = get_SNP500_stock_Return("all_stocks")
    
    stocks_return = stocks_return[stocks_return.columns.drop(list(stocks_return.filter(regex='Log Return')))]

    stocks_return.columns = stocks_return.columns.str.replace(' Return', '')

    stocks_return = stocks_return[stocks_return.index >= start_return]

    SNP500_correlation_matrix = stocks_return.corr()

    SNP500_correlation_matrix.index.name = 'Symbol'

    return SNP500_correlation_matrix


def save_SNP500_correlation_matrix(SNP500_correlation_matrix):
    """
    Saves the S&P 500 correlation matrix to a CSV file.

    Parameters:
    - SNP500_correlation_matrix (pandas.DataFrame): The correlation matrix to be saved.
    """
    SNP500_correlation_matrix.to_csv("C:/Users/loris/Desktop/td/data/SNP500_Correlation/SNP500_Correlation_Matrix.csv")


def get_SNP500_correlation_matrix():
    """
    Reads the S&P 500 correlation matrix from a CSV file.

    Returns:
    - pandas.DataFrame: The correlation matrix with 'Symbol' as the index.
    """
    return pd.read_csv("C:/Users/loris/Desktop/td/data/SNP500_Correlation/SNP500_Correlation_Matrix.csv", index_col='Symbol')


def compute_2D_projection(correlation_matrix):
    """
    Compute a 2D projection of stock.

    Parameters:
    correlation_matrix (pandas.DataFrame): DataFrame representing the stocks correlation matrix.

    Returns:
    pandas.DataFrame: DataFrame containing the 2D projection of stocks based on their correlations.
    """
    tsne = TSNE(verbose=1, perplexity=3, n_iter=3000, early_exaggeration=1, method='exact')
    stocks_vectors = tsne.fit_transform(correlation_matrix)

    stocks_vectors = pd.DataFrame(stocks_vectors, columns=['d1', 'd2'], index=correlation_matrix.index)

    return stocks_vectors


def save_SNP500_stocks_vectors(SNP500_stocks_vectors):
    """
    Saves the provided S&P 500 stocks vectors to a CSV file.

    Parameters:
    - SNP500_stocks_vectors (pandas.DataFrame): The stocks vectors to be saved.
    """
    SNP500_stocks_vectors.to_csv("C:/Users/loris/Desktop/td/data/SNP500_Correlation/SNP500_Stocks_Vectors.csv")

    
def get_SNP500_stocks_vectors():
    """
    Reads the S&P 500 stocks vectors from a CSV file.

    Returns:
    - pandas.DataFrame: The stocks vectors with 'Symbol' as the index.
    """
    return pd.read_csv("C:/Users/loris/Desktop/td/data/SNP500_Correlation/SNP500_Stocks_Vectors.csv", index_col='Symbol')


def add_SNP500_info_and_daily_returns_to_2D_projection(stocks_vectors, start_return=datetime.datetime.now() - datetime.timedelta(days=365)):
    """
    Adds S&P 500 stock information and daily returns to a 2D projection of stock vectors.

    Parameters:
    - stocks_vectors (pandas.DataFrame): 2D projection of stock vectors.
    - start_return (datetime.datetime, optional): Start date for computing returns. Defaults to one year ago.

    Returns:
    - pandas.DataFrame: 2D projection with added columns for stock information (Security, GICS Sector) and daily returns.
    """
    SNP500_list = get_SNP500_list()

    stocks_vect_with_info = stocks_vectors.merge(SNP500_list[['Security', 'GICS Sector']], 'left', left_index=True, right_index=True)

    stocks_return = get_SNP500_stock_Return("all_stocks")
    
    stocks_return = stocks_return[stocks_return.columns.drop(list(stocks_return.filter(regex='Log Return')))]

    stocks_return.columns = stocks_return.columns.str.replace(' Return', '')

    # stocks_return = stocks_return.fillna(0)[stocks_return.index >= start_return]
    stocks_return = stocks_return[stocks_return.index >= start_return]

    stocks_return = stocks_return.stack().reset_index(name='Return').rename(columns={'level_1':'Symbol'}).set_index('Symbol', drop=True)

    stocks_vect_with_ret = stocks_vect_with_info.merge(stocks_return, 'left', left_index=True, right_index=True)

    return stocks_vect_with_ret


def plot_projection_with_daily_return(stocks_vect_with_ret):
    """
    Plots a 2D projection of stock vectors with daily returns as colors.

    Parameters:
    - stocks_vect_with_ret (pandas.DataFrame): DataFrame containing 2D projection data with daily returns.

    Returns:
    - plotly.graph_objects.Figure: Plotly figure displaying the 2D projection.
    """
    return_spec = stocks_vect_with_ret['Return'].dropna().sort_values()
    return_min = return_spec.min()
    return_max = return_spec.max()
    return_neg = return_spec[return_spec<0]
    return_pos = return_spec[return_spec>=0]

    fig = px.scatter(stocks_vect_with_ret,
                     x="d1",
                     y="d2",
                     animation_frame="Date",
                     animation_group="Security",
                     color="Return",
                     color_continuous_scale=[(0,'darkred'),
                                             ((return_neg.quantile(2/3)-return_min)/(return_max-return_min),'darkorange'),
                                             ((return_neg.quantile(8/9)-return_min)/(return_max-return_min),'LightSalmon'),
                                             (-return_min/(return_max-return_min),'grey'),
                                             ((return_pos.quantile(1/9)-return_min)/(return_max-return_min),'GreenYellow'),
                                             ((return_pos.quantile(1/3)-return_min)/(return_max-return_min),'lawngreen'),
                                             (1,'darkgreen')],
                     range_color=[return_spec.iloc[0],return_spec.iloc[-1]],
                     symbol='GICS Sector',
                     symbol_sequence = ['circle', 'square', 'diamond', 'cross', 'x', 'triangle-up', 'triangle-down', 'triangle-left', 'triangle-right', 'triangle-ne', 'triangle-se', 'triangle-sw', 'triangle-nw', 'pentagon', 'hexagon', 'hexagon2', 'octagon', 'star', 'hexagram', 'star-triangle-up', 'star-triangle-down', 'star-square', 'star-diamond', 'diamond-tall', 'diamond-wide', 'hourglass', 'bowtie', 'circle-cross', 'circle-x', 'square-cross', 'square-x', 'diamond-cross', 'diamond-x', 'cross-thin', 'x-thin', 'asterisk', 'hash', 'y-up', 'y-down', 'y-left', 'y-right', 'line-ew', 'line-ns', 'line-ne', 'line-nw', 'arrow-up', 'arrow-down', 'arrow-left', 'arrow-right', 'arrow-bar-up', 'arrow-bar-down', 'arrow-bar-left', 'arrow-bar-right'],
                     hover_name="Security",
                     width=1000, height=1000)

    fig.update_layout(coloraxis_colorbar_x=-0.15,
                      sliders=[dict(active=len(stocks_vect_with_ret['Date'].unique())-1,)])
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    
    return fig


def save_SNP500_projection_plot(fig):
    """
    Saves SNP500 projection plot to an HTML file.

    Parameters:
    - fig (plotly.graph_objects.Figure): The SNP500 projection Plotly figure to be saved.
    """
    fig.write_html("C:/Users/loris/Desktop/td/data/SNP500_Correlation/projection_plot.html")


def get_projection_plot_path():

    return "C:/Users/loris/Desktop/td/data/SNP500_Correlation/projection_plot.html"


def main():
    """
    Orchestrates the main workflow for S&P 500 correlation analysis.

    Steps:
    1. Computes the correlation matrix for S&P 500 stocks.
    2. Saves the correlation matrix to a CSV file.
    3. Computes a 2D projection of the correlation matrix.
    4. Saves the stocks vectors to a CSV file.
    5. Adds S&P 500 stock information and daily returns to the 2D projection.
    6. Plots the 2D projection with daily returns.
    7. Saves the projection plot to an HTML file.
    """
    SNP500_correlation_matrix = compute_SNP500_correlation_matrix()
    save_SNP500_correlation_matrix(SNP500_correlation_matrix)
    SNP500_stocks_vectors = compute_2D_projection(SNP500_correlation_matrix)
    save_SNP500_stocks_vectors(SNP500_stocks_vectors)
    stocks_vect_with_ret = add_SNP500_info_and_daily_returns_to_2D_projection(SNP500_stocks_vectors, start_return=datetime.datetime.now() - datetime.timedelta(days=365))
    fig = plot_projection_with_daily_return(stocks_vect_with_ret)
    save_SNP500_projection_plot(fig)


if __name__ == "__main__":
    main()
