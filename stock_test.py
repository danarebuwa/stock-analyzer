import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

st.title('Company Performance Analysis')
st.write('This application fetches and analyses financial data of public companies to determine their performance. Financial statements such as income statement, balance sheet, and cash flow statement are fetched and key financial ratios are calculated to provide insights into the company’s financial health.')

if not st.session_state.get('data_fetched', False):  # If 'data_fetched' not set in session_state, show the intro
    st.markdown("## About")
    st.markdown("This application is created by **Daniel Bosun-Arebuwa**, with the aim to help investors understand fundamental analysis.")


# Function to format numbers with commas and dollar signs
def format_dollars(value):
    return f"${value:,.0f}"

@st.cache(show_spinner=False)
def get_financial_statement_symbols(api_key):
    url = f"https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data
    
# Function to fetch income statement
def get_income_statement(symbol, api_key):
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{symbol}?limit=120&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

# Function to fetch quote
def get_quote(symbol, api_key):
    url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data[0]

# Function to fetch balance sheet
def get_balance_sheet(symbol, api_key):
    url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{symbol}?limit=1&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data[0]

# Function to fetch cash flow statement
def get_cash_flow_statement(symbol, api_key):
    url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{symbol}?limit=1&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data[0]
# Function to fetch enterprise value
def get_enterprise_value(symbol, api_key):
    url = f"https://financialmodelingprep.com/api/v3/enterprise-values/{symbol}?limit=40&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

# Function to fetch financial statement growth
def get_financial_statement_growth(symbol, api_key):
    url = f"https://financialmodelingprep.com/api/v3/financial-growth/{symbol}?limit=20&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data


# Function to fetch key metrics
def get_key_metrics(symbol, api_key):
    url = f"https://financialmodelingprep.com/api/v3/key-metrics/{symbol}?limit=40&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

# Function to fetch company rating
def get_company_rating(symbol, api_key):
    url = f"https://financialmodelingprep.com/api/v3/rating/{symbol}?apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

# Function to fetch discounted cash flow value
def get_discounted_cash_flow(symbol, api_key):
    url = f"https://financialmodelingprep.com/api/v3/discounted-cash-flow/{symbol}?apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

st.sidebar.write("Please get your FMP API key here [link](https://financialmodelingprep.com/developer)")
api_key = st.sidebar.text_input("Enter your API key")
companies = get_financial_statement_symbols(api_key)
selected_company = st.sidebar.selectbox("Select a company", companies)

st.sidebar.markdown("## How to use")
st.sidebar.markdown("""
1. Enter your API key in the box above. Press Enter then allow a second for list to load
2. Select a company from the dropdown list. Allow a second before next step
3. Click the 'Fetch data' button.
4. After the data is fetched, you can view the company's financial statements, as well as key financial ratios and metrics on the main page.
5. You can also select metrics to visualize in the 'Select the metrics to visualize' dropdown on the main page.
""")

# Initialize the session_state for fetched_data
if 'fetched_data' not in st.session_state:
    st.session_state['fetched_data'] = None

# Fetch data button
if st.sidebar.button("Fetch data"):
    if api_key and selected_company:
        # Fetch all the data and store it in session_state
        st.session_state['fetched_data'] = {
            'income_data': get_income_statement(selected_company, api_key)[0],
            'balance_data': get_balance_sheet(selected_company, api_key),
            'cash_flow_data': get_cash_flow_statement(selected_company, api_key),
            'quote_data': get_quote(selected_company, api_key),
            'enterprise_value_data': get_enterprise_value(selected_company, api_key),
            'financial_statement_growth_data': get_financial_statement_growth(selected_company, api_key),
            'key_metrics_data': get_key_metrics(selected_company, api_key),
            'company_rating_data': get_company_rating(selected_company, api_key),
            'discounted_cash_flow_data': get_discounted_cash_flow(selected_company, api_key),
        }

