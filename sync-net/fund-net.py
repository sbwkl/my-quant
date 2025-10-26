import pyperclip
import akshare as ak

def main():
    code_lines = code_str.splitlines()
    method_lines = method_str.splitlines()
    net_list = []
    for row in zip(code_lines, method_lines):
        code, method_name = row
        method = globals().get(method_name)
        _, date, net = method(code)
        net_list.append(net)
        print(f'{code} {date} {net}')
    
    pyperclip.copy('\n'.join(net_list))

def a_fund(symbol):
    his_df = ak.fund_open_fund_info_em(symbol=symbol, indicator="单位净值走势")
    last = his_df.tail(1)
    net = str(last["单位净值"].item())
    return (symbol, last["净值日期"].item(), net)

def sh_index(symbol):
    return a_index('sh' + symbol)
def sz_index(symbol):
    return a_index('sz' + symbol)
def csi_index(symbol):
    return a_index('csi' + symbol)

def hk_index(symbol):
    try:
        his_df = ak.stock_hk_index_daily_em(symbol=symbol)
        last = his_df.tail(1)
        net = str(last["latest"].item())
        return (symbol, last["date"].item(), net)
    except Exception:
        return (symbol, '', '')
    
def hk_stock(symbol):
    his_df = ak.stock_hk_hist(symbol=symbol, period="daily", start_date="20250401", end_date="22220101", adjust="")
    last = his_df.tail(1)
    net = str(last["收盘"].item())
    return (symbol, last["日期"].item(), net)

def a_index(symbol):
    his_df = ak.stock_zh_index_daily_em(symbol=symbol)
    last = his_df.tail(1)
    net = str(last['close'].item())
    return (symbol, last['date'].item(), net)

def forex(symbol):
    his_df = ak.forex_hist_em(symbol=symbol)
    last = his_df.tail(1)
    return (symbol, last['日期'].item(), str(last['最新价'].item()))

def global_index(symbol):
    name_map = {
        'HSI': '恒生指数',
        'SPX': '标普500',
        'GDAXI': '德国DAX30'
    }
    his_df = ak.index_global_hist_em(symbol=name_map[symbol])
    last = his_df.tail(1)
    return (symbol, last['日期'].item(), str(last['最新价'].item()))

code_str='''001605
010213
005642
007549
750001
164906
009179
000934
006327
519736
001668
004752
000071
007802
160633
005775
001071
519195
006039
166019
001063
002708
162412
001064
000051
090010
160119
000968
012323
110020
519915
001717
014424
011309
002656
019518
004419
000942
002903
270042
000001
399006
000300
000905
000852
932000
000922
000991
399989
000990
000942
399396
000827
000993
399971
HSI
HSHCI
00700
399967
399812
000016
399975
H30533
H11136
HSTECH
000688
GDAXI
SPX
518880
USDCNH
JPYCNH
000369
110022
'''
method_str='''a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
a_fund
sh_index
sz_index
sh_index
sh_index
sh_index
csi_index
sh_index
sh_index
sz_index
sh_index
sh_index
sz_index
sh_index
sh_index
sz_index
global_index
hk_index
hk_stock
sz_index
sz_index
sh_index
sz_index
csi_index
csi_index
hk_index
sh_index
global_index
global_index
a_fund
forex
forex
a_fund
a_fund
'''

if __name__ == "__main__":
    main()