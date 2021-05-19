# RSI Challenge with Optimization

from datetime import datetime
import backtrader as bt

from btplotting import BacktraderPlotting


# Create a subclass of Strategy to define the indicators and logic

class RSIStrategy(bt.Strategy):

    params = (
        ('maperiod', 31),
    )

    def __init__(self):

        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=self.params.maperiod, safediv=True) # Use RSI indicator for the chart

    def next(self):

        if not self.position: # If not in market ...

            if self.rsi < 30: # If RSI is oversold ...

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.buy()

        else: # if in market ... 

            if self.rsi > 70:
                
                # SELL, SELL, SELL!!! (with all possible default parameters)              
                self.sell()

if __name__ == '__main__':

    #Variable for our starting cash
    startcash = 10000

    cerebro = bt.Cerebro(optreturn=False) # Instantiate
    strats = cerebro.optstrategy(RSIStrategy, maperiod=range(1, 100)) # Add the trading strategy
    
    # Create a data feed
    data = bt.feeds.YahooFinanceData(
        dataname="MFST",
        fromdate=datetime(2011, 1, 1),
        todate=datetime(2021, 12, 31)
    )

    cerebro.adddata(data) # Add data feed

    # Set our desired cash start
    cerebro.broker.setcash(startcash)

    opt_runs = cerebro.run() # run it all - loop over data

    # Generate results list
    final_results_list = []
    for run in opt_runs:
        for strategy in run:
            value = round(strategy.broker.get_value(),2)
            PnL = round(value - startcash,2)
            maperiod = strategy.params.maperiod
            final_results_list.append([maperiod,PnL])

    #Sort Results List
    by_period = sorted(final_results_list, key=lambda x: x[0])
    by_PnL = sorted(final_results_list, key=lambda x: x[1], reverse=True)

    by_period_index = 0
    highestPeriod = 0
    highestPnL = 0

    # loop over data to get highest value
    for pd in by_period:

        print(pd)

        if highestPeriod < pd[1]:
            highestPeriod = pd[1]
            by_period_index = pd[0]

    for pnl in by_PnL:
        
        if highestPnL < pnl[1]:
            highestPnL = pnl[1]
        
    print(f'Highest Period: MAPeriod = {by_period_index}, Value = {highestPeriod}, Profit = {highestPnL}')
    
    # Instantiate cerebro again to modify data
    cerebro = bt.Cerebro()
    cerebro.addstrategy(RSIStrategy, maperiod=by_period_index)

    # Add new data
    cerebro.adddata(data)

    cerebro.addanalyzer(bt.analyzers.SharpeRatio)

    cerebro.run()

    p = BacktraderPlotting(style="bar")

    cerebro.plot(p)
