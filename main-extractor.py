# References:
# 1. https://tinyurl.com/y5pewlw3
# 2. https://developers.google.com/youtube/v3/getting-started
# 3. https://developers.google.com/youtube/v3/quickstart/python
# 4. https://github.com/TheComeUpCode/SpotifyGeneratePlaylist/blob/master/create_playlist.py
# 5. https://github.com/youtube/api-samples/blob/master/python/add_channel_section.py

import json
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.errors
import youtube_dl

# for your api_key, follow the guide here:
# https://developers.google.com/youtube/registering_an_application
api_key=''

# for your channel_id, go to your Youtube channel and check the url, which looks similar to:
# https://www.youtube.com/channel/UCuAXFkgsw1L7xaCfnd5JJOw for example
# in this case, 'UCuAXFkgsw1L7xaCfnd5JJOw' is the channel_id
channel_id=''

# songs_metadata = {}

def get_authenticated_service():
    # reference: https://github.com/youtube/api-samples/blob/master/python/add_channel_section.py
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    # client_secret_file = 'client_secret.json'
    # scopes = ['https://www.googleapis.com/auth/youtube.readonly']
    service_name = 'youtube'
    version = 'v3'
    # flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes)
    # credentials = flow.run_console()
    # youtube_client = build(service_name, version, credentials=credentials)
    youtube_client = build(service_name, version, developerKey=api_key)
    return youtube_client

def get_like_dislike_ratio(likes, dislikes):
    ratio = (likes - dislikes) / (likes + dislikes)
    return '{:.2%}'.format(ratio)

def get_metadata_for_each_video(yt_client, video_id):
    # get general metadata
    meta = yt_client.videos().list(part='snippet, statistics, topicDetails', id=video_id).execute()
    main_item = meta['items'][0]
    metadata = {}

    # get statistics
    if main_item.get('statistics'):
        comprehensive_stats = main_item['statistics']
        metadata['view_count'] = comprehensive_stats['viewCount']
        if comprehensive_stats.get('likeCount') and comprehensive_stats.get('dislikeCount'):
            metadata['likes'] = int(comprehensive_stats['likeCount'])
            metadata['dislikes'] = int(comprehensive_stats['dislikeCount'])
            metadata['like_to_dislike_ratio'] = get_like_dislike_ratio(metadata['likes'], metadata['dislikes'])

    # get topics such as music genre
    if main_item.get('topicDetails'):
        topic_details = main_item['topicDetails']
        wikipedia_links = topic_details['topicCategories']
        topics = []
        for link in wikipedia_links:
            topic = link.split('wiki/')[1]
            topic = topic.replace('_', ' ')
            topics.append(topic)
        metadata['topics'] = topics

    return metadata

def merge_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def get_playlists():
    yt_client = get_authenticated_service()
    content_data = yt_client.channels().list(part='contentDetails', id=channel_id).execute()
    playlist_id = content_data['items'][0]['contentDetails']['relatedPlaylists']['favorites']
    next_page_token = None
    video_list = []
    count = 0
    invalid_videos = ['Deleted video', 'Private video']

    while True:
        res = yt_client.playlistItems().list(playlistId=playlist_id,
                                    part='snippet',
                                    pageToken=next_page_token).execute()
        items = res['items']
        for idx in range(len(items)):
            item = items[idx]['snippet']
            title = item['title']
            channel_title = item['channelTitle']
            playlist_item_id = count
            video_id = item['resourceId']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            if title not in invalid_videos:
                basic_metadata = {'id':playlist_item_id, 'video_link':video_url}
                additional_metadata = get_metadata_for_each_video(yt_client, video_id)
                song_metadata = merge_dicts(basic_metadata, additional_metadata)
                video_list.append(song_metadata)
                next_page_token = res.get('nextPageToken')
                count+=1
        if next_page_token is None:
            break

    return video_list

get_playlists()
