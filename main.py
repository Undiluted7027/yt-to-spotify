import requests, os, spotipy, config
from bs4 import BeautifulSoup
import google_auth_oauthlib.flow, googleapiclient.discovery, googleapiclient.errors
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from find_tracks import get_tracks_sp, sp_setup


def user_playlists_sp(queried_playlist, spotifyObject):
    playlists_sp = spotifyObject.current_user_playlists(limit=50)
    for playlist in playlists_sp['items']:
        if playlist['name'] == queried_playlist:
            print(playlist)
            return playlist['id'], playlist['tracks']['total']


def create_playlist(sp_username="your_sp_user_id", yt_playlist_id="your_yt_playlist_id"):
    spotifyObject, desc = sp_setup(), ""
    yt_playlist_id = input("Enter YouTube Public Playlist ID:")
    ids_of_tracks = get_tracks_sp(yt_playlist_id)
    name_of_playlist = input("Enter name of new Spotify Playlist (Enter 0 for adding songs to existing playlist and 1 to create new playlist but not add songs in it)\n Note: You need ID of existing playlist\n")
    if name_of_playlist == "0":
        name_of_playlist = input("Enter name of existing playlist: ")
        queried_playlist_id = user_playlists_sp(name_of_playlist, spotifyObject)
        #playlist_id = input("Enter playlist ID")
        existing_playlist = spotifyObject.user_playlist_add_tracks(sp_username, queried_playlist_id[0], ids_of_tracks[0], position=queried_playlist_id[1])
    elif name_of_playlist == "1":
        name_of_playlist = input("Enter name for new playlist (would be created without any songs):")
        desc = input("Add description if any")
        my_playlist = spotifyObject.user_playlist_create(user=sp_username, name=name_of_playlist, public=True, description=desc)
    elif name_of_playlist == "10":
        exit()
    else:
        print("This can only be done for authenticated users")
        my_playlist = spotifyObject.user_playlist_create(user=sp_username, name=name_of_playlist, public=True, description=desc)
        queried_playlist_id = user_playlists_sp(name_of_playlist, spotifyObject)
        print(ids_of_tracks)
        my_new_playlist = spotifyObject.user_playlist_add_tracks(sp_username, queried_playlist_id, ids_of_tracks[0])
        exit()
    
create_playlist()


