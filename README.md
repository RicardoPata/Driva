# Driva

This bot is looking for 2 chart patterns to apply a strategy

Once bot its running, first thing it does is extract btc OHLC values and transfers to a dataframe.
After 3 candles on the dataframe, bot can now start looking for pattern

Patter on uptrend will be : 1 red candle and 2 green candles. If this pattern is found, calculate percentual difference between lowest and highest point on that pattern, if its bigger than 1, looks for retracement, if retracement hits, set stop loss and target price . Send email once bet is on

This bot will use CCXT library to get live BTC/USD price

