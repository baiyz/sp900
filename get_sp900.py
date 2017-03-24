#!/usr/bin/env python

import time
import json
from finsymbols import symbols
from googlefinance import getQuotes
from yahoo_finance import Share

DEBUG = False

sp500 = symbols.get_sp500_symbols()
sp400 = symbols.get_sp400_symbols()
sp900 = sp500 + sp400

google_bad_list = ['APH', 'LMT']

sp900_all = {}
sp900_chg = {}
for stock in sp900:
    print stock['symbol']
    try:
        if stock['symbol'] not in google_bad_list and '.' in stock['symbol']:
            equity_parsed = getQuotes(stock['symbol'])[0]
            sp900_all[stock['symbol']] = float(equity_parsed['ChangePercent'])
            print float(equity_parsed['ChangePercent'])
            if DEBUG:
                print "{}\t{}\t{}\t{}%".format(stock['symbol'], stock['company'], equity_parsed['LastTradePrice'], equity_parsed['ChangePercent'])
        else:
            equity = Share(stock['symbol'])
            sp900_all[stock['symbol']] = float(equity.get_percent_change().strip('%'))/100
            print float(equity.get_percent_change().strip('%'))/100
            if DEBUG:
                print "{}\t{}\t{}\t{}".format(stock['symbol'], equity.get_name(), equity.get_price(), equity.get_percent_change())
    except:
        pass

for ticker in sp900_all:
    if sp900_all[ticker] > 0.03 or sp900_all[ticker] < -0.03:
        sp900_chg[ticker] = sp900_all[ticker]

with open('result/SP900_{}.txt'.format(time.strftime("%Y%m%d%H%M%S")), 'w') as fd:
    tab = ''
    for ticker in sp900_chg:
        if '.' not in ticker:
            tab += "{}\t{}\n".format(ticker, sp900_chg[ticker]*100)
    fd.write(tab)
