"""Works only with currencies."""

import MetaTrader5 as mt5
import pandas as pd
import finplot as fplt
import time
import tkinter as tk

asset_dict = {'Euro': 'EURUSD', 'British Pound': 'GBPUSD', 'Aussie Dollar': 'AUDUSD', 'Kiwi Dollar': 'NZDUSD',
              'Japanese Yen': 'USDJPY', 'Swiss Frank': 'USDCHF', 'Canadien Dollar': 'USDCAD', 'Swedish Krona': 'USDSEK',
              'Norwegian Krone': 'USDNOK', 'Danish Krone': 'USDDKK', 'Sing Dollar': 'USDSGD', 'Hong-Kong $': 'USDHKD',
              'Chinese Renminbi': 'USDCNH', 'Thai Baht': 'USDTHB', 'Turkish Lira': 'USDTRY', 'Mexican Peso': 'USDMXN',
              'Russian Rubles': 'USDRUB', 'Czech Koruna': 'USDCZK', 'Polish Zloty': 'USDPLN', 'Hungarian Forint': 'USDHUF',
              'South-African Rand': 'USDZAR',
              'Gold': 'XAUUSD', 'Silver': 'XAGUSD', 'Platinum': 'XPTSUD', 'Paladium': 'XPDUSD',
              'Brent': 'XBRUSD', 'WTI': 'XTIUSD', 'Nat-Gas': 'XNGUSD',
              'S&P-500': 'US500', 'Dow-Jones': 'US30', 'NASDAQ': 'USTEC', 'Russel-2000': 'US2000', 'CA60': 'CA60',
              'DAX': 'DE30', 'M-DAX': 'MidDE60', 'Tec-DAX': 'TecDE30', 'Eu-Stoxx 50': 'STOXX50',
              'F40': 'F40', 'IBEX': 'ES35', 'MIB': 'IT40', 'NETH25': 'NETH25',
              'Footsie': 'UK100', 'Swiss Market Index': 'SWI20', 'NOR25': 'NOR25', 'SE30': 'SE30',
              'AUS200': 'AUS200', 'Nikki': 'JP225', 'CHINA50': 'CHINA50', 'Hang Seng': 'HK50',
              'CHINAH': 'CHINAH', 'SA40': 'SA40'}

denomination_dict ={'None': None, 'EUR': 'EURUSD', 'GBP': 'GBPUSD', 'AUD': 'AUDUSD', 'NZD': 'NZDUSD',
                    'JPY': 'USDJPY', 'CHF': 'USDCHF', 'CAD': 'USDCAD', 'SEK': 'USDSEK',
                    'NOK': 'USDNOK', 'DKK': 'USDDKK', 'SGD': 'USDSGD', 'HKD': 'USDHKD',
                    'CNH': 'USDCNH', 'THB': 'USDTHB', 'TRY': 'USDTRY', 'MXN': 'USDMXN',
                    'RUB': 'USDRUB', 'CZK': 'USDCZK', 'PLN': 'USDPLN', 'HUF': 'USDHUF',
                    'ZAR': 'USDZAR'}


def dollarPair(currency: str):
    if currency in ['EUR', 'GBP', 'AUD', 'NZD']:
        return currency + 'USD'
    else:
        return 'USD' + currency


def dollarizer(asset, dollarpair, period):

    mt5.symbol_select(dollarpair)
    time.sleep(2)
    
    asset_rates = pd.DataFrame(mt5.copy_rates_from_pos(asset, mt5.TIMEFRAME_H1, 0, period)).drop(columns=['spread', 'real_volume'])
    dollar_rates = pd.DataFrame(mt5.copy_rates_from_pos(dollarpair, mt5.TIMEFRAME_H1, 0, period)).drop(columns=['spread', 'real_volume'])
        
    asset_rates['time'] = pd.to_datetime(asset_rates['time'], unit='s')
    dollar_rates['time'] = pd.to_datetime(dollar_rates['time'], unit='s')

    asset_rates.set_index(keys=['time'], inplace=True)
    dollar_rates.set_index(keys=['time'], inplace=True)
    
    if dollarpair[3:6] == 'USD':     # quoted in dollar
        dollarised_asset = asset_rates[['open', 'high', 'low', 'close']] * dollar_rates[['open', 'high', 'low', 'close']]
    
    else:                             # based in dollar
        dollarised_asset = asset_rates[['open', 'high', 'low', 'close']] / dollar_rates[['open', 'high', 'low', 'close']]
        dollarised_asset.rename(columns={'high': 'low', 'low': 'high'})
    
    # dollarised_asset['vol'] = (asset_rates['tick_volume'] + dollar_rates['tick_volume']) / 2
    return dollarised_asset


