import schedule
import time
import atexit
import signal
from lark0 import LarkClient
from gmail_api0 import GmailService

alerting = False

def cleanup():
    print("执行退出前的清理操作...")

def signal_handler(signum, frame):
    print(f"收到信号 {signum}，程序即将退出")
    cleanup()
    exit(0)

def loop_task(client, service):
    global alerting
    if alerting:
        return
    
    messages = service.message_list("from donotreply@interactivebrokers.com is:unread")
    if len(messages) == 0:
        print('未发现告警邮件，继续监听')
        return
    
    alert_message = None
    for message in messages:
        msg = service.message_get(message["id"])
        if msg is not None and "chongqian" in msg["snippet"]:
            alert_message = msg
            break
    if alert_message is None:
        print('未发现有效的告警邮件，继续监听')
        return

    alerting = True
    msg = client.send_msg('低于警戒线，看盘');
    while True:
        res = client.read_users(msg.message_id)
        if len(res.items) > 0:
            break
        client.urgent_phone(msg.message_id)
        time.sleep(60)
    
    alerting = False

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print('设置定时任务')

    client = LarkClient()
    service = GmailService()

    schedule.every(5).minutes.do(loop_task, client=client, service=service)

    print("定时任务已启动，按 Ctrl+C 终止...")

    loop_task(client, service)

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n任务已停止")

def main_test():
    service = GmailService()
    msg_list = service.message_list('from donotreply@interactivebrokers.com is:unread')
    print(msg_list)

if __name__ == "__main__":
    main()
    # main_test()