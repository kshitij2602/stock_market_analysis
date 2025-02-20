import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Define multiple stocks tickers
tickers = ["AAPL", "MSFT","GOOGL", "TSLA", "AMZN"]
start_date="2020-01-01"
end_date="2024-02-10"

#Create an empty dictionary to store Data
stock_data={}
# Loop throuigh each stock and fetch data
for ticker in tickers:
    stock_data[ticker]=yf.download(ticker, start=start_date,end=end_date)

#convert dictionary to a multi-index dataframe
df=pd.concat(stock_data, axis=1)

#Display the first 5 rows of the dataframe
# print(df.head())

# Cleaning and structuring the Data
df.reset_index(inplace=True)
#Flatten multi-index column names
df.columns= ['_'.join(col).strip() if isinstance(col, tuple)else col for col in df.columns]

#Rename Date_ to Date
df.rename(columns={'Date__':'Date'}, inplace=True)
# Display the cleaned Data

print(df.head())

#Check for missing values 
print(df.isnull().sum())
# Fill missing values using the recommended ffill() method
df.ffill(inplace=True)

#plt.style.use('seaborn-darkgrid')



# Plot Adjusted Close Prices for each stock
plt.figure(figsize=(12, 6))
for ticker in ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]:
    plt.plot(df["Date"], df[f"{ticker}_Close_{ticker}"], label=ticker)

plt.xlabel("Date")
plt.ylabel("Stock Price (USD)")
plt.title("Stock Price Trends (2020-2024)")
plt.legend()
plt.show()

#Calculate Daily Return
for ticker in ["AAPL","MSFT","GOOGL","TSLA","AMZN"]:
    df[f"Daily Return_{ticker}"]=df[f"{ticker}_Close_{ticker}"].pct_change()

#Display first few rows
print(df.head())

plt.figure(figsize=(12,6))
for ticker in ["AAPL","MSFT","GOOGL","TSLA","AMZN"]:
    sns.kdeplot(df[f"Daily Return_{ticker}"].dropna(), label=ticker, fill=True)

plt.xlabel("Daily Return")
plt.ylabel("Density")
plt.title("Stock Return Distributions")
plt.legend()
plt.show()

# Lets analyze how stock stock move together using  correlation Heatmap

# Create a DataFrame of only daily returns

returns_df=df[[f"Daily Return_{ticker}" for ticker in tickers]]

#compute correlation matrix 
corr_matrix= returns_df.corr()
# Plot heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Stock Returns Correlation Matrix")
plt.show()

# Define a rolling window size 
window_size = 30 #30 days

# Calculate rolling standard deviation ( volatility) for each stock 

for ticker in tickers :
    df[f"{ticker}_Volatility"]=df[f"{ticker}_Close_{ticker}"].pct_change().rolling(window = window_size).std()

#Plot rolling volatility 
plt.figure(figsize=(12,6))
for ticker in tickers :
    plt.plot(df['Date'],df[f"{ticker}_Volatility"], label=f"{ticker} Volatility")

plt.xlabel('Date')
plt.ylabel("Rolling Volatility (30-day)")
plt.title("Stock price Volatility ( 30-day Rolling Standard Deviation)")
plt.legend()
plt.show()

