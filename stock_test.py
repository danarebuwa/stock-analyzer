import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

st.title('Company Performance Analysis')
st.write('This application fetches and analyses financial data of public companies to determine their performance. Financial statements such as income statement, balance sheet, and cash flow statement are fetched and key financial ratios are calculated to provide insights into the company’s financial health.')

if 'fetched_data' not in st.session_state:
    st.session_state['fetched_data'] = False
    
if st.session_state['fetched_data'] == False:
    st.markdown("## About")
    st.markdown("This application is created by **Daniel Bosun-Arebuwa**, with the aim to help investors understand fundamental analysis.")

    st.markdown("## How to Use")
    st.markdown("""
    1. Get your API key from [Financial Modeling Prep](https://financialmodelingprep.com/developer).
    2. Enter the API key in the sidebar.
    3. Select the company you are interested in from the dropdown list in the sidebar.
    4. Click on the 'Fetch data' button.
    5. View the fetched data and financial ratios, and explore the visualizations.
    """)
    

def format_dollars(value):
    return f"${value:,.0f}"


@st.cache(show_spinner=False)
def fetch_resource(url: str):
    return requests.get(url).json()


def get_financial_statement_symbols(api_key):
    url = f"https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey={api_key}"
    data = fetch_resource(url)
    return data


def get_income_statement(symbol, api_key):
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{symbol}?limit=120&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data


def get_quote(symbol, api_key):
    url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data[0]


def get_balance_sheet(symbol, api_key):
    url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{symbol}?limit=1&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data[0]


def get_cash_flow_statement(symbol, api_key):
    url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{symbol}?limit=1&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data[0]

def get_enterprise_value(symbol, api_key):
    url = f"https://financialmodelingprep.com/api/v3/enterprise-values/{symbol}?limit=40&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

def get_financial_statement_growth(symbol, api_key):
    url = f"https://financialmodelingprep.com/api/v3/financial-growth/{symbol}?limit=20&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data



def get_key_metrics(symbol, api_key):
    url = f"https://financialmodelingprep.com/api/v3/key-metrics/{symbol}?limit=40&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data


def get_company_rating(symbol, api_key):
    url = f"https://financialmodelingprep.com/api/v3/rating/{symbol}?apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data


def get_discounted_cash_flow(symbol, api_key):
    url = f"https://financialmodelingprep.com/api/v3/discounted-cash-flow/{symbol}?apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

st.sidebar.write("Please get your FMP API key here [link](https://financialmodelingprep.com/developer)")


api_key = st.sidebar.text_input("Enter your API key")
companies = get_financial_statement_symbols(api_key)
selected_company = st.sidebar.selectbox("Select a company", companies)

