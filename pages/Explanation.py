import streamlit as st

# Your existing Streamlit code...

# Display the formula in a more compact form
st.write("The formula for the ETF future value of the investment is:")
st.latex(r'''
FV \approx P \left(1 + \frac{r}{12}\right)^{12N} + \sum_{k=1}^{12N} C_k \left(1 + \frac{r}{12}\right)^{12N - k}
''')

st.write("Where:")
st.latex(r'''
P = \text{initial principal balance (lump sum investment)}
''')
st.latex(r'''
r = \text{annual interest rate (decimal)}
''')
st.latex(r'''
N = \text{number of years}
''')
st.latex(r'''
C_k = C \left(1 + \frac{i}{100}\right)^{\left\lfloor \frac{k-1}{12} \right\rfloor}
''')

st.write("Here,")
st.latex(r'''
C = \text{initial monthly contribution}
''')
st.latex(r'''
i = \text{yearly increase percentage}
''')
st.latex(r'''
\left\lfloor \frac{k-1}{12} \right\rfloor = \text{floor division for yearly increase}
''')

st.latex(r'''
\text{For Average Return:} \\
\bar{R} = \frac{1}{n} \sum_{i=1}^{n} R_i
''')

st.latex(r'''
\text{For Annualized Return:} \\
\text{Annualized Return} = \left( \prod_{i=1}^{n} (1 + R_i) \right)^{\frac{1}{n}} - 1
''')

st.latex(r'''
\text{Annualized Return} = \left( \frac{\text{Final Value}}{\text{Initial Value}} \right)^{\frac{1}{n}} - 1
''')

st.write('''
### Data Input and Investment Estimation Methodology

**Data Input:**

Our investment calculator utilizes real-time market data to provide the most accurate and up-to-date analysis. The data for ETF stocks is sourced directly from the Yahoo Finance API, renowned for its reliability and wide coverage of financial information. When you select a specific ETF stock, our system retrieves historical price data for that stock, starting from January 1, 1990, up to today's date. This comprehensive dataset forms the foundation of our investment simulations.

**Estimation of Investment Returns:**

The investment returns are estimated using a combination of historical data analysis and financial projection techniques. Here’s how our calculator works:

1. **Initial Parameters:**
   - You provide the initial investment amount (lump sum), monthly contribution, desired investment period (in years), and an annual percentage increase in your monthly contribution.
   - The selected ETF stock's historical data is analyzed to determine its annualized return rate.

2. **Compounded Growth Calculation:**
   - The initial investment amount is compounded over the investment period based on the calculated annualized return. This process assumes monthly compounding to reflect the real-world growth of investments.
   - Your monthly contributions, adjusted annually based on your specified increase rate, are also factored into the calculation. Each contribution is compounded individually for the remaining investment period.

3. **Projection of Future Value:**
   - By summing the compounded initial investment and the compounded value of all monthly contributions, we project the future value of your investment.
   - This method provides an estimate of how much your investment could grow, taking into account the effect of reinvesting dividends and the growth potential of the ETF stock.

4. **Monthly Growth Tracking:**
   - To give you a detailed view of your investment’s growth trajectory, we also calculate and display the monthly growth in investment value. This insight allows you to see not just the final outcome, but also how your investment could evolve over time.

**Please Note:** 
Our estimates are based on historical data and do not guarantee future performance. Market volatility, economic changes, and other external factors can impact investment returns. We recommend using these estimates as a guideline and consulting with a financial advisor for personalized investment advice.
''')


# Rest of your Streamlit code...
# hide made with streamlit
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)