import yfinance as yf

def getLatestPrice(stockTicker: str) -> int:
    ticker = yf.Ticker(stockTicker)
    priceHistory = ticker.history(period="1d")
    latestPrice = priceHistory.iloc[-1]['Close']
    print(latestPrice)
    return latestPrice

if __name__ == "__main__":
    getLatestPrice("msft")
