import streamlit as st
import plotly.express as px
import pandas as pd
import requests
from datetime import datetime, timedelta
from PIL import Image

# ------------- Title of the page -------------
st.set_page_config(page_title='Bitcoin Blockchain live analysis', page_icon=':bar_chart:', layout='wide')
# Title and bitcoin logos. a lot of them.
st.title('Analisi in diretta di Bitcoin - BitPolito')
bitcoin_logo = 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bitcoin.svg/1200px-Bitcoin.svg.png'
bitpolito_logo = Image.open("bitpolito_logo.png")
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11 = st.columns(11)
col1.image(bitcoin_logo, width=50)
col2.image(bitpolito_logo, width=50)
col3.image(bitcoin_logo, width=50)
col4.image(bitpolito_logo, width=50)
col5.image(bitcoin_logo, width=50)
col6.image(bitpolito_logo, width=50)
col7.image(bitcoin_logo, width=50)
col8.image(bitpolito_logo, width=50)
col9.image(bitcoin_logo, width=50)
col10.image(bitpolito_logo, width=50)
col11.image(bitcoin_logo, width=50)


# ------------- Bitcoin Nodes -------------
# create two columns
col1, col2 = st.columns(2)
# ----- on the first column put a map of the world with all the bitcoin nodes
map_data = requests.get('https://bitnodes.io/api/v1/snapshots/latest/?field=coordinates')
col1.header("Nodi Bitcoin nel mondo")
map_data = pd.DataFrame(map_data.json()['coordinates'], columns=['lat', 'lon'])
col1.map(map_data, zoom=1, use_container_width=True)
st.write("Fonte: https://bitnodes.io/")

# ----- on the second column put some statistics about the nodes
col2.header("Statistiche sui nodi")
nodes_data = requests.get('https://bitnodes.io/api/v1/snapshots/latest/')
nodes_data = nodes_data.json()
# numbr of nodes
col2.write(f"Nodi totali: **{nodes_data['total_nodes']}**")
# top cities
cities = {}
for node in nodes_data['nodes'].values():
    if node[-3] not in cities:
        cities[node[-3]] = 1
    else:
        cities[node[-3]] += 1
# sort cities by number of nodes
cities = {k: v for k, v in sorted(cities.items(), key=lambda item: item[1], reverse=True)}
del cities[None]
# display top 10 cities in a bullet list
col2.write("Top 10 città per numero di nodi:")
for i, info in enumerate(list(cities)[:10]):
    city = info.split('/')[1]
    continent = info.split('/')[0]
    col2.write(f"{i+1}) {city} ({continent}): **{cities[info]} nodi**")


# ------------- Date sidebar (for network data) -------------
st.header("Startistiche sulla rete Bitcoin")
# Define date range dropdown options
date_ranges = {
    "All": 365*20,
    "Last 7 Days": 7,
    "Last 30 Days": 30,
    "Last 90 Days": 90,
    "Last Year": 365,
    "Last 5 Years": 365*5
}
# Create a selectbox panel for date filters
date_range = st.selectbox("Date Range", options=list(date_ranges.keys()))
end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
start_date = end_date - timedelta(days=date_ranges[date_range]) 

# ------------- Load network data -------------
def get_blockchaincom_data(url, col):
    data = requests.get(url).json()
    df = pd.DataFrame(data['values']).rename(columns={"x":"Date","y":col})
    df['Date'] = pd.to_datetime(df['Date'], unit='s')
    df = df.sort_values(by="Date", ascending=False)
    return df 

@st.cache_data
def load_chart_data():
    # Get historical BTC address data from Blockchain.com
    addr_url = 'https://api.blockchain.info/charts/n-unique-addresses?timespan=all&format=json'
    addr_df = get_blockchaincom_data(addr_url, "Addresses")

    # Get historical BTC transaction data from Blockchain.com
    tx_url = 'https://api.blockchain.info/charts/n-transactions?timespan=all&format=json'
    tx_df = get_blockchaincom_data(tx_url, "Transactions")


    # Get historical BTC hash rate data from Blockchain.com
    hs_url = 'https://api.blockchain.info/charts/hash-rate?timespan=all&format=json'
    hs_df = get_blockchaincom_data(hs_url, "Hash")

    return addr_df, tx_df, hs_df

addr_df, tx_df, hash_df = load_chart_data()
addr_df = addr_df.loc[(addr_df['Date'] >= pd.Timestamp(start_date)) & (addr_df['Date'] <= pd.Timestamp(end_date))]
tx_df = tx_df.loc[(tx_df['Date'] >= pd.Timestamp(start_date)) & (tx_df['Date'] <= pd.Timestamp(end_date))]
hash_df = hash_df.loc[(hash_df['Date'] >= pd.Timestamp(start_date)) & (hash_df['Date'] <= pd.Timestamp(end_date))]


# ------------- Display network data in charts -------------
col1, col2 = st.columns(2)
# Create a line chart of hash rate
with col1:
    chart_hash = px.line(hash_df, x='Date', y='Hash', title='Hash rate totale', color_discrete_sequence=['#071CD8'])
    chart_hash.update_layout(yaxis_title='Hash rate Hash/s')
    st.plotly_chart(chart_hash, use_container_width=True)
# Create some other values
with col2:
    # metric for current hashrate
    current_hash = round(hash_df.iloc[0]['Hash']/10**9, 2)
    delta = round((hash_df.iloc[0]['Hash'] - hash_df.iloc[1]['Hash'])/10**9, 2)
    col2.metric(label="Hash rate attuale", value=f'{current_hash} TH/s', delta=f'{delta} TH/s')
    # metric for lastest block time
    last = requests.get('https://blockchain.info/latestblock').json()
    time_diff = datetime.now() - datetime.fromtimestamp(last['time'])
    col2.metric(label="Ultimo blocco minato ", value=f'{time_diff.seconds//60} minuti e {time_diff.seconds%60} seccondi fa')


col1, col2 = st.columns(2)
# Create a line chart of daily addresses
with col1:
    chart_txn = px.line(tx_df, x='Date', y='Transactions', title='Transazioni giornaliere', color_discrete_sequence=['#F7931A'])
    chart_txn.update_layout(yaxis_title='Transactions')
    st.plotly_chart(chart_txn, use_container_width=True)
# Create a line chart of daily transactions
with col2:
    chart_addr = px.line(addr_df, x='Date', y='Addresses', title='Indirizzi attivi giornalieri', color_discrete_sequence=['#F7931A'])
    chart_addr.update_layout(yaxis_title='Active Addresses')
    st.plotly_chart(chart_addr, use_container_width=True)

st.write("Fonte: https://www.blockchain.com/charts")