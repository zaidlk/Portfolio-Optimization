from src.strategies.sharpe_ratio import SharpeRatio
from src.strategies.strategy import Strategy
from src.settings import PortfolioSettings

class StrategyFactory:
    def get_strategy(self, settings: PortfolioSettings, start_date: str, end_date: str) -> Strategy:
        if settings.strategy_type == "sharpe_ratio":
            return SharpeRatio(settings, start_date, end_date)
        else:
            raise ValueError(f"Unknown strategy type: {settings.strategy_type}")