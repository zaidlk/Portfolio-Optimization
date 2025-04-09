import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, timedelta
import yfinance as yf
import traceback

from src.settings import PortfolioSettings
from src.optimization import OptimizationPortfolio
from src.strategy_factory import StrategyFactory

st.set_page_config(
    page_title="Portfolio Optimizer",
    page_icon="💰",
    layout="wide"
)

# App title and description
st.title("Portfolio Optimization App 💰")
st.markdown("""
This app helps you optimize your investment portfolio using the Sharpe ratio.
Enter your portfolio settings, select a date range, and get the optimal asset allocation.
""")

# Sidebar for inputs
st.sidebar.header("Portfolio Settings")

# User inputs
capital = st.sidebar.number_input("Initial Capital ($)", min_value=1000.0, value=10000.0, step=1000.0)

# Default tickers
default_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
ticker_input = st.sidebar.text_area("Stock Tickers (one per line)", "\n".join(default_tickers))
tickers = [ticker.strip() for ticker in ticker_input.split("\n") if ticker.strip()]
print("tickers", tickers)

# Strategy selection
strategy_type = st.sidebar.selectbox(
    "Optimization Strategy",
    ["sharpe_ratio"],
    index=0
)

# Date range selection
st.sidebar.header("Date Range")
end_date = st.sidebar.date_input("End Date", date.today())
start_date = st.sidebar.date_input("Start Date", end_date - timedelta(days=365))

# Format dates for yfinance
start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")

# Run optimization button
if st.sidebar.button("Optimize Portfolio"):
    with st.spinner("Optimizing your portfolio..."):
        try:
            # Create portfolio settings
            print("capital", capital)
            print("tickers", tickers)
            print("strategy_type", strategy_type)
            settings = PortfolioSettings(capital, tickers, strategy_type)
            
            # Run optimization
            optimizer = OptimizationPortfolio(settings, start_date_str, end_date_str)
            weights = optimizer.optimize()
            
            # Display results
            st.header("Optimization Results")
            
            # Create a table of weights
            weights_df = pd.DataFrame({
                'Ticker': list(weights.keys()),
                'Weight (%)': [round(w * 100, 2) for w in weights.values()],
                'Amount ($)': [round(w * capital, 2) for w in weights.values()]
            })
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("Allocation Weights")
                st.dataframe(weights_df)
            
            with col2:
                st.subheader("Portfolio Allocation")
                fig = px.pie(weights_df, values='Weight (%)', names='Ticker', title='Optimal Portfolio Allocation')
                st.plotly_chart(fig)
            
            # Display historical performance
            st.header("Historical Performance")
            
            # Get historical data - handle errors gracefully
            try:
                hist_data = yf.download(tickers, start=start_date_str, end=end_date_str)['Adj Close']
                if hist_data.empty:
                    st.warning("No historical data available from Yahoo Finance. Showing simulated performance instead.")
                    # Create simulated data
                    date_range = pd.date_range(start=start_date, end=end_date, freq='B')
                    hist_data = pd.DataFrame(index=date_range)
                    for ticker in tickers:
                        # Random walk starting at 100
                        returns = np.random.normal(0.0005, 0.01, len(date_range))
                        prices = 100 * np.cumprod(1 + returns)
                        hist_data[ticker] = prices
            except Exception as e:
                st.warning(f"Error fetching historical data: {e}. Showing simulated performance instead.")
                # Create simulated data
                date_range = pd.date_range(start=start_date, end=end_date, freq='B')
                hist_data = pd.DataFrame(index=date_range)
                for ticker in tickers:
                    # Random walk starting at 100
                    returns = np.random.normal(0.0005, 0.01, len(date_range))
                    prices = 100 * np.cumprod(1 + returns)
                    hist_data[ticker] = prices
            
            # Calculate portfolio performance
            weighted_returns = pd.DataFrame()
            for ticker, weight in weights.items():
                if ticker in hist_data.columns:
                    weighted_returns[ticker] = hist_data[ticker] * weight
            
            portfolio_value = weighted_returns.sum(axis=1)
            portfolio_normalized = portfolio_value / portfolio_value.iloc[0]
            
            # Create a DataFrame for plotting
            performance_df = pd.DataFrame({
                'Date': portfolio_normalized.index,
                'Value': portfolio_normalized.values
            })
            
            # Plot portfolio performance
            fig = px.line(performance_df, x='Date', y='Value', title='Normalized Portfolio Performance')
            st.plotly_chart(fig)
            
            # Risk metrics
            returns = portfolio_value.pct_change().dropna()
            annual_return = returns.mean() * 252
            annual_volatility = returns.std() * np.sqrt(252)
            sharpe_ratio = (annual_return - settings.risk_free_rate) / annual_volatility
            
            # Display metrics
            st.header("Risk Metrics")
            metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
            
            metrics_col1.metric("Annual Return", f"{annual_return:.2%}")
            metrics_col2.metric("Annual Volatility", f"{annual_volatility:.2%}")
            metrics_col3.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.code(traceback.format_exc())

# If no optimization has been run yet, show sample visuals
if 'weights' not in locals():
    st.info("👈 Enter your portfolio settings and click 'Optimize Portfolio' to get started.")
    
    # Show some sample data about the stocks
    if tickers:
        try:
            with st.spinner("Loading stock data..."):
                # Try to get sample data, use mock data if API fails
                try:
                    sample_data = yf.download(tickers, start=(date.today() - timedelta(days=30)).strftime("%Y-%m-%d"), end=date.today().strftime("%Y-%m-%d"))['Adj Close']
                    if sample_data.empty:
                        raise ValueError("No data returned from Yahoo Finance")
                except Exception as e:
                    st.warning(f"Could not fetch real stock data: {e}. Showing simulated data instead.")
                    # Create mock data
                    date_range = pd.date_range(start=date.today() - timedelta(days=30), end=date.today(), freq='B')
                    sample_data = pd.DataFrame(index=date_range)
                    for ticker in tickers:
                        # Start with a random price between 50 and 500
                        base_price = np.random.uniform(50, 500)
                        # Generate random daily returns
                        daily_returns = np.random.normal(0.0005, 0.01, len(date_range))
                        # Calculate cumulative returns
                        cum_returns = np.cumprod(1 + daily_returns)
                        # Generate price series
                        sample_data[ticker] = base_price * cum_returns
                
                # Normalize data
                normalized_data = sample_data / sample_data.iloc[0]
                
                # Plot recent performance
                st.header("Recent Stock Performance (30 days)")
                norm_df = normalized_data.reset_index()
                norm_df = pd.melt(norm_df, id_vars=['Date'], value_vars=tickers, var_name='Ticker', value_name='Normalized Price')
                
                fig = px.line(norm_df, x='Date', y='Normalized Price', color='Ticker', title='Normalized Stock Prices (Last 30 Days)')
                st.plotly_chart(fig)
        except Exception as e:
            st.error(f"Couldn't load sample data: {e}")
            st.code(traceback.format_exc())

# Add footer with information
st.markdown("---")
st.markdown("""
### How it works
This app uses Modern Portfolio Theory to find the optimal weights for your portfolio by maximizing the Sharpe ratio.
The Sharpe ratio measures the excess return per unit of risk.

**Formula**: Sharpe Ratio = (Expected Return - Risk-Free Rate) / Portfolio Volatility

**Note**: This app uses simulated data when Yahoo Finance API data is unavailable.

The optimization process finds the weights that give you the highest possible return for a given level of risk.
""")