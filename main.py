import googleapiclient.discovery
import googleapiclient.errors

from secret_key import *

def video_comments(video_id):
    replies = []
    youtube = googleapiclient.discovery.build('youtube', 'v3',
        developerKey = youtube_api_key)
    video_threads = youtube.commentThreads().list(
        part = 'snippet',
        videoId = video_id,
        maxResults = 5
    ).execute()

    while video_threads:
        # get top level comments
        for thread in video_threads['items']:
            comment = thread['snippet']['topLevelComment']['snippet']['textDisplay']
            replycount = thread['snippet']['totalReplyCount']
            # get replies for a top level comment
            if replycount > 0:
                video_thread_replies=youtube.comments().list(
                    part = 'snippet',
                    parentId = thread['snippet']['topLevelComment']['id'],
                    maxResults=5
                ).execute()
                while video_thread_replies:
                    for reply in video_thread_replies['items']:
                        replies.append(reply['snippet']['textDisplay'])
                    # check if there is more replies
                    if 'nextPageToken' in video_thread_replies:
                        video_thread_replies = youtube.comments().list(
                            part = 'snippet',
                            parentId = thread['snippet']['topLevelComment']['id'],
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
                pageToken = video_threads['nextPageToken']
            ).execute()
        else:
            break


# Enter video id
video_id = youtube_video_id

# Call function
video_comments(video_id)
