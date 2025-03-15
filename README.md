
# Stock Arbitrage Detector

A Python application that detects arbitrage opportunities between NSE (National Stock Exchange) and BSE (Bombay Stock Exchange) for the top 50 stocks by market capitalization.

## Features

- Real-time price comparison between NSE and BSE
- Configurable arbitrage threshold
- Interactive web interface with live updates
- Summary metrics and detailed opportunity view
- Top 50 Indian stocks by market cap

## Prerequisites

- Python 3.7+
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd stock-arbitrage-detector
```

2. Install required packages:
```bash
pip install streamlit pandas yfinance
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run scripts/app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Use the sidebar controls to:
   - Adjust the arbitrage threshold
   - Refresh data

## How it Works

The application:
1. Fetches real-time stock prices from both NSE and BSE using Yahoo Finance API
2. Compares prices between exchanges
3. Identifies opportunities where price difference exceeds the threshold
4. Displays actionable arbitrage opportunities with buy/sell recommendations

## Data Source

Stock data is fetched using the Yahoo Finance API through the `yfinance` package. NSE stocks are suffixed with .NS and BSE stocks with .BO

## License

MIT License
