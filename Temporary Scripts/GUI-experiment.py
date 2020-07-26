import tkinter as tk

mainWindow = tk.Tk()
mainWindow.geometry('360x480')
mainWindow.title('Synthesizer')

variable = tk.StringVar()
variable.set(None)
values = ['EUR', 'GBP', 'NZD', 'AUD']

dropDown = tk.OptionMenu(mainWindow, variable, *values)

dropDown.pack()

mainWindow.mainloop()

print(variable.get())