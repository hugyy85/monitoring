from os import getenv
from sys import argv

import psutil
import requests


BOT_TOKEN = getenv('TG_BOT_TOKEN')
CHAT_ID = getenv('CHAT_ID')


class Monitor:

    def __init__(self, server_name: str, interval_sec: int = 60, deadline: int = 90):
        self.server_name = server_name
        self.interval = interval_sec  # seconds
        # граница для срабатывания
        self.deadline = deadline  # percent

    def send_notification_if_alert(self, value: float, name: str, deadline: int = None):
        deadline = deadline or self.deadline
        if value > deadline:
            self.send_tg_notification(f'{name} ALERT: {value}% on {self.server_name} server.'
                                      f' Interval: {self.interval} sec. Deadline: {self.deadline}%')

    @staticmethod
    def send_tg_notification(message: str):
        response = requests.get(
            f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}'
        )
        response.raise_for_status()

    def check(self):
        self.send_notification_if_alert(psutil.cpu_percent(interval=self.interval), 'CPU')
        self.send_notification_if_alert(psutil.virtual_memory().percent, 'MEMORY')
        self.send_notification_if_alert(psutil.disk_usage('/').percent, 'DISK')
        self.send_notification_if_alert(psutil.getloadavg()[2], 'LOAD_AVERAGE_15_MIN', deadline=psutil.cpu_count() + 1)


if __name__ == '__main__':
    args = argv[1:]
    if not args:
        raise ValueError('server name is required')
    server_name_ = args[0]
    interval_sec_ = int(args[1]) if len(args) > 1 else 60
    deadline_ = int(args[2]) if len(args) > 2 else 90
    Monitor(server_name=server_name_, interval_sec=interval_sec_, deadline=deadline_).check()
