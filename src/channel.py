import json
import os
from googleapiclient.discovery import build

YT_API_KEY = os.getenv('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.__channel = Channel.get_service().channels().list(id=self.__channel_id, part='snippet,contentDetails,statistics').execute()

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        # youtube = build('youtube', 'v3', developerKey=YT_API_KEY)
        # channel = youtube.channels().list(id=self.__channel_id, part='snippet,contentDetails,statistics').execute()
        print(json.dumps(self.__channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=YT_API_KEY)

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def title(self):
        return self.__channel['items'][0]['snippet']['title']

    @property
    def description(self):
        return self.__channel['items'][0]['snippet']['description']

    @property
    def url(self):
        return f"https://www.youtube.com/{self.__channel['items'][0]['snippet']['customUrl']}/"

    @property
    def subscriber_count(self):
        return self.__channel['items'][0]['statistics']['subscriberCount']

    @property
    def video_count(self):
        return self.__channel['items'][0]['statistics']['videoCount']

    @property
    def view_count(self):
        return self.__channel['items'][0]['statistics']['viewCount']

    def to_json(self, json_file):
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({'channel_id': self.channel_id, 'title': self.title,
                       'description': self.description, 'url': self.url,
                       'subscriberCount': self.subscriber_count, 'videoCount': self.video_count,
                       'viewCount': self.view_count}, f, ensure_ascii=False, indent=2)

