import schedule
import time
import atexit
import signal
from lark0 import LarkClient

def cleanup():
    print("执行退出前的清理操作...")

def signal_handler(signum, frame):
    print(f"收到信号 {signum}，程序即将退出")
    cleanup()
    exit(0)

def loop_task():
    print('monitor')

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print('设置定时任务')

    schedule.every(5).minutes.do(loop_task)

    print("定时任务已启动，按 Ctrl+C 终止...")

    client = LarkClient()

    loop_task()

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n任务已停止")

if __name__ == "__main__":
    main()