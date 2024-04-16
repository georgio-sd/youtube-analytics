import googleapiclient.discovery
import googleapiclient.errors
import re

from secret_key import *

def video_comments(video_id):
    replies = []
    youtube = googleapiclient.discovery.build('youtube', 'v3',
        developerKey = youtube_api_key)
    video_threads = youtube.commentThreads().list(
        part = 'snippet',
        videoId = video_id,
        textFormat = 'plainText'
    ).execute()

    while video_threads:
        # get top level comments
        for thread in video_threads['items']:
            comment = re.sub('\n', ' ', thread['snippet']['topLevelComment']['snippet']['textDisplay'])
            replycount = thread['snippet']['totalReplyCount']
            # get replies of a top level comment
            if replycount > 0:
                video_thread_replies=youtube.comments().list(
                    part = 'snippet',
                    parentId = thread['snippet']['topLevelComment']['id'],
                    textFormat = 'plainText'
                ).execute()
                while video_thread_replies:
                    for reply in video_thread_replies['items']:
                        s = re.sub('[\u200b]*@@[a-zA-Z0-9_-]+', ' ', reply['snippet']['textDisplay'])
                        s = re.sub('[\u200d]', ' ', s)
                        s = re.sub('[\u200b]', ' ', s)
                        s = re.sub('\n', ' ', s)
                        replies.append(s)
                        #print(reply['snippet']['textDisplay'])
                        #print(re.sub('@@[a-zA-Z0-9_-]+', ' ', reply['snippet']['textDisplay']), end = '\n\n')

                    # check if there is more replies
                    if 'nextPageToken' in video_thread_replies:
                        video_thread_replies = youtube.comments().list(
                            part = 'snippet',
                            parentId = thread['snippet']['topLevelComment']['id'],
                            textFormat = 'plainText',
                            pageToken = video_thread_replies['nextPageToken']
                        ).execute()
                    else:
                        break
            # print a top level comment with its replies
            print(comment, replies, replycount, end = '\n\n')
            replies = []
        # check if there is more top level comments
        if 'nextPageToken' in video_threads:
            video_threads = youtube.commentThreads().list(
                part = 'snippet',
                videoId = video_id,
                textFormat = 'plainText',
                pageToken = video_threads['nextPageToken']
            ).execute()
        else:
            break


# Enter video id
video_id = youtube_video_id

# Call function
video_comments(video_id)
