from dataclasses import dataclass
from typing import Dict
from src.settings import PortfolioSettings
import yfinance as yf


@dataclass
class SimulationPortfolio:
    settings : PortfolioSettings
    start_date : str
    end_date : str
    weights : Dict[str, float]
    

    def get_data(self):
        self.data = yf.download(self.settings.tickers, start=self.start_date, end=self.end_date)
        return self.data

    def compute_expected_returns(self):
        capitals = [self.settings.capital * self.weights[stock] for stock in self.weights]
        returns = [(self.data['Close'][stock].iloc[-1]-self.data['Close'][stock].iloc[0])/self.data['Close'][stock].iloc[0] for stock in self.weights]
        return sum([returns[i] * capitals[i] for i in range(len(self.settings.tickers))])

    