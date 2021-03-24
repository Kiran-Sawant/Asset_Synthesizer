# Asset_Synthesizer
The python app can take one asset(including other currencies) and a currency, the program will return a candlestick
plot of that asset denominated in the selected currency. The app requires an MT5 terminal running in the background.
Version-1 of the app is CLI based and Version-2 is GUI based.

## Synthesizer app interface
<img src='snippets/Interface.PNG'>
<br>
Select the security from the list-box, select the currency from the options-menu, insert the number of periods in hours.
You can optionally insert values for indicators like Simple Moving Average and standard Deviation.
<br>
The app uses <a href='https://github.com/highfestiva/finplot.git'>finplot</a> by <a href='https://github.com/highfestiva'>highfestiva</a>
for rendering the graph as shown below.
<br>
<br>
<img src='snippets/SnP 500 SEK.PNG'>
<br>
The above candlestick plot is of SnP500 emini futures denominated in Swedish Krona, with 24 & 8 period SMAs and standard deviation ploted
on a separate axis.
