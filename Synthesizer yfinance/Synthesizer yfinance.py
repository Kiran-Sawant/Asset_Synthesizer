import tkinter as tk
from tkinter import ttk
import tkcalendar as tcal
import pandas as pd
import finplot as fplt
import yfinance as yf
import datetime as dt

pd.set_option('precision', 3)

denomination_dict = {'USD':'USD', 'EUR': 'EURUSD=X','GBP': 'GBPUSD=X', 'AUD': 'AUDUSD=X', 'NZD':'NZDUSD=X',
                        'JPY': 'JPY=X', 'INR':'INR=X', 'SGD':'SGD=X', 'ZAR':'ZAR=X', 'RUB':'RUB=X',
                        'NOK':'USDNOK=X', 'SEK':'SEK=X', 'CHF':'CHF=X', 'TRY':'TRY=X', 'AED':'AED=X',
                        'CNH':'CNH=X', 'BRL':'BRL=X', 'CAD':'CAD=X', 'BTC':'BTC-USD', 'ETH':'ETH-USD',}

#_____________Tk functions______________#
def errorBox():
    """Error dialog for empty symbol-box"""
    top = tk.Toplevel(mainWindow)
    top.title('ERROR')
    top.geometry('170x80')
    label = tk.Label(top, text='symbol not entered!').pack(pady=10)
    btn = ttk.Button(top, text='ok', command=lambda: top.destroy()).pack(pady=5)

def errorBox2():
    """Error dialog for wrong symbol input"""
    top = tk.Toplevel(mainWindow)   
    top.title('ERROR')
    top.geometry('170x80')
    label = ttk.Label(top, text='Invalid Symbol!').pack(pady=10)
    btn = ttk.Button(top, text='Got it', command=lambda: top.destroy()).pack(pady=5)

#____________Core Functions________________#
def dollarPair(currency: str) -> str:

    if currency in ['EUR', 'GBP', 'AUD', 'NZD', 'BTC', 'ETH']:
        return currency + 'USD'
    else:
        return 'USD' + currency

def dollarizer(df, dollarpair: str, start, end, interval: int):
    """Takes OCHL Dataframe of a non-dollar asset and returns its dollarised price."""
    
    base = df
    usd_crosser = dollarpair + '=X'
    crosser_ticker = yf.Ticker(usd_crosser)
    crosser_history = crosser_ticker.history(start=start, end=end, interval=interval).drop(columns=['Dividends', 'Stock Splits', 'Volume'])

    if dollarpair[3:6] == 'USD':                # if crosser is dollar quoted (eg. GBPUSD for FTSE100)
        dollarised_base = base[['Open', 'High', 'Low', 'Close']] * crosser_history[['Open', 'High', 'Low', 'Close']]
    else:                                       # if crosser is dollar based (eg. USDINR for SENSEX)
        dollarised_base = base[['Open', 'High', 'Low', 'Close']] / crosser_history[['Open', 'High', 'Low', 'Close']]
        dollarised_base.rename(columns={'high': 'low', 'low': 'high'})
    
    return dollarised_base


