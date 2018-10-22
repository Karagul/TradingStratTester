# Trading Simulator tool

This tool provides a simple way to test different trading strategies on historical data sets. The original intention for the code is to be hooked directly to the Bloomberg API, but it can be run using two excel files called *curr_time_series.xlsx* and *index_time_series.xlsx*. These files are not provided.

#### Caveat: This tool is written for Python for 3.4 and PyQT4. Please check for the PyQT5 branch for a more modern (and sligtly broken) version. All screenshots are taken from the unfinished PyQT5 version.

![alt text](https://i.imgur.com/pJIe4mC.png)



### Using the tool

This tools allows you to visualise different trading strategies. Start by choosing a curency (default is USD) and a the price time series of a financial instrument. In the screenshot above MSCI ACWI in USD is chosen. 










### Adding your own strategies

Adding a new strategy to the tool is very simple. The modules.py contains the different trading strategies.
