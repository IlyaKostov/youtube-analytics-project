import os
from googleapiclient.discovery import build

from src.wrong_id import WrongId

YT_API_KEY = os.getenv('YT_API_KEY')


class Video:
    def __init__(self, video_id):
        self.__video_id = video_id
        try:
            self.video = self.get_service().videos().list(id=self.__video_id,
                                                          part='snippet,contentDetails,statistics').execute()
            if len(self.video['items']) == 0:
                raise WrongId
        except WrongId as a:
            print(a.message)
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None
        else:
            self.title = self.video['items'][0]['snippet']['title']
            self.url = f'https://youtu.be/{self.__video_id}'
            self.view_count = self.video['items'][0]['statistics']['viewCount']
            self.like_count = self.video['items'][0]['statistics']['likeCount']

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=YT_API_KEY)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__video_id})'

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id, pl_video_id):
        super().__init__(video_id)
        self.pl_video_id = pl_video_id
