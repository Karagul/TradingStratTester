# Trading Simulator tool

This tool provides a simple way to test different trading strategies on historical data sets. The original intention for the code is to be hooked directly to the Bloomberg API, but it can be run using two excel files called *curr_time_series.xlsx* and *index_time_series.xlsx*. These files are not provided.

#### Caveat: This tool is written for Python for 3.4 and PyQT4. Please check for the PyQT5 branch for a more modern (and sligtly broken) version. All screenshots are taken from the unfinished PyQT5 version.

![alt text](https://i.imgur.com/pJIe4mC.png)



### Using the tool

This tools allows you to visualise different trading strategies. Start by choosing a curency (default is USD) and a the price time series of a financial instrument. In the screenshot above MSCI ACWI in USD is chosen. 

###### Strategies
The next step now is to choose a trading strategy. There are six* different strategies to choose from:
* Golden Cross (trade when an X day moving average crosses the 50 day moving avarge).
* Moving Average (trade when an X day moving average crosses px).
* Derivative (a variation of the Moving Average strategy which also sends a buy signal when the derivative of the moving average is positive).
* Mean Reversal (trade when the X day moving average moves Y standard deviations).

X and Y represent user input above.

A strategy will always start trading from 100 by design. (This shows the performance loss/gain of not immediatly investing and instead waiting for the first signal).

By changing currency, one can compare the performace of the same strategy 





All strategies have a two day delay built in. What this means is that a trade won't be executed until 2 days after the buy/sell signal to simulate realistic conditions. This can be changed by changing the "delay" variable in modules.py in the functions "simulator" adn "simulator_error_check". This part of the code lacks good documentation and comments (will hopefuly change when I have time), so tread lightly.

\*The buttons which say "IMPLEMENT STRATEGY" ("LEMENT STR in PyQT5...") are strategies which have been redacted.










### Adding your own strategies

Adding a new strategy to the tool is very simple. The modules.py contains the different trading strategies.
