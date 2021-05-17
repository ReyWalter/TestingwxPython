# Testing Backtrader

from __future__ import (absolute_import, division, print_function, unicode_literals)

import backtrader as bt

if __name__ == '__main__':

    # Instantiate Cerebro
    cerebro = bt.Cerebro()

    # Sets the cash of broker to $100k
    cerebro.broker.setcash(100000.0)

    # Prints Broker's Initial Money
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run cerebro to loop over data
    cerebro.run()

    # Prints Broker's Final Money
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
