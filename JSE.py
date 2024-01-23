import streamlit as st
from datetime import date

import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd
import STOCKDATA
import requests
from PIL import Image
from io import BytesIO


START = "1990-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('JSE Stocks')

# hide made with streamlit
hide_streamlit_style = """
			<style>
			#MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
			</style>
			"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


stocks = STOCKDATA.JSE




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
    try:
        data = yf.download(ticker, START, TODAY)
        data.reset_index(inplace=True)
        # remove outliers from data remove if standard deviation is less than 3
        data = data[data['Close'].between(data['Close'].quantile(.01), data['Close'].quantile(.99))]        
        return data
    except Exception as e:
        st.error(f"Failed to download data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of an error


data = load_data(selected_stock)






st.subheader('Company Details for '+selected_stock)

st.subheader('Stock Data')

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

    ticker = yf.Ticker(selected_stock)

    # show actions (dividends, splits, capital gains)
    st.subheader('Actions')
    st.write(ticker.actions)

    st.subheader('Splits')
    st.write(ticker.splits)

    st.subheader('Capital Gains')
    st.write(ticker.capital_gains)

    return div





def ReturnTicker():
   return yf.Ticker(selected_stock)

def FinancialStatements():
    # Get the data
    ticker = yf.Ticker(selected_stock)
    stock = ticker
    stock = stock.financials
    st.subheader('Financial Statements')
    st.write(stock.tail())

 
    st.subheader('Income Statement')
    st.write(ticker.income_stmt)
    st.subheader('Quarterly Income Statement')
    st.write(ticker.quarterly_income_stmt)
    st.subheader('Balance Sheet')
    st.write(ticker.balance_sheet)
    st.subheader('Quarterly Balance Sheet')
    st.write(ticker.quarterly_balance_sheet)
    st.subheader('Cash Flow')
    st.write(ticker.cashflow)
    st.subheader('Quarterly Cash Flow')
    st.write(ticker.quarterly_cashflow)

    # show holders
    #msft.major_holders
    #msft.institutional_holders
    #msft.mutualfund_holders

    try:
        st.subheader("Major Holders")
        st.write(ticker.major_holders)
    except:
        st.write("No Major Holders")
    
    try:
        st.subheader("Institutional Holders")
        st.write(ticker.institutional_holders)
    except:        
        st.subheader("Mutual Fund Holders")
        st.write(ticker.mutualfund_holders)
    

    # show options expirations
    #msft.options
    try:
        st.subheader("Options Expirations")
        st.write(ticker.options)
    except:
        st.write("No Options Expirations")

with st.spinner('Loading data...'):
    plot_raw_data()



with st.spinner('Loading data...'):
    FinancialStatements()

with st.spinner('Loading data...'):
    dividendData()

with st.spinner('Computing Future Stock Prices...'):
    # Predict forecast with Prophet.
    df_train = data[['Date', 'Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)
    

    
    

    # Show and plot forecast
    st.subheader('Forecast data')
    st.write(forecast.tail())

    st.write(f'Forecast plot for {n_years} years')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)

    st.write("Forecast components")
    fig2 = m.plot_components(forecast)
    st.write(fig2)

def News():
    # Remove .JO from selected_stock
    stock_symbol = selected_stock.replace('JO', '')
    
    # Fetch news data from Yahoo Finance
    response = requests.get(f"https://query2.finance.yahoo.com/v1/finance/search?q={stock_symbol}",headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
    print(f'https://query2.finance.yahoo.com/v1/finance/search?q={stock_symbol}')
    
    if response.status_code == 200:
        news_data = response.json()        
        # Extract 'quotes' from news_data if available
        st.write('# News')
        if 'news' in news_data:             
             for news in news_data['news']:    
                    with st.expander(f"{news['title']}"):
                        # Display the publisher and link
                        st.markdown(f"**Publisher:** {news['publisher']}")
                        st.markdown(f"[Read More]({news['link']})")

                        # Display the thumbnail image if available
                        if 'thumbnail' in news and 'resolutions' in news['thumbnail']:
                            # Fetching the first available image resolution
                            thumbnail_url = news['thumbnail']['resolutions'][0]['url']
                            response = requests.get(thumbnail_url)
                            img = Image.open(BytesIO(response.content))
                            st.image(img, width=300)  # Adjust width as needed

                        # Display related tickers if available
                        if 'relatedTickers' in news and news['relatedTickers']:
                            st.markdown(f"**Related Tickers:** {', '.join(news['relatedTickers'])}")

                        st.markdown("---")  # Separator line
        else:
            st.write('# News')
            st.write("No quotes found in the response.")
    else:
            st.write('# News')
            st.write('No news found for this stock.')
     
ticker = yf.Ticker(selected_stock)
ticker_info = ticker.info
     
        
# Company General Information
with st.expander("Company General Information"):
    st.write(f"**Address:** {ticker_info['address1']}, {ticker_info['address2']}, {ticker_info['city']}, {ticker_info['country']}, {ticker_info['zip']}")
    st.write(f"**Phone:** {ticker_info['phone']}")
    st.write(f"**Website:** {ticker_info['website']}")
    st.write(f"**Industry:** {ticker_info['industry']}")
    # ... (other general information)

# Financial Information
with st.expander("Financial Information"):
    # Assuming these keys exist in your data
    st.write(f"**Market Cap:** {ticker_info.get('marketCap', 'N/A')}")
    st.write(f"**Previous Close:** {ticker_info.get('previousClose', 'N/A')}")
    st.write(f"**Open Price:** {ticker_info.get('open', 'N/A')}")
    # ... (other financial information)
    

# Key Personnel
with st.expander("Key Personnel"):
    # Assuming 'companyOfficers' is a list of dictionaries containing officer info
    for officer in ticker_info.get('companyOfficers', []):
        st.write(f"**Name:** {officer.get('name', 'N/A')}")
        st.write(f"**Title:** {officer.get('title', 'N/A')}")
        st.write(f"**Age:** {officer.get('age', 'N/A')}")
        st.write(f"**Total Pay:** {officer.get('totalPay', 'N/A')}")
        st.write("---")  # Separator line

# Risk Assessment
with st.expander("Risk Assessment"):
    st.write(f"**Audit Risk:** {ticker_info.get('auditRisk', 'N/A')}")
    st.write(f"**Board Risk:** {ticker_info.get('boardRisk', 'N/A')}")
    st.write(f"**Compensation Risk:** {ticker_info.get('compensationRisk', 'N/A')}")
        
# Business Summary
with st.expander("Business Summary"):
    st.write(ticker_info.get('longBusinessSummary', 'N/A'))

# Performance Metrics
with st.expander("Performance Metrics"):
    st.write(f"**Earnings Growth:** {ticker_info.get('earningsGrowth', 'N/A')}")
    st.write(f"**Revenue Growth:** {ticker_info.get('revenueGrowth', 'N/A')}")
    st.write(f"**Return on Assets:** {ticker_info.get('returnOnAssets', 'N/A')}")
    st.write(f"**Return on Equity:** {ticker_info.get('returnOnEquity', 'N/A')}")
    # ... (other performance metrics)        
        
with st.spinner('Loading News data...'):
    News()
