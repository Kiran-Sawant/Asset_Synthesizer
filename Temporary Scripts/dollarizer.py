import MetaTrader5 as mt5
import pandas as pd
import finplot as fplt
import time

mt5.initialize()

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

dollaried_dax = dollarizer('DE30', dollarPair(mt5.symbol_info('DE30').currency_profit), 30)
print(dollaried_dax.round(3))
print('\n')
print(dollaried_dax.iloc[-1, 3])

mt5.shutdown()