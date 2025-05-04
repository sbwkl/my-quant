from datetime import datetime, timedelta
import akshare as ak
import pandas as pd
import copy
import collections
import inspect
from matplotlib_inline import backend_inline
from matplotlib import pyplot as plt
from IPython import display

def use_svg_display():
    backend_inline.set_matplotlib_formats('svg')

class HyperParameters:
    def save_hyperparameters(self, ignore=[]):
        frame = inspect.currentframe().f_back
        _, _, _, local_vars = inspect.getargvalues(frame)
        self.hparams = {k:v for k, v in local_vars.items()
                        if k not in set(ignore+['self']) and not k.startswith('_')}
        for k, v in self.hparams.items():
            setattr(self, k, v)
            
class ProgressBoard(HyperParameters):

    def __init__(self, xlabel=None, ylabel=None, xlim=None,
                 ylim=None, xscale='linear', yscale='linear',
                 ls=['-', '--', '-.', ':'], colors=['C0', 'C1', 'C2', 'C3'],
                 fig=None, axes=None, figsize=(3.5, 2.5), display=True):
        self.save_hyperparameters()

    def draw(self, x, y, label):
        Point = collections.namedtuple('Point', ['x', 'y'])
        if not hasattr(self, 'data'):
            self.data = collections.OrderedDict()
        if label not in self.data:
            self.data[label] = []
        line = self.data[label]
        line.append(Point(x, y))
        if not self.display:
            return
        use_svg_display()
        if self.fig is None:
            self.fig = plt.figure(figsize=self.figsize)
        plt_lines, labels = [], []
        for (k, v), ls, color in zip(self.data.items(), self.ls, self.colors):
            plt_lines.append(plt.plot([p.x for p in v], [p.y for p in v],
                                          linestyle=ls, color=color)[0])
            labels.append(k)
        axes = self.axes if self.axes else plt.gca()
        if self.xlim: axes.set_xlim(self.xlim)
        if self.ylim: axes.set_ylim(self.ylim)
            
        axes.set_xlabel(self.xlabel)
        axes.set_ylabel(self.ylabel)
        axes.set_xscale(self.xscale)
        axes.set_yscale(self.yscale)
        axes.legend(plt_lines, labels)
        display.display(self.fig)
        display.clear_output(wait=True)

class Portfolio():
    def __init__(self, max_pos, daily_budge):
        self.max_pos = max_pos
        self.daily_budge = daily_budge
        self.cash = max_pos * daily_budge
        self.net_worth = self.cash
        self.net_worth_his = []
        
        self.position = []
        self.trades = []
        self.press = 0
        self.last_buy  = datetime(1949, 10, 1, 9, 31, 0)
        self.last_sell = datetime(1949, 10, 1, 9, 31, 0)
        
class Regression():
    def __init__(self):
        pass

    def reg_test(self, strategy, data, every_n=1):
        his_price = data.load_his_price()
        start_time = his_price.index[0]

        n = 0
        for current_time, price_row in his_price.iterrows():
            strategy._eval(current_time, price_row)

            n += 1
            if n % every_n == 0:
                days = (current_time - start_time).days
                strategy.board.draw(days, strategy.portfolio.net_worth, 'net-worth')
                pass
        strategy._eval_last(current_time, price_row)

class AkShareData():
    def __init__(self, boll_args, his_args):
        self.boll_args = boll_args
        self.his_args = his_args

    def load_boll_data(self):
        symbol, start_date, end_date, period, n, k = self.boll_args
        boll_raw = ak.fund_etf_hist_em(symbol=symbol, period=period, start_date=start_date, end_date=end_date, adjust="")
        
        boll_raw['std'] = boll_raw['收盘'].rolling(window=n).std(ddof=1).round(3)
        boll_raw['MID'] = boll_raw['收盘'].rolling(window=n).mean().round(3)
        boll_raw['UP']  = boll_raw['MID'] + k * boll_raw['std']
        boll_raw['LOW'] = boll_raw['MID'] - k * boll_raw['std']
        
        col_mapping = {'日期': 'date', '开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low', '成交量': 'vol', '成交额': 'money'}
        
        boll = boll_raw.rename(columns=col_mapping)
        return boll
        
    def load_his_price(self):
        symbol, start_date, end_date, period = self.his_args
        col_mapping = {'日期': 'date', '开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low', '成交量': 'vol', '成交额': 'money'}
        
        his_price_raw = ak.fund_etf_hist_em(symbol=symbol, period=period, start_date=start_date, end_date=end_date, adjust="")
        his_price_raw = his_price_raw.rename(columns=col_mapping)[col_mapping.values()]
        his_price_raw["date_idx"] = pd.to_datetime(his_price_raw["date"])
        his_price = his_price_raw.drop(columns='date')
        his_price = his_price.set_index("date_idx")
        
        return his_price

class Strategy(HyperParameters):
    def __init__(self, max_pos=10, daily_budge=2000):
        self.save_hyperparameters()
        self.board = ProgressBoard(xlabel='date', ylabel='net worth', figsize=(7, 5))
        self.portfolio = Portfolio(max_pos, daily_budge)

    def sell(self, init_trade, price):
        portfolio = self.portfolio
        
        if len(portfolio.position) == 0:
            return
        portfolio = self.portfolio
        trade = init_trade()
        
        sell_money = 0
        for buy_trade in portfolio.position:
            pos = buy_trade['pos']
            sell_trade = copy.deepcopy(trade)
            sell_trade.update({
                'op': 'sell',
                'pos': pos, 
                'money': pos * price,
                'price': price, 
            })
            sell_money += pos * price
            portfolio.trades.append({
                'buy': buy_trade,
                'sell': sell_trade
            })
        portfolio.position = []
        portfolio.cash += sell_money

    def dummy_sell(self, init_trade, price):
        trade = init_trade()
        for buy_trade in self.portfolio.position:
            pos = buy_trade['pos']
            sell_trade = copy.deepcopy(trade)
            sell_trade.update({
                'op': 'sell',
                'pos': pos, 
                'money': pos * price,
                'price': price, 
            })
            self.portfolio.trades.append({
                'buy': buy_trade,
                'sell': sell_trade
            })
        
        
    def buy(self, init_trade, price):
        portfolio = self.portfolio
        trade = init_trade()
        
        # 仓位是 100 的整数倍
        pos = portfolio.daily_budge // (price * 100) * 100
        buy_money = pos * price
        trade.update({
            'op': 'buy',
            'pos': pos, 
            'money': buy_money,
            'price': price, 
        })
        portfolio.position.append(trade)
        portfolio.press = max(portfolio.press, len(portfolio.position))
        portfolio.cash -= buy_money

    def wait(self, price):
        portfolio = self.portfolio
        
        # 等待机会
        market_value = 0
        for buy_trade in portfolio.position:
            pos = buy_trade['pos']
            market_value += pos * price
        portfolio.net_worth = portfolio.cash + market_value