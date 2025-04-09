from src.settings import PortfolioSettings
import numpy as np
import yfinance as yf
from scipy.optimize import minimize
from src.strategies.sharpe_ratio import SharpeRatio


class OptimizationPortfolio:
    
    def __init__(self, settings: PortfolioSettings, start_date: str, end_date: str) -> None:
        self.settings = settings
        self.start_date = start_date
        self.end_date = end_date
        self.data = yf.download(self.settings.tickers, start=self.start_date, end=self.end_date)
        self.weights = None
        self.strategy = SharpeRatio(self.settings, self.start_date, self.end_date)

    def compute_negative_sharpe_ratio(self, weights):
        return -self.strategy.compute_metric(weights)

    
    def optimize(self):
        print(f"Optimizing portfolio for {self.settings.tickers}")
        initial_weights = {stock: 1/len(self.settings.tickers) for stock in self.settings.tickers}
        bounds = [(0, 1) for _ in range(len(self.settings.tickers))]
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        result = minimize(self.compute_negative_sharpe_ratio, list(initial_weights.values()), method='SLSQP', bounds=bounds, constraints=constraints)
        self.weights = {stock: result.x[i] for i, stock in enumerate(self.settings.tickers)}
        
        return self.weights

    def get_weights(self):
        if not self.weights:
            self.optimize()
        return self.weights

        
        