import yfinance as yf

def getLatestPrice(stockTicker: str) -> str:
    ticker = yf.Ticker(stockTicker)
    priceHistory = ticker.history(period="1d")
    if len(priceHistory) == 0:
        return "There is no price history for the symbol {}".format(stockTicker)
    else:
        latestPrice = priceHistory.iloc[-1]['Close']
        name = ticker.info['longName']
        industry = ticker.info['industry']
        currency = ticker.info['currency']
        return ('{} : {}\nIndustry: {}\nPrice: {}${}'.format(name, stockTicker, industry, currency, latestPrice))