import os
from typing import List, Optional
import numpy as np
import pandas as pd
import yfinance as yf


class MarketDataLoader:
    """Fetches historical financial data from Yahoo Finance with automated disk caching

    and return sanitization.
    """

    def __init__(self, cache_dir: str = "data"):
        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def fetch_data(
        self,
        ticker: str,
        start_date: str,
        end_date: str,
        use_cache: bool = True,
    ) -> pd.DataFrame:
        """Retrieves price data from local cache if present; otherwise downloads from yfinance."""
        sanitized_ticker = ticker.replace("^", "").replace(".", "_")
        cache_path = os.path.join(
            self.cache_dir, f"{sanitized_ticker}_{start_date}_{end_date}.csv"
        )

        if use_cache and os.path.exists(cache_path):
            print(f"[CACHE HIT] Loading {ticker} from {cache_path}")
            df = pd.read_csv(cache_path, index_col=0, parse_dates=True)
            return df

        print(
            f"[API CALL] Downloading {ticker} from Yahoo Finance ({start_date} to {end_date})..."
        )
        data = yf.download(
            ticker, start=start_date, end=end_date, progress=False
        )

        if data.empty:
            raise ValueError(
                f"No data returned for ticker '{ticker}'. Verify the symbol and dates."
            )

        # Flatten multi-index columns returned by modern yfinance versions
        if isinstance(data.columns, pd.MultiIndex):
            data = data.xs(key=ticker, axis=1, level=1)

        df = self._clean_and_preprocess(data)
        df.to_csv(cache_path)
        print(f"[CACHE STORED] Saved dataset to {cache_path}")
        return df

    def _clean_and_preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handles missing price entries and calculates daily percentage and log returns."""
        df = df.copy()

        # Forward fill weekends/holidays, then backfill any opening edge-cases
        df = df.ffill().bfill()

        price_col = "Adj Close" if "Adj Close" in df.columns else "Close"

        # Simple percentage return: (P_t - P_{t-1}) / P_{t-1}
        df["Simple_Return"] = df[price_col].pct_change()

        # Logarithmic return: ln(P_t / P_{t-1}) -> Time-additive across periods
        df["Log_Return"] = np.log(df[price_col] / df[price_col].shift(1))

        # 20-day rolling annualized standard deviation (assuming 252 market days/year)
        df["Rolling_Vol_20D"] = (
            df["Simple_Return"].rolling(window=20).std() * np.sqrt(252)
        )

        return df


class TechnicalIndicators:
    """Calculates quantitative momentum, volatility, and trend indicators."""

    @staticmethod
    def add_moving_averages(
        df: pd.DataFrame, windows: List[int] = [20, 50, 200]
    ) -> pd.DataFrame:
        df = df.copy()
        price_col = "Adj Close" if "Adj Close" in df.columns else "Close"
        for w in windows:
            df[f"SMA_{w}"] = df[price_col].rolling(window=w).mean()
            df[f"EMA_{w}"] = df[price_col].ewm(span=w, adjust=False).mean()
        return df

    @staticmethod
    def add_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        df = df.copy()
        price_col = "Adj Close" if "Adj Close" in df.columns else "Close"
        delta = df[price_col].diff()

        gain = delta.where(delta > 0, 0).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / (loss + 1e-9)  # Avoid division by zero
        df[f"RSI_{period}"] = 100 - (100 / (1 + rs))
        return df

    @staticmethod
    def add_bollinger_bands(
        df: pd.DataFrame, window: int = 20, num_std: float = 2.0
    ) -> pd.DataFrame:
        df = df.copy()
        price_col = "Adj Close" if "Adj Close" in df.columns else "Close"
        df["BB_Middle"] = df[price_col].rolling(window=window).mean()
        std = df[price_col].rolling(window=window).std()

        df["BB_Upper"] = df["BB_Middle"] + (num_std * std)
        df["BB_Lower"] = df["BB_Middle"] - (num_std * std)
        df["BB_Bandwidth"] = (df["BB_Upper"] - df["BB_Lower"]) / df["BB_Middle"]
        return df

    @classmethod
    def add_all_indicators(cls, df: pd.DataFrame) -> pd.DataFrame:
        df = cls.add_moving_averages(df)
        df = cls.add_rsi(df)
        df = cls.add_bollinger_bands(df)
        return df.dropna()


if __name__ == "__main__":
    loader = MarketDataLoader()
    # Test on Barclays PLC (London Stock Exchange)
    test_ticker = "BARC.L"
    raw_data = loader.fetch_data(
        test_ticker, start_date="2022-01-01", end_date="2025-12-31"
    )
    processed_data = TechnicalIndicators.add_all_indicators(raw_data)

    print("\n" + "=" * 55)
    print(f"Engine Test Successful: {test_ticker}")
    print(f"Data Points: {len(processed_data)} days")
    print(
        f"Generated Columns: {list(processed_data.columns[-6:])}"
    )  # Show newest indicator columns
    print("=" * 55)