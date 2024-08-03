# region imports
from AlgorithmImports import *
# endregion

class Demo(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2019, 6, 6)
        self.set_end_date(2023,6,6)
        self.set_cash(5000)
        self.spy = self.add_equity("SPY", Resolution.DAILY)
        self.ma1_spy = self.SMA(self.spy.Symbol,30)
        self.ma2_spy = self.SMA(self.spy.Symbol,150)
        self.rsi1_spy = self.RSI(self.spy.symbol, 5, Resolution.DAILY)
        self.set_warm_up(100)

    def on_data(self, data: Slice):
        rsi1_spy_value = self.rsi1_spy.Current.Value
        if self.is_warming_up:
            return
        if not self.portfolio.invested:
            if self.spy.price > self.ma2_spy.Current.Value and self.spy.price < self.ma1_spy.Current.Value and rsi1_spy_value < 30:
                self.set_holdings(self.spy.symbol, 1)
                self.debug("Buy at " + str(self.spy.symbol) + " price:" + str(self.spy.price) + " > MA " + str(self.ma1_spy.Current.Value))

        if self.portfolio.invested:
            if self.spy.price < (self.portfolio[self.spy.symbol].average_price * 0.90):
                self.liquidate(self.spy.symbol)
                self.debug("Stop loss tigger for " + str(self.spy.symbol) + " at price:" + str(self.spy.price))

            if self.spy.price > (self.portfolio[self.spy.symbol].average_price * 1.30):
                self.liquidate(self.spy.symbol)
                self.debug("Take profit tigger for " + str(self.spy.symbol) + " at price:" + str(self.spy.price))

            if self.spy.price < self.ma1_spy.Current.Value and rsi1_spy_value < 30:
                self.liquidate(self.spy.symbol)
                self.debug("Sell at " + str(self.spy.symbol) + " price:" + str(self.spy.price) + " < MA " + str(self.ma1_spy.Current.Value))

        self.Plot("SPY", "MA30", self.ma1_spy.Current.Value)
        self.Plot("SPY", "MA159", self.ma2_spy.Current.Value)
        self.Plot("SPY", "SPY", self.spy.price)
    
    def on_order_event(self, order_event):
        order = self.transactions.get_order_by_id(order_event.order_id)
        #self.log("{0}: {1}: {2}:".format(self.time, order.type, order_event))
