import os
import googleapiclient.discovery
import googleapiclient.errors

from secret_key import *

api_service_name = "youtube"
api_version = "v3"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=youtube_api_key)

request = youtube.commentThreads().list(
    part="snippet",
    videoId=youtube_video_id,
    maxResults=100
)
response = request.execute()

for item in response['items']:
    print(item['snippet']['topLevelComment']['snippet']['textDisplay'])
