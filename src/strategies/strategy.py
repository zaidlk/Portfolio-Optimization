from abc import abstractmethod
from src.settings import PortfolioSettings
from typing import List

class Strategy:
    def __init__(self, settings: PortfolioSettings, start_date: str, end_date: str) -> None:
        self.settings = settings
        self.start_date = start_date
        self.end_date = end_date

    @abstractmethod
    def compute_metric(self, weights: List[float]):
        pass
        
    
    