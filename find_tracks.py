import spotipy, config
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from search_song import get_list_of_playlist_items

def sp_setup():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config.sp_client_id,
        client_secret=config.sp_client_secret, redirect_uri="http://localhost:8888/callback", scope="playlist-modify-public"))
    return sp


def get_tracks_sp(yt_playlist_id):
    music = get_list_of_playlist_items(yt_playlist_id)
    bug_songs, track_ids = [], []
    spotifyObject = sp_setup()
    #print(spotifyObject.search(q="album:" + "Dua Lipa  Levitating Featuring DaBaby Official Music Video", type="album", limit=10))
    for j in music:

        searchResults = spotifyObject.search(q="track:" + j, type="track", limit=10)
        #print(j)
        if searchResults['tracks']['items'] != []:
            for i in searchResults['tracks']['items']:
                #print(f"https://open.spotify.com/track/{i['id']}")
                track_ids.append(i['id'])
                break
        else:
            bug_songs.append(j)
    track_ids = ["spotify:track:" + track for track in track_ids]
    return track_ids, len(music)-len(bug_songs)