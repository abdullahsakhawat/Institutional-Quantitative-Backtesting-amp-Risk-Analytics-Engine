# Institutional-Quantitative-Backtesting-amp-Risk-Analytics-Engine
In this programme I will be taking stock market and historic data and applying strategies to that data. Then mathematically calculating whether using the strategy would have resulted in us making money or losing money. I will also factor in the risk taken to get the stated results and all of this data will be presented on an interactive dashboard
## Development Log

**Day 1: Environment Architecture & Data Ingestion Engine**
* Configured local workspace and locked environment dependencies (`requirements.txt`).
* Implemented `.gitignore` to prevent massive CSV data caches from bloating the production repository.
* Engineered `src/data_loader.py` using object-oriented Python.
* Built `MarketDataLoader` to automatically fetch historical market data via `yfinance`, sanitize missing price gaps, and cache the datasets locally for high-speed retrieval.
* Implemented quantitative transformations, computing time-additive logarithmic returns and a robust technical indicator suite (Moving Averages, RSI, Bollinger Bands).