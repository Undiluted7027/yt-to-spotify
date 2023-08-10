import requests, json, os, config
import googleapiclient.discovery

API_KEY = config.yt_api_key

def yt_setup():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = API_KEY)
    return youtube


def dummy_request(id_playlist):
    yt_api_obj = yt_setup()
    playlist_items_request = yt_api_obj.playlistItems().list(
    part="snippet",
    playlistId= id_playlist,
    maxResults = 50
)
    api_response = playlist_items_request.execute()
    if api_response['pageInfo']['totalResults'] <= 50:
        return api_response['items']
    else:
        return api_response['nextPageToken'], api_response['pageInfo']['totalResults'], api_response['items']


def get_list_of_playlist_items(id_playlist):
    yt_api_obj = yt_setup()
    playlist_items_request = yt_api_obj.playlistItems().list(
    part="snippet",
    playlistId= id_playlist,
    maxResults = 50
)
    api_response = playlist_items_request.execute()
    all_videos = []
    if api_response['pageInfo']['totalResults'] > 50:
        nextPageToken, totalResults, firstPage = dummy_request(id_playlist)
        first_page_videos = [i['snippet']['title'] for i in firstPage]
        all_videos, iter_var = first_page_videos, 0
        while iter_var <= totalResults:
            
            yt_api_obj = yt_setup()
            playlist_items_request = yt_api_obj.playlistItems().list(
            part="snippet",
            playlistId= id_playlist,
            pageToken=nextPageToken,
            maxResults=50
        )
            api_response = playlist_items_request.execute()
            
            try:
                nextPageToken = api_response['nextPageToken']
                all_videos += [i['snippet']['title'] for i in api_response['items']]
                iter_var += 50
                
            except KeyError:
                all_videos += [i['snippet']['title'] for i in api_response['items']]
                break
        else:
            all_videos = [i['snippet']['title'] for i in dummy_request(id_playlist)]

    all_videos_filtered = ["".join(j for j in i if (j.isalnum() or j==" ") and (ord(j)<128)) for i in all_videos]
    #print(all_videos_filtered)
    return all_videos_filtered


