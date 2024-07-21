from datetime import datetime
import random
from monitor import yt_monitor
import json, time
class Logger:
    def message(self, message):
        print(f'[{datetime.now().strftime("%H:%M:%S")}] {message}')

class youtube(Logger):
    def __init__(self):
        with open("E:\\OneDrive\\lavoro\\YTMONITOR\\data.json", "rb") as f:
            data = json.load(f)
            usernames = data["usernames"]
            api_keys = data["api_key"]
            WEBHOOK_URL = data["webhook_url"]
            f.close()
        YTAPI_KEY = random.choice(api_keys)
        self.yt_m = yt_monitor(YTAPI_KEY, WEBHOOK_URL,usernames)
        while True:
            self.message("\033[1m--MONITORING--\033[0m")
            i=0
            for channel_id in self.yt_m.channel_ids:
                self.yt_m.current_username = usernames[i]
                self.yt_m.monitor_channels(channel_id)
                i+=1
            time.sleep(3600)

youtube()


