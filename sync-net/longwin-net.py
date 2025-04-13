import pyperclip
import akshare as ak

symbols = ['100032','000478','001052','100038','000968','001180','161017','012323','001051','519915','002708','011309','162412','001469','004752','000051','502010','003765','001064','000727','000071','012348','164906','014424','006327','340001','110027','003376','100050','019518','004419','050025','000369','004424','000942','270042','019524']
net_list = []
for symbol in symbols:
    his_df = ak.fund_open_fund_info_em(symbol=symbol, indicator="单位净值走势")
    last = his_df.tail(1)
    net = str(last["单位净值"].item())
    net_list.append(net)
    print(f'{symbol} {last["净值日期"].item()} {net}')

pyperclip.copy('\n'.join(net_list))


