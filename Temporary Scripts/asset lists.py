import tkinter as tk

asset_dict = {'Euro': 'EURUSD', 'British Pound': 'GBPUSD', 'AUD': 'AUDUSD', 'NZD': 'NZDUSD',
              'JPY': 'USDJPY', 'Swiss Frank': 'USDCHF', 'CAD': 'USDCAD', 'SEK': 'USDSEK',
              'NOK': 'USDNOK', 'DKK': 'USDDKK', 'SGD': 'USDSGD', 'HKD': 'USDHKD',
              'CNH': 'USDCNH', 'THB': 'USDTHB', 'TRY': 'USDTRY', 'MXN': 'USDMXN',
              'RUB': 'USDRUB', 'CZK': 'USDCZK', 'PLN': 'USDPLN', 'HUF': 'USDHUF',
              'ZAR': 'USDZAR',
              'Gold': 'XAUUSD', 'Silver': 'XAGUSD', 'Platinum': 'XPTSUD', 'Paladium': 'XPDUSD',
              'Brent': 'XBRUSD', 'WTI': 'XTIUSD', 'Nat-Gas': 'XNGUSD',
              'S&P-500': 'US500', 'Dow-Jones': 'US30', 'NASDAQ': 'USTEC', 'Russel-2000': 'US2000', 'CA60': 'CA60',
              'DAX': 'DE30', 'M-DAX': 'MidDE60', 'Tec-DAX': 'TecDE30', 'Eu-Stoxx 50': 'STOXX50',
              'F40': 'F40', 'IBEX': 'ES35', 'MIB': 'IT40', 'NETH25': 'NETH25',
              'Futsie': 'UK100', 'Swiss-20': 'SWI20', 'NOR25': 'NOR25', 'SE30': 'SE30',
              'AUS200': 'AUS200', 'Nikki': 'JP225', 'CHINA50': 'CHINA50', 'Heng Sheng': 'HK50',
              'CHINAH': 'CHINAH', 'SA40': 'SA40'}

denomination_dict ={'None': None, 'EUR': 'EURUSD', 'GBP': 'GBPUSD', 'AUD': 'AUDUSD', 'NZD': 'NZDUSD',
                    'JPY': 'USDJPY', 'CHF': 'USDCHF', 'CAD': 'USDCAD', 'SEK': 'USDSEK',
                    'NOK': 'USDNOK', 'DKK': 'USDDKK', 'SGD': 'USDSGD', 'HKD': 'USDHKD',
                    'CNH': 'USDCNH', 'THB': 'USDTHB', 'TRY': 'USDTRY', 'MXN': 'USDMXN',
                    'RUB': 'USDRUB', 'CZK': 'USDCZK', 'PLN': 'USDPLN', 'HUF': 'USDHUF',
                    'ZAR': 'USDZAR'}

def test():
    selection = assetListBox.curselection()[0]
    symbol = assetListBox.get(selection)
    # print(asset_dict[symbol])
    drop = opMenuVar.get()
    print(f"{asset_dict[symbol]}/{denomination_dict[drop]}")

# print(list(asset_dict.keys()))
mainWindow = tk.Tk()
mainWindow.geometry('390x370')
mainWindow.title('Synthesizer')

#________GUI Variables________#
listBox1Var = tk.Variable(mainWindow)
listBox1Var.set(list(asset_dict.keys()))

opMenuVar = tk.Variable(mainWindow)
opMenuVar.set(None)

periodEntryVar = tk.IntVar(mainWindow, value=240)

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
# Plot button
button = tk.Button(mainWindow, text='Plot', command=test)

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
# button
button.grid(row=8, column=2, sticky='ew', padx=4)

#__________cofiguring widgets__________#
assetListBox.config(width=20, height=20)
button.config(activebackground='green', activeforeground='white')

mainWindow.mainloop()