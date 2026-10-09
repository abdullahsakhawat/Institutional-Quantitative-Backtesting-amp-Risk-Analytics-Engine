# Institutional-Quantitative-Backtesting-amp-Risk-Analytics-Engine
In this programme I will be taking stock market and historic data and applying strategies to that data. Then mathematically calculating whether using the strategy would have resulted in us making money or losing money. I will also factor in the risk taken to get the stated results and all of this data will be presented on an interactive dashboard
## Development Log

**Day 1: Environment Architecture & Data Ingestion Engine**
* `requirements.txt` is used to tell any developers who access my githup repositry which libraries or tools to download to run the project with command `pip install -r requirements.txt` 
* While creating this project, I will source a lot of publicly available data to process. This `.gitignore` file contains code that will ensure the files containing data aren't uploaded to this GitHub repository; this keeps the repository clean and professional. The files are ignored based on file type and location, which includes `.csv` files in the `data/` folder and `.pyc` files throughout the whole program. Finally, `.vscode/` and `.idea/` ignore any non-useful files that are created by the IDE itself.
* Engineered `src/data_loader.py` using object-oriented Python.
* Built `MarketDataLoader` to automatically fetch historical market data via `yfinance`, sanitize missing price gaps, and cache the datasets locally for high-speed retrieval.
* Implemented quantitative transformations, computing time-additive logarithmic returns and a robust technical indicator suite (Moving Averages, RSI, Bollinger Bands).