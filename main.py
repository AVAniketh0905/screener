import datetime
import yfinance as yf
import pandas as pd
import logging

logging.basicConfig(
    filename="log.txt", level=logging.INFO, format="%(asctime)s - %(message)s"
)


# Function to fetch stock data
def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period="2y")


# Function to calculate percentage away from 52-week high
def percentage_away_from_52w_high(stock_data):
    high_52w = stock_data["High"].max()
    last_close = stock_data["Close"].iloc[-1]
    return (high_52w - last_close) / high_52w * 100


# Function to calculate returns
def calculate_returns(stock_data, period_days):
    # Ensure the stock_data DataFrame has a DateTime index
    if not isinstance(stock_data.index, pd.DatetimeIndex):
        stock_data.index = pd.to_datetime(stock_data.index)

    # Sort the DataFrame by the index (date) to ensure proper order
    stock_data = stock_data.sort_index()

    # Determine the latest date and the date that is `period_days` ago
    latest_date = stock_data.index[-1]
    start_date = latest_date - pd.Timedelta(days=period_days)

    # Find the nearest available date within the DataFrame
    if start_date in stock_data.index:
        start_date_actual = start_date
    else:
        start_date_actual = stock_data.index.asof(start_date)

    # Check if the nearest date is within a 2-day range
    if abs((start_date_actual - start_date).days) <= 2:
        start_price = stock_data.loc[start_date_actual, "Close"]
        end_price = stock_data.loc[latest_date, "Close"]
        return (end_price - start_price) / start_price * 100

    return None


# Fetch the list of Nifty 200 stocks (example tickers)
nifty_200 = pd.read_csv("ind_nifty200list.csv")

symbols = nifty_200["Symbol"]

stocks_data = {}
for symbol in symbols:
    logging.info(f"Fetching data for {symbol}...")
    data = fetch_stock_data(f"{symbol}.NS")  # Appending ".NS" to fetch data from NSE
    if not data.empty:
        stocks_data[symbol] = data
        logging.info(f"Data for {symbol} fetched successfully.")
    else:
        logging.info(f"No data available for {symbol}.")

# Calculate percentage away from 52-week high and sort
stocks_info = []
for ticker, data in stocks_data.items():
    away_52w_high = percentage_away_from_52w_high(data)
    recent_price = data["Close"].iloc[-1]
    if recent_price > 5000:
        continue

    returns_6m = calculate_returns(data, 182)
    returns_1y = calculate_returns(data, 365)

    if returns_6m is not None and returns_1y is not None:
        if returns_6m > 0 and returns_1y > 20 and returns_1y > returns_6m:
            stocks_info.append(
                (ticker, away_52w_high, recent_price, returns_6m, returns_1y)
            )

stocks_info.sort(key=lambda x: x[1])
top_30_stocks = stocks_info[:30]

# Filter top n_stocks stocks meeting criteria
max_stocks = 10
selected_stocks = []
for stock in top_30_stocks:
    if len(selected_stocks) < max_stocks:
        # Check if the stock price hasn't closed at upper or lower circuit
        data = stocks_data[stock[0]]
        if not (
            (data["Close"] == data["High"]).any()
            or (data["Close"] == data["Low"]).any()
        ):
            selected_stocks.append(stock[0])

# Ensure the selected stocks were not shortlisted in the previous 5 months
shortlisted_stocks_last_5_months = []  # Load from your historical data
final_stocks = [
    stock for stock in selected_stocks if stock not in shortlisted_stocks_last_5_months
]

# Write the final stocks to results.txt
current_date = datetime.now().strftime("%d-%m-%Y")
with open("results.txt", "w") as f:
    f.write(f"Date: {current_date}\n")
    f.write("Buy the following stocks the next day:\n")
    for stock in final_stocks[:max_stocks]:
        f.write(f"{stock}\n")
