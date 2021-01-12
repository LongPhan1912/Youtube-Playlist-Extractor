# General references:
# 0. https://github.com/lttkgp/youtube_title_parse
# 1. https://tinyurl.com/y5pewlw3
# 2. https://developers.google.com/youtube/v3/getting-started
# 3. https://developers.google.com/youtube/v3/quickstart/python
# 4. https://github.com/TheComeUpCode/SpotifyGeneratePlaylist/blob/master/create_playlist.py
# 5. https://github.com/youtube/api-samples/blob/master/python/add_channel_section.py

import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.errors
import pandas as pd
import csv
import json
from youtube_title_parse import get_artist_title

# for your api_key, follow the guide here:
# https://developers.google.com/youtube/registering_an_application
api_key=''

# for your channel_id, go to your Youtube channel and check the url, which looks similar to:
# https://www.youtube.com/channel/UCuAXFkgsw1L7xaCfnd5JJOw for example
# in this case, 'UCuAXFkgsw1L7xaCfnd5JJOw' is the channel_id
channel_id=''

def get_authenticated_service():
    # references:
    # https://github.com/youtube/api-samples/blob/master/python/add_channel_section.py
    # https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps#python
    service_name = 'youtube'
    version = 'v3'

    # if you do NOT want to hard code the api_key:
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    # client_secret_file = 'client_secret.json'
    # scopes = ['https://www.googleapis.com/auth/youtube.readonly']
    # flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes)
    # credentials = flow.run_console()
    # youtube_client = build(service_name, version, credentials=credentials)

    # otherwise:
    youtube_client = build(service_name, version, developerKey=api_key)

    return youtube_client

def get_like_dislike_ratio(likes, dislikes):
    ratio = (likes - dislikes) / (likes + dislikes)
    return '{:.2%}'.format(ratio)

def get_metadata_for_each_video(yt_client, video_id):
    # get general metadata
    # reference: https://developers-dot-devsite-v2-prod.appspot.com/youtube/v3/docs/videos/list#id
    meta = yt_client.videos().list(part='snippet, statistics, topicDetails', id=video_id).execute()
    main_item = meta['items'][0]
    metadata = {}

    # get channel title; used in case we cannot extract the artist name from the title
    if main_item.get('snippet'):
        snippet = main_item['snippet']
        metadata['channel_title'] = snippet['channelTitle']

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
            topics.append(topic.upper())
        metadata['topics'] = topics
    else: # if we do not get any tags for the video topic
        metadata['topics'] = ['OTHER']

    return metadata

# helper function to merge two dictionaries together
def merge_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def get_playlists():
    yt_client = get_authenticated_service()
    # get the general content details
    # reference: https://developers.google.com/youtube/v3/docs/playlistItems/list#ruby
    content_data = yt_client.channels().list(part='contentDetails', id=channel_id).execute()

    related_playlists = content_data['items'][0]['contentDetails']['relatedPlaylists']
    # this lets you get the id for your Favorites playlist.
    # print out the related_playlists field to look for any other playlists, e.g. liked videos
    playlist_id = related_playlists['favorites']
    next_page_token = None
    video_list = []
    count = 0
    invalid_videos = ['Deleted video', 'Private video']

    while True:
        # get the snippet information from our playlist
        # the page token is kind of like a linked list;
        # we jump from one token to another until we reach the end
        res = yt_client.playlistItems().list(playlistId=playlist_id,
                                    part='snippet',
                                    pageToken=next_page_token).execute()
        items = res['items']
        for idx in range(len(items)):
            item = items[idx]['snippet']
            video_title = item['title']
            playlist_item_id = count
            video_id = item['resourceId']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            # make sure we have a valid video (and title)
            if video_title not in invalid_videos:
                additional_metadata = get_metadata_for_each_video(yt_client, video_id)
                tuple = get_artist_title(video_title)
                if tuple != None:
                    artist, song_name = tuple[0], tuple[1]
                else:
                    # if we cannot extract meaningful information from our title,
                    # use the channel title (person who uploaded the video) and default video title instead
                    artist, song_name = additional_metadata['channel_title'], video_title
                basic_metadata = { 'id':playlist_item_id,
                                    'video_title':video_title,
                                    'video_id': video_id,
                                    'video_link':video_url,
                                    'artist': artist,
                                    'song_name': song_name }

                # get a comprehensive dictionary of all the useful information needed for any given video
                # add or remove any dictionary fields you'd like :)
                song_metadata = merge_dicts(basic_metadata, additional_metadata)
                video_list.append(song_metadata)
                # go to the next video on the playlist
                next_page_token = res.get('nextPageToken')
                count+=1

        # once you reach the end (i.e. null), stop
        if next_page_token is None:
            break

    return video_list


# these functions let you export your playlist into any data format you'd like
def export_to_json(video_list):
    with open('favorite-playlist.txt', 'w') as output_file:
        json.dump(video_list, output_file, ensure_ascii=False, indent=4)

# the excel export will heavily depend on the csv export
def export_to_csv(video_list):
    # reference: https://stackoverflow.com/questions/3086973/how-do-i-convert-this-list-of-dictionaries-to-a-csv-file
    keys = video_list[0].keys()
    with open('favorite-playlist.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(video_list)

def export_to_excel(video_list):
    df = pd.read_csv('favorite-playlist.csv')
    output_file = pd.ExcelWriter('favorites-playlist.xlsx')
    df.to_excel(output_file, index=False)
    output_file.save()

# output the full list of videos you have in your chosen playlist (in this case, the Favorites playlist)
def your_output_choice():
    # depending on the length of your playlist, please use this function call sparsely
    # you are only limited to 10,000 api calls per day, so this can be a very expensive operation
    video_list = get_playlists()

    # warning: if you choose choice (0 and 2) or (1 and 2) or all three, you're making loads of api calls
    # so pick only one choice, or both (0 and 1)

    # choice 0:
    export_to_csv(video_list)
    # choice 1 (needs choice 0 to work):
    export_to_excel(video_list)
    # choice 2:
    # export_to_json(video_list)

# if __name__ == "__main__":
#     your_output_choice()

