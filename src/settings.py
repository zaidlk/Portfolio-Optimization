from dataclasses import dataclass
import numpy as np
import pandas as pd
import yfinance as yf



class PortfolioSettings:

    def __init__(self, capital: float, tickers: list[str], strategy_type: str):
        self.capital = capital
        self.tickers = tickers
        
        # Try to get risk-free rate from Yahoo Finance, use default if it fails
        try:
            tnx_data = yf.download("^IRX", period="1d")
            if not tnx_data.empty:
                self.risk_free_rate = tnx_data.iloc[-1]["Close"] / 100
                print("risk free rate :", self.risk_free_rate)
            else:
                self.risk_free_rate = 0.045  # 4.5% as default
        except Exception as e:
            print(f"Could not retrieve risk-free rate: {e}")
            self.risk_free_rate = 0.045  # 4.5% as default
        print("risk free rate :", self.risk_free_rate)
        self.strategy_type = strategy_type
    

    
    
    


    