def synthesize(symbol1, symbol2, period):
    """Takes 2 MT5 currency symbols with common USD and returns a DataFrame of OCHLV
    of the price of first symbol denominated in second symbol.
    
    note: Requires both the assets to have USD in common, ie. either denomination
    or base."""

    mt5.symbol_select(symbol1)
    mt5.symbol_select(symbol2)
    time.sleep(2)

    # Asset on which the pricing will be based.
    base_asset = pd.DataFrame(mt5.copy_rates_from_pos(symbol1, mt5.TIMEFRAME_H1, 1, period)).drop(columns=['spread', 'real_volume'])
    # Asset to quote the base in, generally a currency.
    quote_asset = pd.DataFrame(mt5.copy_rates_from_pos(symbol2, mt5.TIMEFRAME_H1, 1, period)).drop(columns=['spread', 'real_volume'])

    # converting timestamps to Datetime-index.
    base_asset['time'] = pd.to_datetime(base_asset['time'], unit='s')
    quote_asset['time'] = pd.to_datetime(quote_asset['time'], unit='s')

    base_asset.set_index(keys=['time'], inplace=True)
    quote_asset.set_index(keys=['time'], inplace=True)

    baseAsset_quote = mt5.symbol_info(symbol1).currency_profit

    if symbol1[0:3] == 'USD':                       # Dollar based ie. USDJPY, USDCHF...
        if symbol2[3:6] == 'USD':
            basequote = (1/ base_asset[['open', 'high', 'low', 'close']]) * (1/ quote_asset[['open', 'high', 'low', 'close']])
            basequote.rename(columns={'high':'low', 'low':'high'}, inplace=True)
        else:
            # basequote = quote_asset[['open', 'high', 'low', 'close']] / base_asset[['open', 'high', 'low', 'close']]
            basequote = (1/ base_asset[['open', 'high', 'low', 'close']]) * quote_asset[['open', 'high', 'low', 'close']]
            basequote.rename(columns={'high':'low', 'low':'high'}, inplace=True)
    
    elif symbol1[3:6] == 'USD' or baseAsset_quote == 'USD':  # Dollar quoted ie. EURUSD, SnP500...
        if symbol2[3:6] == 'USD':
            basequote = base_asset[['open', 'high', 'low', 'close']] / quote_asset[['open', 'high', 'low', 'close']]
            # basequote.rename(columns={'high':'low', 'low':'high'}, inplace=True)
        else:
            basequote = base_asset[['open', 'high', 'low', 'close']] * quote_asset[['open', 'high', 'low', 'close']]
    
    else:
        dollarisedAsset = dollarizer(symbol1, dollarPair(baseAsset_quote), period)

        if symbol2[3:6] == 'USD':
            basequote =  dollarisedAsset[['open', 'high', 'low', 'close']] / quote_asset[['open', 'high', 'low', 'close']]
        else:
            basequote = dollarisedAsset[['open', 'high', 'low', 'close']] * quote_asset[['open', 'high', 'low', 'close']]

    return basequote


def plotter():

    # getting the selections
    selection = assetListBox.curselection()[0]
    asset = asset_dict[assetListBox.get(selection)]
    currency = denomination_dict[opMenuVar.get()]
    periods = periodEntryVar.get()

    if currency is None:        # No currency is selected.
        synthetic_asset = pd.DataFrame(mt5.copy_rates_from_pos(asset, mt5.TIMEFRAME_H1, 1, periods)).drop(columns=['spread', 'real_volume'])
        synthetic_asset['time'] = pd.to_datetime(synthetic_asset['time'], unit='s')
        synthetic_asset.set_index(keys=['time'], inplace=True)
    else:
        synthetic_asset = synthesize(asset, currency, periods)
    
    synthetic_asset.dropna(inplace=True)

    # Calculaating Simple Moving averages
    synthetic_asset['SMA 1'] = synthetic_asset['close'].rolling(sma1boxVar.get()).mean()
    synthetic_asset['SMA 2'] = synthetic_asset['close'].rolling(sma2boxVar.get()).mean()
    # Calculating Standard-deviation.
    synthetic_asset['pct_change'] = synthetic_asset['close'].pct_change() * 100
    synthetic_asset['std-dev'] = synthetic_asset['pct_change'].ewm(stddevVar.get()).std()

    candle_stick_data = fplt.PandasDataSource(synthetic_asset[['open', 'close', 'high', 'low']])
    ax, ax2 = fplt.create_plot(title=f'{asset}/{currency}', rows=2)
    candle_plot = fplt.candlestick_ochl(candle_stick_data, ax=ax)

    # Plotting SMAs
    sma1 = fplt.plot(synthetic_asset['SMA 1'], legend=f'{sma1boxVar.get()} SMA', ax=ax)
    sma2 = fplt.plot(synthetic_asset['SMA 2'], legend=f'{sma2boxVar.get()} SMA', ax=ax)
    # Plotting Std-dev
    stdDevPlot = fplt.plot(synthetic_asset['std-dev'], legend=f'Std Dev {stddevVar.get()}', ax=ax2)
    fplt.add_text(pos=(synthetic_asset.index[-1], synthetic_asset['std-dev'].iloc[-1]), s=f"{synthetic_asset['std-dev'].iloc[-1].round(3)}", ax=ax2)

    fplt.show()