if st.sidebar.button("Fetch data"):
    if api_key and selected_company:
        st.session_state['fetched_data'] = True
        # Main content
        income_data = get_income_statement(selected_company, api_key)[0]
        balance_data = get_balance_sheet(selected_company, api_key)
        cash_flow_data = get_cash_flow_statement(selected_company, api_key)
        quote_data = get_quote(selected_company, api_key)
        enterprise_value_data = get_enterprise_value(selected_company, api_key)
        financial_statement_growth_data = get_financial_statement_growth(selected_company, api_key)
        key_metrics_data = get_key_metrics(selected_company, api_key)
        company_rating_data = get_company_rating(selected_company, api_key)
        discounted_cash_flow_data = get_discounted_cash_flow(selected_company, api_key)


       
        st.subheader("Income Statement")
        st.table(pd.DataFrame(income_data, index=[0]))

        st.subheader("Balance Sheet")
        st.table(pd.DataFrame(balance_data, index=[0]))

        st.subheader("Cash Flow Statement")
        st.table(pd.DataFrame(cash_flow_data, index=[0]))

        st.subheader("Enterprise Value")
        st.table(pd.DataFrame(enterprise_value_data))

        data = get_financial_statement_growth(selected_company, api_key)
        df = pd.DataFrame(data)


       
        options = df.columns.drop('date').tolist()

        
        columns_to_plot = st.multiselect('Select the metrics to visualize', options)

        fig = go.Figure()

       
        for col in columns_to_plot:
            fig.add_trace(go.Scatter(x=df['date'], y=df[col], mode='lines+markers', name=col))

    
        fig.update_layout(title='Financial Statement Growth Over the Years',
                        xaxis_title='Year',
                        yaxis_title='Growth')

    
        st.plotly_chart(fig)

        st.subheader("Financial Statement Growth")
        st.table(pd.DataFrame(financial_statement_growth_data))


        st.subheader("Key Metrics")
        st.table(pd.DataFrame(key_metrics_data))

        st.subheader("Company Rating")
        st.table(pd.DataFrame(company_rating_data))

        st.subheader("Discounted Cash Flow Value")
        st.table(pd.DataFrame(discounted_cash_flow_data))

        
        gross_margin = income_data['grossProfit'] / income_data['revenue']
        st.write("Gross Margin: This ratio indicates the percentage of revenue that exceeds the cost of goods sold. A higher gross margin indicates greater efficiency in turning raw materials into income.")
        st.write(f"**Gross Margin:** {(gross_margin)}")

        operating_margin = income_data['operatingIncome'] / income_data['revenue']
        st.write("Operating Margin: This ratio indicates how much profit a company makes on a dollar of sales after paying for variable costs of production, but before paying interest or tax.")
        st.write(f"**Operating Margin:** {(operating_margin)}")

        net_profit_margin = income_data['netIncome'] / income_data['revenue']
        st.write("Net Profit Margin: This ratio indicates how much net profit a company makes with its total sales revenue. A high net profit margin means that a company is more efficient at converting sales into actual profit.")
        st.write(f"**Net Profit Margin:** {(net_profit_margin)}")

        roa = income_data['netIncome'] / balance_data['totalAssets']
        st.write("Return on Assets (ROA): This ratio indicates how profitable a company is relative to its total assets. ROA gives an idea as to how efficient management is at using its assets to generate earnings.")
        st.write(f"**Return on Assets (ROA):** {(roa)}")

        
        operating_cash_flow = cash_flow_data['operatingCashFlow']
        st.write("Operating Cash Flow (OCF): This is a measure of the amount of cash generated by a company's normal business operations. It can be a better measure of a company's profitability as it is harder to manipulate with accounting practices.")
        st.write(f"**Operating Cash Flow:** {format_dollars(operating_cash_flow)}")

        capital_expenditure = cash_flow_data['capitalExpenditure']
        free_cash_flow = operating_cash_flow - capital_expenditure
        st.write("Free Cash Flow (FCF): This is a measure of a company's financial performance and represents the cash that a company is able to generate after spending the money required to maintain or expand its asset base.")
        st.write(f"**Free Cash Flow:** {format_dollars(free_cash_flow)}")

        price_to_book_ratio = quote_data['price'] / (balance_data['totalStockholdersEquity'] / income_data['weightedAverageShsOut'])
        st.write("Price to Book Ratio (P/B): This ratio compares a company's market value to its book value. A low P/B ratio could mean the stock is undervalued, while a high P/B ratio could mean the stock is overvalued.")
        st.write(f"**Price to Book Ratio:** {(price_to_book_ratio)}")

        price_to_earnings_ratio = quote_data['price'] / income_data['epsdiluted']
        st.write("Price to Earnings Ratio (P/E): This ratio measures the price you pay for each dollar of earning. A high P/E ratio could mean the stock's price is high relative to earnings and possibly overvalued. Conversely, a low P/E might indicate that the current stock price is low relative to earnings.")
        st.write(f"**Price to Earnings Ratio:** {(price_to_earnings_ratio)}")

        debt_ratio = balance_data['totalDebt'] / balance_data['totalAssets']
        st.write("Debt Ratio: This ratio indicates what proportion of debt a company has relative to its assets. A debt ratio greater than 1 indicates that a company has more debt than assets, while a debt ratio less than 1 indicates that a company has more assets than debt.")
        st.write(f"**Debt Ratio:** {(debt_ratio)}")

        
