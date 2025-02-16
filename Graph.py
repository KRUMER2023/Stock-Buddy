import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import pytz
import ta

def fetch_stock_data(ticker: str, period: str, interval: str) -> pd.DataFrame:
    try:
        end_date = datetime.now()
        if period == '1wk':
            start_date = end_date - timedelta(days=7)
            data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
        else:
            data = yf.download(ticker, period=period, interval=interval)
        return data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

def process_data(data: pd.DataFrame) -> pd.DataFrame:
    if data.index.tzinfo is None:
        data.index = data.index.tz_localize('UTC')
    data.index = data.index.tz_convert('Asia/Kolkata')  # Set to Indian Standard Time (IST)
    data.reset_index(inplace=True)  # Reset index so 'Datetime' is a column, not an index
    data.rename(columns={'Date': 'Datetime'}, inplace=True)  # Ensure the 'Date' column is renamed to 'Datetime'
    
    data['Datetime'] = pd.to_datetime(data['Datetime'])
    
    return data

def calculate_metrics(data: pd.DataFrame) -> tuple:
    last_close = data['Close'].iloc[-1]
    prev_close = data['Close'].iloc[0]
    change = last_close - prev_close
    pct_change = (change / prev_close) * 100
    high = data['High'].max()
    low = data['Low'].min()
    volume = data['Volume'].sum()
    return last_close, change, pct_change, high, low, volume

def add_technical_indicators(data: pd.DataFrame) -> pd.DataFrame:
    temp_data = pd.Series(data['Close'].values.flatten())
    sma_20 = ta.trend.sma_indicator(temp_data, window=20)
    ema_20 = ta.trend.ema_indicator(temp_data, window=20)
    data['SMA_20'] = sma_20
    data['EMA_20'] = ema_20
    return data

st.set_page_config(layout="wide")
st.title('Real Time Stock Dashboard')

st.sidebar.header('Chart Parameters')
ticker = st.sidebar.text_input('Ticker', 'TCS.NS')
time_period = st.sidebar.selectbox('Time Period', ['1d', '1wk', '1mo', '1y', 'max'])
chart_type = st.sidebar.selectbox('Chart Type', ['Candlestick', 'Line'])
indicators = st.sidebar.multiselect('Technical Indicators', ['SMA 20', 'EMA 20'])

interval_mapping = {
    '1d': '1m',
    '1wk': '30m',
    '1mo': '1d',
    '1y': '1wk',
    'max': '1wk'
}

if st.sidebar.button('Update'):
    data = fetch_stock_data(ticker, time_period, interval_mapping[time_period])
    if not data.empty:
        data = process_data(data)
        data = add_technical_indicators(data)

        last_close, change, pct_change, high, low, volume = calculate_metrics(data)
        
        st.metric(label=f"{ticker} Last Price", 
                  value=f"{float(last_close):.2f} INR", 
                  delta=f"{float(change):.2f} ({float(pct_change):.2f}%)")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("High", f"{float(high):.2f} INR")
        col2.metric("Low", f"{float(low):.2f} INR")
        col3.metric("Volume", f"{float(volume):,}")
        
        fig = go.Figure()
        
        if chart_type == 'Candlestick':
            fig.add_trace(go.Candlestick(x=pd.to_datetime(data['Datetime']),
                                        open=data['Open'],
                                        high=data['High'],
                                        low=data['Low'],
                                        close=data['Close'],
                                        name='Candlestick'))
        elif chart_type == 'Line':
            fig.add_trace(go.Scatter(x=data['Datetime'], y=data['Close'], mode='lines', name='Close Price'))
        
        for indicator in indicators:
            if indicator == 'SMA 20':
                fig.add_trace(go.Scatter(x=data['Datetime'], y=data['SMA_20'], name='SMA 20', line=dict(dash='dash')))
            elif indicator == 'EMA 20':
                fig.add_trace(go.Scatter(x=data['Datetime'], y=data['EMA_20'], name='EMA 20', line=dict(dash='dot')))

        fig.update_layout(title=f'{ticker} {time_period.upper()} Chart',
                          xaxis_title='Time',
                          yaxis_title='Price (INR)',
                          height=600,
                          xaxis_rangeslider_visible=False,  # Hide range slider
                          xaxis=dict(type='date'))  # Set xaxis type to date

        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader('Historical Data')
        st.dataframe(data[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']])
        
    else:
        st.warning(f"No data found for ticker {ticker}. Please check the ticker symbol.")

st.sidebar.header('Real-Time Stock Prices')
stock_symbols = ['TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'RELIANCE.NS']
for symbol in stock_symbols:
    real_time_data = fetch_stock_data(symbol, '1d', '1m')
    if not real_time_data.empty:
        real_time_data = process_data(real_time_data)
        last_price = real_time_data['Close'].iloc[-1]
        open_price = real_time_data['Open'].iloc[0]
        change = last_price - open_price
        pct_change = (change / open_price) * 100
        st.sidebar.metric(f"{symbol}", f"{float(last_price):.2f} INR", f"{float(change):.2f} ({float(pct_change):.2f}%)")
        
st.sidebar.subheader('About')
st.sidebar.info('This dashboard provides stock data and technical indicators for various time periods. Use the sidebar to customize your view.')