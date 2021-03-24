"""CLI version of synthesizer. Works with currencies only"""

import MetaTrader5 as mt5
import pandas as pd
import finplot as fplt

mt5.initialize()

def synthesize(symbol1, symbol2, periods):
    """Takes 2 MT5 currency symbols with common USD and returns a DataFrame of OCHLV
    of the price of first symbol denominated in second symbol.
    
    note: Requires both the assets to have USD in common, ie. either denomination
    or base."""

    # Asset on which the pricing will be based.
    base_asset = pd.DataFrame(mt5.copy_rates_from_pos(symbol1, mt5.TIMEFRAME_H1, 1, period))
    # Asset to quote the base in, generally a currency.
    quote_asset = pd.DataFrame(mt5.copy_rates_from_pos(symbol2, mt5.TIMEFRAME_H1, 1, period))

    # converting timestamps to Datetime-index.
    base_asset['time'] = pd.to_datetime(base_asset['time'], unit='s')
    quote_asset['time'] = pd.to_datetime(quote_asset['time'], unit='s')

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

    # averaging volume.
    basequote['vol'] = ((base_asset['tick_volume'] + quote_asset['tick_volume'])/2)
    basequote.set_index(keys=[base_asset['time']], inplace=True)

    return basequote

symbol1 = input('Enter base symbol: ').upper()
symbol2 = input('Enter quote symbol: ').upper()
period = int(input('Enter period in Hours: '))

synthetic_asset = synthesize(symbol1, symbol2, period)
print(synthetic_asset)

candle_stick_data = fplt.PandasDataSource(synthetic_asset[['open', 'close', 'high', 'low']])
volume = fplt.PandasDataSource(synthetic_asset[['open', 'close', 'vol']])

ax = fplt.create_plot(title=f'{symbol1}/{symbol2}', rows=1)
axo = ax.overlay()

candle_plot = fplt.candlestick_ochl(candle_stick_data, ax=ax)
volume_olay = fplt.volume_ocv(volume, ax=axo)

fplt.show()
mt5.shutdown()