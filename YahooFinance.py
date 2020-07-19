from yahooquery import Ticker
from typing import List

def getLatestPrice(stockTicker: str) -> str:
    ticker = Ticker(stockTicker)
    tickerInfo = ticker.price
    returnMessage = ''
    for symbol in tickerInfo.keys():
        info = tickerInfo[symbol]
        if type(info) == str or 'regularMarketPrice' not in info:
            returnMessage += 'Quote not found for ticker symbol: {}\n'.format(symbol.upper())
        else:
            name = info['longName']
            latestPrice = info['regularMarketPrice']
            updateTime = info['regularMarketTime']
            currency = info['currency']
            currencySymbol = info['currencySymbol']
            industry = ticker.summary_profile[symbol]['industry'] if 'industry' in ticker.summary_profile[symbol] else ''
            returnMessage += '{} : {}\nIndustry: {}\nPrice ({}): {}{}\nLast Updated (UTC): {}\n'.format(name, symbol.upper(), industry, currency, currencySymbol, latestPrice, updateTime)
    return returnMessage

def getPortfolio(stockTickers: List[str]):
    tickers = Ticker(stockTickers)
    tickerInfo = tickers.price
    returnMessage = 'Ticker\t Price\t\t As of(UTC)\n'
    for symbol in tickerInfo.keys():
        info = tickerInfo[symbol]
        if type(info) == str or 'regularMarketPrice' not in info:
            returnMessage += '{}\t {}\t {}\n'.format(symbol.upper(), "No price info", "N/A")
        else:
            name = info['longName']
            latestPrice = info['regularMarketPrice']
            updateTime = info['regularMarketTime']
            currency = info['currency']
            currencySymbol = info['currencySymbol']
            returnMessage += '{}\t {}{}\t {}\n'.format(symbol.upper(), currencySymbol, latestPrice, updateTime)
    return returnMessage