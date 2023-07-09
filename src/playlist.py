import isodate as isodate
from googleapiclient.discovery import build

import datetime

from src.video import YT_API_KEY


class PlayList:
    __slots__ = ('playlist_id', 'channel_id', 'title', 'url')

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        playlists = self.get_service().playlists().list(id=self.playlist_id,
                                                        part='contentDetails,snippet',
                                                        maxResults=50,
                                                        ).execute()
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.title = playlists['items'][0]['snippet']['title']

    @property
    def total_duration(self):
        total = datetime.timedelta()
        videos = self.get_videos()['items']
        for video in videos:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total += duration
        return total

    def show_best_video(self):
        videos = self.get_videos()['items']
        best_video = max(videos, key=lambda x: int(x['statistics']['likeCount']))
        url_best_video = f'https://youtu.be/{best_video["id"]}'
        return url_best_video

    def get_playlist_videos(self):
        return self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails, snippet',
                                                       maxResults=50).execute()

    def get_videos(self):
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.get_playlist_videos()['items']]
        return self.get_service().videos().list(part='contentDetails,statistics',
                                                id=','.join(video_ids)
                                                ).execute()

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=YT_API_KEY)