def synthesize(base, quote, start, end, interval):
    """Creates a Dataframe of passed Base against selected quote."""
    # Base
    base_ticker = yf.Ticker(base)
    base_denomination = base_ticker.info['currency']

    # Quote
    quote_crosser = dollarPair(quote)       # USD converting for that currency, eg. AUDUSD for AUD
    quote_symbol = denomination_dict[quote]
    quote_ticker = yf.Ticker(quote_symbol)

    base_history = base_ticker.history(start=start, end=end, interval=interval).drop(columns=['Dividends', 'Stock Splits', 'Volume'])
    quote_history = quote_ticker.history(start=start, end=end, interval=interval).drop(columns=['Dividends', 'Stock Splits', 'Volume'])

    if base_denomination == 'USD':              # if base is USD denominated (eg. SnP500, BTCUSD, etc).
        if quote_crosser[3:6] == 'USD':         # if quotes USD crosser is USD quoted (eg. AUDUSD).
            synthetic = base_history[['Open', 'High', 'Low', 'Close']] / quote_history[['Open', 'High', 'Low', 'Close']]
            synthetic.rename(columns={'High':'Low', 'Low':'High'}, inplace=True)
        else:                                   # if quotes USD crosser is USD Based (eg. USDJPY).
            synthetic = base_history[['Open', 'High', 'Low', 'Close']] * quote_history[['Open', 'High', 'Low', 'Close']]
    else:                                       # If base is non-USD denomination (eg. Nikki, FTSE100, etc.)
        dollarised_base = dollarizer(base_history, dollarPair(base_denomination), start, end, interval)

        if quote_symbol == 'USD':
            synthetic = dollarised_base
        elif quote_crosser[3:6] == 'USD':         # if quotes USD crosser is USD quoted (eg. AUDUSD).
            synthetic = dollarised_base[['Open', 'High', 'Low', 'Close']] / quote_history[['Open', 'High', 'Low', 'Close']]
            synthetic.rename(columns={'High':'Low', 'Low':'High'}, inplace=True)
        else:                                   # if quotes USD crosser is USD Based (eg. USDJPY).
            synthetic = dollarised_base[['Open', 'High', 'Low', 'Close']] * quote_history[['Open', 'High', 'Low', 'Close']]

    # base_history = base_ticker.history(start=start, end=end, interval=interval)
    # quote_history = quote_ticker.history(start=start, end=end, interval=interval)

    return synthetic



def plotter():
    """Takes the input value from widgets and creates a candlestick plot."""

    base = (symbolVar.get()).upper()
    quote = quoteCurrency.get()
    start_date = startDateCal.get_date()
    end_date = endDateCal.get_date()
    interval = intervalVar.get()

    #______If no symbol entered_______#
    if len(base) == 0:
        errorBox()
        return None
    else:
        pass

    base_ticker = yf.Ticker(base)

    #_____If symbol is invalid________#
    try:
        base_currency = base_ticker.info['currency']
    except ImportError:
        errorBox2()
        return None
    else:
        pass

    if quote == 'Select' or quote == base_currency:                             # No currency is selected or base denomination = selected currency.
        base_ticker = yf.Ticker(base)
        base_quote = base_ticker.history(start=start_date, end=end_date, interval=interval).drop(columns=['Dividends', 'Stock Splits', 'Volume'])
    else:                                                                       # A currency is selected.
        base_quote = synthesize(base, quote, start_date, end_date, interval)
    
    base_quote.dropna(inplace=True)

    # print(base_quote)
    # Calculating Simple Moving averages
    base_quote['SMA 1'] = base_quote['Close'].rolling(sma1Var.get()).mean()
    base_quote['SMA 2'] = base_quote['Close'].rolling(sma2Var.get()).mean()

    # print(base_quote)
    # Calculating Standard-deviation.
    base_quote['pct_change'] = base_quote['Close'].pct_change() * 100
    base_quote['std-dev'] = base_quote['pct_change'].rolling(stdDevVar.get()).std()
    # print(base_quote)

    candle_stick_data = fplt.PandasDataSource(base_quote[['Open', 'Close', 'High', 'Low']])
    ax, ax2 = fplt.create_plot(title=f"{base}/{quote}", rows=2)
    candle_plot = fplt.candlestick_ochl(candle_stick_data, ax=ax)

    # Plotting SMAs
    sma1 = fplt.plot(base_quote['SMA 1'], legend=f'{sma1Var.get()} SMA', ax=ax)
    sma2 = fplt.plot(base_quote['SMA 2'], legend=f'{sma2Var.get()} SMA', ax=ax)
    # Ploting StdDev
    stdDevPlot = fplt.plot(base_quote['std-dev'], legend=f'{stdDevVar.get()} period std-dev', ax=ax2)
    fplt.add_text(pos=(base_quote.index[-1], base_quote['std-dev'].iloc[-1]), s=f"{base_quote['std-dev'].iloc[-1].round(2)}%", ax=ax2)

    fplt.show()


