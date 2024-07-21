import json
from googleapiclient.discovery import build
import requests
import isodate

def parse_duration(duration):
    return isodate.parse_duration(duration).total_seconds()

def send_discord_notification(webhook,message):
    data = {"content": message}
    response = requests.post(webhook,json=data)
    response.raise_for_status()
class yt_monitor:

    def __init__(self,API_KEY, WEBHOOK, usernames):
        self.API_KEY = API_KEY
        self.WEBHOOK = WEBHOOK
        self.youtube = build('youtube', 'v3', developerKey=self.API_KEY)
        self.video_to_check = ""
        self.current_username= None
        print("\033[1m--CHANNELS FOUND--\033[0m")
        self.channel_ids = [self.search_channel_by_username(username) for username in usernames]

    def search_channel_by_username(self, username):
        base_url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            'part': 'id,snippet',
            'maxResults': 1,
            'type': 'channel',
            'q': username,
            'key': self.API_KEY
        }

        response = requests.get(base_url, params=params)
        if response.status_code !=200:
            print(f"No channels found for username: {username}")
            return None

        # Sort channels by subscriber count
        items = response.json()["items"][0]
        
        channel_id = items['id']['channelId']
        channel_name = items['snippet']['title']
        print(f"\033[1m{channel_name}\033[0m (ID: {channel_id})")
        return channel_id

    def get_latest_videos(self, channel_id):
        request = self.youtube.search().list(
            part='snippet',
            channelId=channel_id,
            maxResults=1,
            order='date',
            type='video'
        )
        response = request.execute()
        videos = []
        item = response['items'][0]
        video_id = item['id']['videoId']
        self.video_to_check= f"https://www.youtube.com/watch?v={video_id}"
        video_title = item['snippet']['title']
        
        self.video_to_check= f"https://www.youtube.com/watch?v={video_id}"

        videos_request = self.youtube.videos().list(
            part="contentDetails",
            id=video_id
        )
        videos_response = videos_request.execute()

        
        duration_seconds = parse_duration(videos_response['items'][0]['contentDetails']['duration'])
        if duration_seconds > 60: 
            videos.append((video_title, video_id, )) # Filtering out videos shorter than 60 seconds
            return videos
        else:
            return False

    def monitor_channels(self, channel_id):
        with open("E:\\OneDrive\\lavoro\\YTMONITOR\\checked.json", "rb") as f:
            checked_videos = json.load(f)
            f.close()
        try:
            videos = self.get_latest_videos(channel_id)
            if videos != False:
                for title, video_id in videos:
                    if video_id not in checked_videos["checked"]:
                        print(f"\033[1m--New VIDEO from: {self.current_username}--\033[0m")
                        checked_videos["checked"].append(video_id)
                        message = f"**{self.current_username}**: {title}\n**https://www.youtube.com/watch?v={video_id}**"
                        print("\033[1m--Sending Message to DISCORD--\033[0m")
                        send_discord_notification(self.WEBHOOK,message)
                    else:
                        pass
            else:
                print(f"\033[1mShort Found from: {self.current_username}--\033[0m")
        except Exception as e:
            print(f"Error: {e}")
        with open("E:\\OneDrive\\lavoro\\YTMONITOR\\checked.json", "w") as file:
            json.dump(checked_videos, file, indent=4)
            f.close()