# Only process and display the data if it has been fetched
if st.session_state['fetched_data'] is not None:
        # Main content
        income_data = st.session_state['fetched_data']['income_data']
        income_df = pd.DataFrame(income_data, index=[0]).transpose()
        income_df = income_df.applymap(lambda x: "{:,}".format(x) if isinstance(x, (int, float)) else x)
        transposed_income_data = pd.DataFrame(income_data, index=[0]).transpose()
        st.subheader("Income Statement")
        st.table(income_df)

        # Balance Sheet
        balance_data = st.session_state['fetched_data']['balance_data']
        balance_df = pd.DataFrame(balance_data, index=[0]).transpose()
        balance_df = balance_df.applymap(lambda x: "{:,}".format(x) if isinstance(x, (int, float)) else x)
        st.subheader("Balance Sheet")
        st.table(balance_df)


        # Cash Flow Statement
        cash_flow_data = st.session_state['fetched_data']['cash_flow_data']   
        transposed_cash_flow_data = pd.DataFrame(cash_flow_data, index=[0]).transpose()
        st.subheader("Cash Flow Statement")
        st.table(transposed_cash_flow_data)

        # Enterprise Value
        # If enterprise_value_data is a list of dictionaries, you might need to select the first dictionary
        enterprise_value_data = st.session_state['fetched_data']['enterprise_value_data']
        if isinstance(enterprise_value_data, list):
            enterprise_value_data = enterprise_value_data[0]
        transposed_enterprise_value_data = pd.DataFrame(enterprise_value_data, index=[0]).transpose()
        st.subheader("Enterprise Value")
        st.table(transposed_enterprise_value_data)


        data = get_financial_statement_growth(selected_company, api_key)
        df = pd.DataFrame(data)

        # Get the list of possible columns to visualize (excluding 'date')
        options = df.columns.drop('date').tolist()

        # Check if 'selected_columns' is already in session_state
        # If it isn't, initialize it to an empty list
        if 'selected_columns' not in st.session_state:
            st.session_state['selected_columns'] = []

        # Use multiselect to let the user pick which columns to visualize
        # And store the selections in session_state
        st.session_state['selected_columns'] = st.multiselect('Select the metrics to visualize', options, st.session_state['selected_columns'])

        # Create a Plotly figure
        fig = go.Figure()

        # Add a trace for each selected column
        for col in st.session_state['selected_columns']:
            fig.add_trace(go.Scatter(x=df['date'], y=df[col], mode='lines+markers', name=col))

        # Set plot title and labels
        fig.update_layout(title='Financial Statement Growth Over the Years',
                            xaxis_title='Year',
                            yaxis_title='Growth')

        # Display the figure
        st.plotly_chart(fig)


        # Transpose and display Financial Statement Growth
        # Assuming financial_statement_growth_data is a list of dictionaries
        financial_statement_growth_data = st.session_state['fetched_data']['financial_statement_growth_data']
        if isinstance(financial_statement_growth_data, list) and len(financial_statement_growth_data) > 0:
            transposed_financial_statement_growth_data = pd.DataFrame(financial_statement_growth_data[0], index=[0]).transpose()
        else:
            transposed_financial_statement_growth_data = pd.DataFrame(financial_statement_growth_data, index=[0]).transpose()

        st.subheader("Financial Statement Growth")
        st.table(transposed_financial_statement_growth_data)

        # Transpose and display Key Metrics
        # Assuming key_metrics_data is a list of dictionaries
        key_metrics_data = st.session_state['fetched_data']['key_metrics_data']
        if isinstance(key_metrics_data, list) and len(key_metrics_data) > 0:
            transposed_key_metrics_data = pd.DataFrame(key_metrics_data[0], index=[0]).transpose()
        else:
            transposed_key_metrics_data = pd.DataFrame(key_metrics_data, index=[0]).transpose()

        st.subheader("Key Metrics")
        st.table(transposed_key_metrics_data)

        # Transpose and display Company Rating
        # Assuming company_rating_data is a list of dictionaries
        company_rating_data = st.session_state['fetched_data']['company_rating_data']
        if isinstance(company_rating_data, list) and len(company_rating_data) > 0:
            transposed_company_rating_data = pd.DataFrame(company_rating_data[0], index=[0]).transpose()
        else:
            transposed_company_rating_data = pd.DataFrame(company_rating_data, index=[0]).transpose()

        st.subheader("Company Rating")
        st.table(transposed_company_rating_data)

        # Transpose and display Discounted Cash Flow Value
        # Assuming discounted_cash_flow_data is a list of dictionaries
        discounted_cash_flow_data = st.session_state['fetched_data']['discounted_cash_flow_data']
        if isinstance(discounted_cash_flow_data, list) and len(discounted_cash_flow_data) > 0:
            transposed_discounted_cash_flow_data = pd.DataFrame(discounted_cash_flow_data[0], index=[0]).transpose()
        else:
            transposed_discounted_cash_flow_data = pd.DataFrame(discounted_cash_flow_data, index=[0]).transpose()

        st.subheader("Discounted Cash Flow Value")
        st.table(transposed_discounted_cash_flow_data)


        # Calculate and display financial ratios with explanations
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

        # Calculate and display Operating Cash Flow and Free Cash Flow
        operating_cash_flow = cash_flow_data['operatingCashFlow']
        st.write("Operating Cash Flow (OCF): This is a measure of the amount of cash generated by a company's normal business operations. It can be a better measure of a company's profitability as it is harder to manipulate with accounting practices.")
        st.write(f"**Operating Cash Flow:** {format_dollars(operating_cash_flow)}")

        capital_expenditure = cash_flow_data['capitalExpenditure']
        free_cash_flow = operating_cash_flow - capital_expenditure
        st.write("Free Cash Flow (FCF): This is a measure of a company's financial performance and represents the cash that a company is able to generate after spending the money required to maintain or expand its asset base.")
        st.write(f"**Free Cash Flow:** {format_dollars(free_cash_flow)}")

        quote_data = st.session_state['fetched_data']['quote_data']
        price_to_book_ratio = quote_data['price'] / (balance_data['totalStockholdersEquity'] / income_data['weightedAverageShsOut'])
        st.write("Price to Book Ratio (P/B): This ratio compares a company's market value to its book value. A low P/B ratio could mean the stock is undervalued, while a high P/B ratio could mean the stock is overvalued.")
        st.write(f"**Price to Book Ratio:** {(price_to_book_ratio)}")

        price_to_earnings_ratio = quote_data['price'] / income_data['epsdiluted']
        st.write("Price to Earnings Ratio (P/E): This ratio measures the price you pay for each dollar of earning. A high P/E ratio could mean the stock's price is high relative to earnings and possibly overvalued. Conversely, a low P/E might indicate that the current stock price is low relative to earnings.")
        st.write(f"**Price to Earnings Ratio:** {(price_to_earnings_ratio)}")

        debt_ratio = balance_data['totalDebt'] / balance_data['totalAssets']
        st.write("Debt Ratio: This ratio indicates what proportion of debt a company has relative to its assets. A debt ratio greater than 1 indicates that a company has more debt than assets, while a debt ratio less than 1 indicates that a company has more assets than debt.")
        st.write(f"**Debt Ratio:** {(debt_ratio)}")

        
