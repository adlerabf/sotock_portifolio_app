def calculate_portfolio_performance(data, weights):
    """
    Calculates daily and cumulative returns of a portfolio based on asset weights.

    Parameters:
    - data (pd.DataFrame): Adjusted close prices with tickers as columns and date as index.
    - weights (list of floats): Portfolio weights for each ticker in the same order as columns in 'data'.

    Returns:
    - daily_returns (pd.Series): Daily returns of the portfolio.
    - cumulative_returns (pd.Series): Cumulative returns of the portfolio.
    """
    # Calculate daily percentage change
    daily_returns = data.pct_change().dropna()

    # Calculate weighted daily return
    portfolio_returns = (daily_returns * weights).sum(axis=1)

    # Calculate cumulative return in percentage
    cumulative_returns = (1 + portfolio_returns).cumprod() - 1

    return portfolio_returns, cumulative_returns