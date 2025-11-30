import schedule
import time
import atexit
import signal
from datetime import datetime
import akshare as ak
import traceback
from diskcache import Cache
import requests
import shutil

def cleanup():
    print("执行退出前的清理操作...")

def signal_handler(signum, frame):
    print(f"收到信号 {signum}，程序即将退出")
    cleanup()
    exit(0) 

def print_task():
    try:
        monitor()
    except Exception as e:
        print(f'发生未知异常')
        traceback.print_exc()
def notify_local(data):
    if shutil.which('termux-notification') is not None and shutil.which('termux-vibrate') is not None:
        print('notify local and vibrate 300ms')
        os.system('termux-notification --title "AU sigal" --content "discover AU basis"')
        os.system('termux-vibrate -d 300')
    else:
        print('termux-notification or termux-vibrate not found, skip notify')

def notify_win11(data):
    try:
        from win11toast import toast
        print('notify to win11 notification')
        toast('au')
    except Exception as e:
        print('win11toast not found, skip notify')

def notify_mp(data):
    print('notify to weixin miniprogram')
    cache = Cache('/tmp/mycache')
    cache_key = 'accessToken'
    # get wxmp accessToken
    token = cache.get(cache_key)
    if token is None:
        res = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxece3e9fb6c702bcc&secret=a857851458de260de09990fec9fafd7b').json()
        token = res.get('access_token')
        if token:
            cache.set(cache_key, token, expire=7200)
    # send notify
    payload = {
        "touser": "o8QZ_11CllfIhV3eJb5I2OD3ypBE",
        "template_id": "iW_S-ZTm8vLQ1CkfWUndOGIfJkIoBvCsJZ1lB2dYY6k",
        "miniprogram_state":"developer",
        "lang":"zh_CN",
        "data":{
            "time3": {
                "value": "2025-10-25 19:29"
            },
            "short_thing19": {
                "value": "AU"
            },
            "thing2": {
                "value": "测试 xxxx"
            },
            "thing11": {
                "value": "备注 xxxx"
            }
        }
    }
    url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=' + token
    requests.post(url, json=payload)

def monitor():
    # f1 = ak.futures_zh_spot(symbol='AG2508', market="CF", adjust='0')['current_price'].item()
    # f2 = ak.futures_foreign_commodity_realtime(symbol='SI')['最新价'].item()
    
    # forex_df = ak.forex_hist_em(symbol="USDCNH")
    forex_df = ak.forex_spot_em()
    forex_df = forex_df[forex_df['代码'] == "USDCNH"]
    usdcnh = forex_df.tail(1)['最新价'].item()
    # f2_cnh = f2 * usdcnh / 31.1034768 * 1000
    
    # print('ag:',f1 - f2_cnh)
    
    # xau = ak.futures_foreign_commodity_realtime(symbol='XAU')['最新价'].item()
    au0 = ak.futures_zh_spot(symbol='AU0', market="CF", adjust='0')['current_price'].item()
    gc = ak.futures_foreign_commodity_realtime(symbol='GC')['最新价'].item()
    gc_cnh = round(gc * usdcnh / 31.1034768, 2)
    basis = round(au0 - gc_cnh, 2)
    
    print(f'{datetime.now()} basis: {basis} = {au0} - {gc_cnh} (￥/g) forex: {usdcnh}')
    
    if basis  < -13.98:
        obj = {}
        nofity_local(obj)
        notify_win11(obj)
        notify_mp(obj)

def main():
    atexit.register(cleanup)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print('设置定时任务')

    schedule.every(1).minutes.do(print_task)

    print("定时任务已启动，按 Ctrl+C 终止...")

    print_task()

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n任务已停止")

if __name__ == "__main__":
    main()