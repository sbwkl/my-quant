import pyperclip
import akshare as ak
import time
import requests

def main():
    code_method = code_method_str.splitlines()
    net_list = []
    for row in code_method:
        code, method_name = row.split('\t')
        method = globals().get(method_name)
        try:
            _, date, net = method(code)
        except Exception as e:
            print(code, method_name, 'error', e)
            _, date, net = code, '', ''
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
    url = f'https://www.csindex.com.cn/csindex-home/perf/index-perf-oneday?indexCode={symbol}'
    res = requests.get(url).json()
    return (symbol, res['data']['intraDayHeader']['tradeDate'], str(res['data']['intraDayHeader']['current']))

def hk_index(symbol):
    
    hk_map = {
        'HSI': '00001.00',
        'HSHCI': '02017.00',
        'HSTECH': '02083.00'
    }
    code = hk_map[symbol]
    
    url = f'https://www.hsi.com.hk/data/chi/indexes/{code}/chart.json'
    res = requests.get(url).json()
    return (symbol, res['lastUpdate'].split()[0], res['previousClose'])
    
def hk_stock(symbol):
    # his_df = ak.stock_hk_hist(symbol=symbol, period="daily", start_date="20250401", end_date="22220101", adjust="")
    his_df = ak.stock_hk_daily(symbol=symbol, adjust="")
    last = his_df.tail(1)
    net = str(last["close"].item())
    return (symbol, last["date"].item(), net)

def a_index(symbol):
    his_df = ak.stock_zh_index_daily(symbol=symbol)
    last = his_df.tail(1)
    net = str(last['close'].item())
    return (symbol, last['date'].item(), net)

forex_spot_em_df = None
def forex(symbol):
    global forex_spot_em_df
    
    if forex_spot_em_df is None:
        forex_spot_em_df = ak.forex_spot_em()
    last = forex_spot_em_df[forex_spot_em_df['代码'] == symbol]
    return (symbol, 'today', str(last['最新价'].item()))

index_global_spot_em_df = None
def global_index(symbol):
    global index_global_spot_em_df

    if index_global_spot_em_df is None:
        index_global_spot_em_df = ak.index_global_spot_em()
    
    last = index_global_spot_em_df[index_global_spot_em_df['代码'] == symbol]
    return (symbol, last['最新行情时间'].item().split()[0], str(last['最新价'].item()))

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
hk_index
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

code_method_str='''001605	a_fund
010213	a_fund
005642	a_fund
007549	a_fund
750001	a_fund
164906	a_fund
009179	a_fund
000934	a_fund
006327	a_fund
519736	a_fund
001668	a_fund
004752	a_fund
000071	a_fund
007802	a_fund
160633	a_fund
005775	a_fund
001071	a_fund
519195	a_fund
006039	a_fund
166019	a_fund
001063	a_fund
002708	a_fund
162412	a_fund
001064	a_fund
000051	a_fund
090010	a_fund
160119	a_fund
000968	a_fund
012323	a_fund
110020	a_fund
519915	a_fund
001717	a_fund
014424	a_fund
011309	a_fund
002656	a_fund
019518	a_fund
004419	a_fund
000942	a_fund
002903	a_fund
270042	a_fund
000001	csi_index
399006	sz_index
000300	csi_index
000905	csi_index
000852	csi_index
932000	csi_index
000922	csi_index
000991	csi_index
399989	csi_index
000990	csi_index
000942	csi_index
399396	sz_index
000827	csi_index
000993	csi_index
399971	csi_index
HSI	hk_index
HSHCI	hk_index
00700	hk_stock
399967	csi_index
399812	csi_index
000016	csi_index
399975	csi_index
H30533	csi_index
H11136	csi_index
HSTECH	hk_index
000688	csi_index
GDAXI	global_index
SPX	global_index
518880	a_fund
USDCNH	forex
JPYCNH	forex
000369	a_fund
110022	a_fund
'''

if __name__ == "__main__":
    main()