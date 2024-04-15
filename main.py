import os
import googleapiclient.discovery
import googleapiclient.errors

from secret_key import youtube_api_key

api_service_name = "youtube"
api_version = "v3"
YOUTUBE_API_KEY = youtube_api_key


youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=YOUTUBE_API_KEY)

request = youtube.commentThreads().list(
    part="snippet",
    videoId="SIm2W9TtzR0",
    maxResults=100
)
response = request.execute()

for item in response['items']:
    print(item['snippet']['topLevelComment']['snippet']['textDisplay'])
