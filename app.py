# app.py

import streamlit as st
import pandas as pd
from arbitrage_detector import detect_arbitrage_opportunities

# Set page config
st.set_page_config(
    page_title="Stock Arbitrage Detector",
    page_icon="📈",
    layout="wide"
)

# Title and description
st.title("📈 Stock Arbitrage Detector")
st.markdown("""
    This app detects arbitrage opportunities between NSE and BSE exchanges.
    It compares stock prices across both exchanges and identifies potential arbitrage opportunities.
""")

# Sidebar controls
st.sidebar.header("Settings")

# Default tickers (top 150 by market cap)
default_tickers = [
    "RELIANCE", "TCS", "HDFCBANK", "INFY", "HINDUNILVR", "ICICIBANK", "BHARTIARTL", "SBIN", "HDFC", "BAJFINANCE",
    "KOTAKBANK", "ASIANPAINT", "WIPRO", "MARUTI", "AXISBANK", "LT", "ITC", "ULTRACEMCO", "HCLTECH", "ADANIPORTS",
    "SUNPHARMA", "TITAN", "BAJAJFINSV", "TECHM", "DIVISLAB", "POWERGRID", "NTPC", "HINDALCO", "TATASTEEL", "SBILIFE",
    "GRASIM", "SHREECEM", "DRREDDY", "BAJAJ-AUTO", "BRITANNIA", "NESTLEIND", "TATACONSUM", "COALINDIA", "HDFCLIFE", "M&M",
    "IOC", "BPCL", "ONGC", "TATAMOTORS", "CIPLA", "EICHERMOT", "UPL", "HEROMOTOCO", "JSWSTEEL", "INDUSINDBK",
    "DABUR", "HAVELLS", "PIDILITIND", "BERGEPAINT", "GODREJCP", "COLPAL", "MARICO", "AMBUJACEM", "SIEMENS", "DLF",
    "BOSCHLTD", "NAUKRI", "LUPIN", "GAIL", "VEDL", "SAIL", "NMDC", "BANKBARODA", "PNB", "CANBK",
    "BIOCON", "TORNTPHARM", "AUROPHARMA", "CADILAHC", "ALKEM", "TORNTPOWER", "PAGEIND", "MUTHOOTFIN", "BANDHANBNK", "FEDERALBNK",
    "ESCORTS", "ASHOKLEY", "BALKRISIND", "RAMCOCEM", "TATAPOWER", "JINDALSTEL", "SRTRANSFIN", "LICHSGFIN", "RECLTD", "PFC",
    "CONCOR", "CUMMINSIND", "BHARATFORG", "EXIDEIND", "APOLLOTYRE", "BATAINDIA", "VOLTAS", "MINDTREE", "MPHASIS", "LTTS",
    "TATACOMM", "PERSISTENT", "COFORGE", "APOLLOHOSP", "FORTIS", "MAXHEALTH", "SYNGENE", "LALPATHLAB", "METROPOLIS", "STAR",
    "NATCOPHARM", "GRANULES", "AJANTPHARM", "ASTRAZEN", "GLAXO", "PFIZER", "ABBOTINDIA", "MRF", "BAJAJHLDNG", "PGHH",
    "3MINDIA", "WHIRLPOOL", "GILLETTE", "BAYERCROP", "GODREJIND", "CRISIL", "HONAUT", "KANSAINER", "AKZOINDIA", "BASF",
    "TATACHEM", "NAVINFLUOR", "ATUL", "SUMICHEM", "SRF", "PIIND", "UBL", "MCDOWELL-N", "RADICO", "MAHABANK",
    "CENTRALBK", "UNIONBANK", "CHOLAFIN", "MANAPPURAM", "IBULHSGFIN", "RBLBANK", "IDFC", "CESC", "NHPC", "SJVN"
]

# User inputs
threshold = st.sidebar.slider(
    "Arbitrage Threshold (%)",
    min_value=0.1,
    max_value=5.0,
    value=0.5,
    step=0.1,
    help="Minimum price difference percentage to consider as arbitrage opportunity"
)

# Add refresh button
if st.sidebar.button("🔄 Refresh Data"):
    st.experimental_rerun()

# Main content
try:
    with st.spinner("Fetching arbitrage opportunities..."):
        opportunities = detect_arbitrage_opportunities(default_tickers, threshold)

    if opportunities:
        # Convert to DataFrame for display
        df = pd.DataFrame(opportunities)
        
        # Display summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Opportunities", len(opportunities))
        with col2:
            avg_diff = df['difference_percentage'].mean()
            st.metric("Avg Price Difference %", f"{avg_diff:.2f}%")
        with col3:
            max_diff = df['difference_percentage'].max()
            st.metric("Max Price Difference %", f"{max_diff:.2f}%")

        # Display opportunities table
        st.subheader("Arbitrage Opportunities")
        st.dataframe(
            df.style.format({
                'price_difference': '₹{:.2f}',
                'difference_percentage': '{:.2f}%',
                'buy_price': '₹{:.2f}',
                'sell_price': '₹{:.2f}'
            }),
            use_container_width=True
        )

    else:
        st.info("No arbitrage opportunities found above the specified threshold.")

except Exception as e:
    st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Built with ❤️ using Streamlit | Data source: Yahoo Finance</p>
    </div>
""", unsafe_allow_html=True)
