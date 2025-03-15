# arbitrage_detector.py

import pandas as pd
import yfinance as yf
from typing import List, Dict, Tuple

def fetch_exchange_data(ticker: str, exchange: str) -> float:
    """
    Fetch real-time stock data for a given ticker symbol from specified exchange.
    """
    try:
        # Append exchange suffix to ticker
        if exchange.upper() == 'NSE':
            full_ticker = f"{ticker}.NS"
        elif exchange.upper() == 'BSE':
            full_ticker = f"{ticker}.BO"
        else:
            raise ValueError(f"Unsupported exchange: {exchange}")

        stock = yf.Ticker(full_ticker)
        history = stock.history(period="1d")
        if history.empty:
            return None
        return history['Close'][-1]

    except Exception as e:
        print(f"Error fetching {exchange} data for {ticker}: {e}")
        return None

def calculate_arbitrage(nse_price: float, bse_price: float, threshold: float = 0.5) -> Dict:
    """
    Calculate arbitrage opportunity between NSE and BSE prices.
    Returns arbitrage details if difference exceeds threshold percentage.
    """
    if nse_price is None or bse_price is None:
        return None

    price_diff = abs(nse_price - bse_price)
    diff_percentage = (price_diff / min(nse_price, bse_price)) * 100

    if diff_percentage > threshold:
        return {
            'price_difference': price_diff,
            'difference_percentage': diff_percentage,
            'buy_exchange': 'BSE' if bse_price < nse_price else 'NSE',
            'sell_exchange': 'NSE' if bse_price < nse_price else 'BSE',
            'buy_price': min(nse_price, bse_price),
            'sell_price': max(nse_price, bse_price)
        }
    return None

def detect_arbitrage_opportunities(tickers: List[str], threshold: float = 0.5) -> List[Dict]:
    """
    Detect arbitrage opportunities for a list of tickers between NSE and BSE.
    """
    opportunities = []

    for ticker in tickers:
        nse_price = fetch_exchange_data(ticker, 'NSE')
        bse_price = fetch_exchange_data(ticker, 'BSE')

        if nse_price and bse_price:
            arbitrage = calculate_arbitrage(nse_price, bse_price, threshold)
            if arbitrage:
                opportunities.append({
                    'ticker': ticker,
                    **arbitrage
                })

    return opportunities

def get_arbitrage_summary(opportunities: List[Dict]) -> pd.DataFrame:
    """
    Convert arbitrage opportunities to a pandas DataFrame for easy visualization.
    """
    if not opportunities:
        return pd.DataFrame()

    df = pd.DataFrame(opportunities)
    df = df.sort_values('difference_percentage', ascending=False)
    df = df.round(2)
    return df
