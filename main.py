import googleapiclient.discovery
import googleapiclient.errors
import re

from secret_key import *

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(
    model_name = "gpt-3.5-turbo",
    temperature = 0.6,
    max_tokens = 512,
    api_key = chatgpt_api_key)

answer = llm.invoke("how can langsmith help with testing?")
print(answer)

def video_comments(video_id):
    comments = []
    topic = []
    youtube = googleapiclient.discovery.build('youtube', 'v3',
        developerKey = youtube_api_key)
    video_threads = youtube.commentThreads().list(
        part = 'snippet',
        videoId = video_id,
        textFormat = 'plainText',
    ).execute()

    while video_threads:
        # get top level comments
        for thread in video_threads['items']:
            topic.append(re.sub('\n', ' ', thread['snippet']['topLevelComment']['snippet']['textDisplay']))
            # get replies of a top level comment
            if thread['snippet']['totalReplyCount'] > 0:
                video_thread_replies=youtube.comments().list(
                    part = 'snippet',
                    parentId = thread['snippet']['topLevelComment']['id'],
                    textFormat = 'plainText',
                ).execute()
                while video_thread_replies:
                    for reply in video_thread_replies['items']:
                        s = re.sub('[\u200b]*@@[a-zA-Z0-9_-]+', ' ', reply['snippet']['textDisplay'])
                        s = re.sub('[\u200d]', ' ', s)
                        s = re.sub('[\u200b]', ' ', s)
                        s = re.sub('\n', ' ', s)
                        topic.append(s)

                    # check if there is more replies
                    if 'nextPageToken' in video_thread_replies:
                        video_thread_replies = youtube.comments().list(
                            part = 'snippet',
                            parentId = thread['snippet']['topLevelComment']['id'],
                            textFormat = 'plainText',
                            pageToken = video_thread_replies['nextPageToken'],
                        ).execute()
                    else:
                        break
            # print a top level comment with its replies
            #print(topic, end = '\n\n')
            comments.append(topic)
            topic = []
        # check if there is more top level comments
        if 'nextPageToken' in video_threads:
            video_threads = youtube.commentThreads().list(
                part = 'snippet',
                videoId = video_id,
                textFormat = 'plainText',
                pageToken = video_threads['nextPageToken'],
            ).execute()
        else:
            break
    return comments


# Enter video id
video_id = youtube_video_id

# Call function
comments = video_comments(video_id)
print(comments)
