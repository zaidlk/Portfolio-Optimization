# Portfolio Optimization App

This application helps you optimize your investment portfolio using the Sharpe ratio, following Modern Portfolio Theory principles.

## Features

- **Portfolio Optimization**: Uses Sharpe ratio to determine optimal asset allocation
- **Interactive Dashboard**: Built with Streamlit for easy visualization and interaction
- **Risk Analysis**: Displays annual return, volatility, and Sharpe ratio
- **Historical Performance**: Shows how your optimized portfolio would have performed
- **Fallback Mechanisms**: Uses simulated data when real market data isn't available

## Installation

```bash
# Clone the repository
git clone git@github.com:zaidlk/Portfolio-Optimization.git
cd Finance

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

The app will be available at http://localhost:8501

## Project Structure

- `app.py`: Main Streamlit application
- `src/`: Core functionality
  - `settings.py`: Portfolio settings
  - `optimization.py`: Portfolio optimization algorithms
  - `strategies/`: Strategy implementations
    - `strategy.py`: Base strategy class
    - `sharpe_ratio.py`: Sharpe ratio implementation
  - `strategy_factory.py`: Factory for creating strategies
- `requirements.txt`: Project dependencies

## License

MIT