# Initializing MT5 terminal.
mt5.initialize()

# Initializing Tk window.
mainWindow = tk.Tk()
mainWindow.geometry('390x370')
mainWindow.title('Synthesizer')

#________GUI Variables________#
listBox1Var = tk.Variable(mainWindow)
listBox1Var.set(list(asset_dict.keys()))

opMenuVar = tk.Variable(mainWindow)
opMenuVar.set(None)

periodEntryVar = tk.IntVar(mainWindow, value=120)

sma1boxVar = tk.IntVar(mainWindow, value=8)
sma2boxVar = tk.IntVar(mainWindow, value=24)

stddevVar = tk.IntVar(mainWindow, value=12)

#___________Creating widgets___________#
# asset list
assetlistlabel = tk.Label(mainWindow, text='Assets :')
assetListBox = tk.Listbox(mainWindow, listvariable=listBox1Var)
scroll1 = tk.Scrollbar(mainWindow, orient=tk.VERTICAL, command=assetListBox.yview)
assetListBox['yscrollcommand'] = scroll1.set
# denomination currency drop-down
denoLable = tk.Label(mainWindow, text='Currencies :')
denoDropdown = tk.OptionMenu(mainWindow, opMenuVar, *list(denomination_dict.keys()))
# period entry box
periodlabel = tk.Label(mainWindow, text='Period (hrs) : ')
periodentry = tk.Entry(mainWindow, textvariable=periodEntryVar)
# SMA labels & entry boxes
sma1Label = tk.Label(mainWindow, text='SMA-1 period: ')
sma2Label = tk.Label(mainWindow, text='SMA-2 period: ')
sma1Box = tk.Entry(mainWindow, textvariable=sma1boxVar)
sma2Box = tk.Entry(mainWindow, textvariable=sma2boxVar)
# std-dev label & entry-box
stddevLabel = tk.Label(mainWindow, text='std-dev period: ')
stddevBox = tk.Entry(mainWindow, textvariable=stddevVar)
# Plot button
button = tk.Button(mainWindow, text='Plot', command=plotter)

#__________placing widgets___________#
# asset list
assetlistlabel.grid(row=0, column=0, sticky='w', padx=4)
assetListBox.grid(row=1, column=0, rowspan=8, sticky='nsw', padx=4)
scroll1.grid(row=1, column=1, rowspan=8, sticky='nsw')
# denomination drop-down
denoLable.grid(row=1, column=2, sticky='nw', padx=4)
denoDropdown.grid(row=1, column=3, sticky='nw')
# period entry-box
periodlabel.grid(row=2, column=2, sticky='nw', padx=4)
periodentry.grid(row=2, column=3, sticky='nw', padx=0)
# SMA labels & entry-boxes
sma1Label.grid(row=3, column=2, sticky='nw', padx=4)
sma2Label.grid(row=4, column=2, sticky='nw', padx=4)
sma1Box.grid(row=3, column=3, sticky='nw')
sma2Box.grid(row=4, column=3, sticky='nw')
# std-devs
stddevLabel.grid(row=5, column=2, sticky='nw')
stddevBox.grid(row=5, column=3, sticky='nw')
# button
button.grid(row=8, column=2, sticky='ew', padx=4)

#__________cofiguring widgets__________#
assetListBox.config(width=20, height=20)
button.config(activebackground='green', activeforeground='white')

# volume = fplt.PandasDataSource(synthetic_asset[['open', 'close', 'vol']])
# axo = ax.overlay()
# volume_olay = fplt.volume_ocv(volume, ax=axo)
mainWindow.mainloop()
mt5.shutdown()