#_________________Tk GUI_____________________#
mainWindow = tk.Tk()
mainWindow.geometry('440x240')
mainWindow.title('Synthesizer Y-Finance (Beta)')

#___________________Tk variables_______________________#
symbolVar = tk.StringVar(mainWindow)
quoteCurrency = tk.StringVar(mainWindow)
intervalVar = tk.StringVar(mainWindow)

sma1Var = tk.IntVar()
sma2Var = tk.IntVar()
stdDevVar = tk.IntVar()

#___________________Creating Widgets____________________#
# symbol Entrybox
symbolBoxLabel = tk.Label(mainWindow, text='Enter Symbol as in Yahoo Finance: ')
symbolBox = ttk.Entry(mainWindow, textvariable=symbolVar)
# Quote
quoteLabel = tk.Label(mainWindow, text='Select Currency: ')
quoteList = ttk.OptionMenu(mainWindow, quoteCurrency, 'Select', *[i for i in denomination_dict])
# Dates
startDateLabel = ttk.Label(mainWindow, text='Start: ')
startDateCal = tcal.DateEntry(mainWindow, background='darkblue', borderwidth=2, month=1, width=8)
endDateLabel = ttk.Label(mainWindow, text='End: ')
endDateCal = tcal.DateEntry(mainWindow, background='darkblue', borderwidth=2, maxdate=dt.date.today(), width=8)
# Interval
intervalLabel = ttk.Label(mainWindow, text='Select Interval: ')
intervalMenu = ttk.OptionMenu(mainWindow, intervalVar, '1d', *['1h', '1d', '1wk', '1mo', '3mo'])
# Plot Button
trigger = ttk.Button(mainWindow, text='Synthesize', command=plotter)
# SMAs
sma1Label = ttk.Label(mainWindow, text='SMA 1: ' )
sma2Label = ttk.Label(mainWindow, text='SMA 2: ' )
sma1Entry = ttk.Entry(mainWindow, textvariable=sma1Var, width=5)
sma2Entry = ttk.Entry(mainWindow, textvariable=sma2Var, width=5)
# Standard Deviation
stdDevLabel = ttk.Label(mainWindow, text='Std Dev: ')
stdDevEntry = ttk.Entry(mainWindow, textvariable=stdDevVar, width=5)
#______Configuring widgets____#


#__________________Placing Widgets____________________#
symbolBoxLabel.grid(row=0, column=0, columnspan=2)
symbolBox.grid(row=1, column=0, sticky='ew', columnspan=4)

quoteLabel.grid(row=0, column=4, columnspan=2, sticky='w', padx=20)
quoteList.grid(row=1, column=4, columnspan=2, sticky='w', padx=20)

startDateLabel.grid(row=2, column=0, sticky='e', pady=5)
startDateCal.grid(row=2, column=1, sticky='w', pady=5)
endDateLabel.grid(row=2, column=2, sticky='e', pady=5)
endDateCal.grid(row=2, column=3, sticky='w', pady=5)

intervalLabel.grid(row=3, column=0, sticky='e', pady=5)
intervalMenu.grid(row=3, column=1, sticky='w', pady=5)

sma1Label.grid(row=4, column=0, sticky='e')
sma1Entry.grid(row=4, column=1)

sma2Label.grid(row=5, column=0, sticky='e', pady=3)
sma2Entry.grid(row=5, column=1, pady=3)

stdDevLabel.grid(row=6, column=0, sticky='e', pady=3)
stdDevEntry.grid(row=6, column=1, pady=3)

trigger.grid(row=7, column=0, padx=5, pady=10)

mainWindow.mainloop()