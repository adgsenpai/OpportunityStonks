import streamlit as st
from datetime import date
import yfinance as yf
from plotly import graph_objs as go
import STOCKDATA
import pandas as pd

START_INVESTMENT = date.today().strftime("%Y-01-01")  # Start of the current year
TODAY = date.today().strftime("%Y-%m-%d")

st.title('JSE ETF Stocks Investment Calculator')

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
    selected_stock = st.selectbox('Select company stock for prediction', options=list(stocks.keys()), format_func=format_func)
    n_years = st.slider('Years of investment:', 1, 25)    
    period = n_years * 365    
    currency = st.selectbox('Select currency', options=['ZAR','USD'])
    monthly_contribution = st.number_input('Monthly Contribution', value=100, step=1, min_value=0)
    yearly_increase = st.number_input('Yearly Increase (%)', value=5.0, step=0.1, min_value=0.0, max_value=100.0)
    lump_sum = st.number_input('Lump Sum Investment', value=0, step=1, min_value=0)

with st.sidebar:
    st.write('Developed with ❤️ by [ADGSTUDIOS](https://adgstudios.co.za/)')

@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, START_INVESTMENT, TODAY)
    data.reset_index(inplace=True)
    return data

data = load_data(selected_stock)

# Compute the number of years based on the data's date range
actual_years = (data['Date'].iloc[-1] - data['Date'].iloc[0]).days / 365.25

initial_price = data['Close'].iloc[0]
final_price = data['Close'].iloc[-1]

# Average Return for the entire period
average_return = (final_price - initial_price) / initial_price

# Annualized Return
annualized_return = (final_price / initial_price) ** (1/actual_years) - 1

with st.expander("Investment Summary"):
	st.metric(label="Average Return", value=f"{average_return:.2%}")
	st.metric(label="Annualized Return", value=f"{annualized_return:.2%}")

def simulate_investment(data, monthly_contribution, yearly_increase, lump_sum, annualized_return, n_years):
    # Create monthly date range starting from the current year
    investment_dates = pd.date_range(START_INVESTMENT, periods=n_years*12, freq='M')
    
    # Initialize DataFrame
    investment_df = pd.DataFrame({
        'Date': investment_dates,
        'Value': 0,
        'Monthly Growth (Value)': 0  # New column for raw money growth
    })

    # Set initial value
    investment_value = lump_sum
    
    for i in range(len(investment_df)):
        # Monthly contribution increases every year
        if i % 12 == 0 and i != 0:
            monthly_contribution += monthly_contribution * (yearly_increase / 100)
        
        # Apply monthly return (approximation)
        monthly_return = (1 + annualized_return) ** (1/12) - 1
        previous_value = investment_value  # Save the previous value
        investment_value = investment_value * (1 + monthly_return) + monthly_contribution
        investment_df['Value'].iloc[i] = investment_value

        # Calculate monthly growth value in terms of raw money and store in the DataFrame
        if i != 0:
            investment_df['Monthly Growth (Value)'].iloc[i] = investment_value - previous_value
    
    return investment_df

# Simulate investment based on input values
investment_df = simulate_investment(data, monthly_contribution, yearly_increase, lump_sum, annualized_return, n_years)

with st.expander("Investment Yield"):
	st.metric(label="Final Value "+ currency, value=f"{investment_df['Value'].iloc[-1]:.2f}")
	st.metric(label="Total Investment "+ currency, value=f"{(monthly_contribution * n_years * 12) + lump_sum:.2f}")
	st.metric(label="Average Monthly Growth "+ currency, value=f"{investment_df['Monthly Growth (Value)'].mean():.2f}")

	

# Plotting
def plot_investment():
    fig = go.Figure()
    
    # Stock data
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
    
    # Simulated investment data
    fig.add_trace(go.Scatter(x=investment_df['Date'], y=investment_df['Value'], name="investment_value", mode='lines'))

    # Monthly Growth in raw money value
    fig.add_trace(go.Scatter(x=investment_df['Date'], y=investment_df['Monthly Growth (Value)'], name="Monthly Growth (Value)"))
    
    fig.layout.update(title_text='Investment Over Time and Monthly Growth Value', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_investment()

# render table
st.subheader('Investment Data')
st.write(investment_df)

st.subheader('Raw data')
st.write(data.tail())

# Plot raw data
def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
    fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

