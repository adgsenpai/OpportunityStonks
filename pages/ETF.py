import streamlit as st
from datetime import date

import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd
import STOCKDATA

START = "1990-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('JSE ETF Stocks')

# hide made with streamlit
hide_streamlit_style = """
			<style>
			#MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
			</style>
			"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


stocks = STOCKDATA.ETF

def format_func(option):
    return stocks[option]


# sidebar
st.sidebar.header('Opportunity Stonks App')

with st.sidebar:
    selected_stock = st.selectbox('Select company stock for prediction', options=list(
        stocks.keys()), format_func=format_func)
    n_years = st.slider('Years of prediction:', 1, 25)
    period = n_years * 365


with st.sidebar:
    st.write('Developed with ❤️ by [ADGSTUDIOS](https://adgstudios.co.za/)')


@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data


data = load_data(selected_stock)

st.subheader('Raw data')
st.write(data.tail())

# Plot raw data


def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'],
                  y=data['Open'], name="stock_open"))
    fig.add_trace(go.Scatter(x=data['Date'],
                  y=data['Close'], name="stock_close"))
    fig.layout.update(
        title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)


def dividendData():
    div = yf.Ticker(selected_stock)
    div = div.dividends
    div = div.reset_index()
    div = div.rename(columns={"Date": "ds", "Dividends": "y"})
    st.subheader('Dividend Payouts')
    st.write(div.tail())
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=div['ds'], y=div['y'], name="dividends"))
    fig.layout.update(title_text='Dividend Payout Plot',
                      xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)
    return div


def News():
    # Get the data
    news = yf.Ticker(selected_stock)
    news = news.news
    st.subheader('News')

    df = pd.DataFrame(news)
    # dorp uuid
    df = df.drop(['uuid', 'providerPublishTime', 'thumbnail',
                 'relatedTickers', 'type'], axis=1)

    # make link clickable
    def make_clickable(val):
        return '<a target="_blank" href="{}">{}</a>'.format(val, val)

    df = df.style.format({'link': make_clickable})
    df = df.to_html(escape=False) + '<br></br>'
    st.write(df, unsafe_allow_html=True)


def FinancialStatements():
    # Get the data
    stock = yf.Ticker(selected_stock)
    stock = stock.financials
    st.subheader('Financial Statements')
    st.write(stock.tail())


with st.spinner('Loading data...'):
    plot_raw_data()

with st.spinner('Loading data...'):
    News()

with st.spinner('Loading data...'):
    FinancialStatements()

with st.spinner('Loading data...'):
    dividendData()

 