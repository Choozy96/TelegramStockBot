from yahooquery import Ticker

def getLatestPrice(stockTicker: str) -> str:
    ticker = Ticker(stockTicker)
    info = ticker.price[stockTicker]
    if 'regularMarketPrice' not in info:
        return "There is no price history for the symbol {}".format(stockTicker.upper())
    else:
        name = info['longName']
        latestPrice = info['regularMarketPrice']
        updateTime = info['regularMarketTime']
        currency = info['currency']
        industry = ticker.summary_profile[stockTicker]['industry']
        return '{} : {}\nIndustry: {}\nPrice: {}${}\nLast Updated: {}'.format(name, stockTicker.upper(), industry, currency, latestPrice, updateTime)