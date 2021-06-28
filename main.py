from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Parameters
CLIENT_ID = YOUR_SPOTIFY_CLIENT_ID
CLIENT_SECRET = YOUR_SPOTIFY_CLIENT_SECRET
REDIRECT_URI = "http://example.com"
SCOPE = "playlist-modify-private"

# Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(scope=SCOPE, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI,
                              cache_path="token.txt"))
user_id = sp.me()["id"]

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

# Makes a request to the webpage and stores the response text in a variable named data.
response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}")
data = response.text

# Creates an array of all the song titles on the webpage.
soup = BeautifulSoup(data, "html.parser")
songs = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
song_titles = [song.getText() for song in songs]

# Stores the year received from the user input.
year = date.split("-")[0]

# Spotify URI is a resource identifier that can be used to locate an artist,album or track.
song_uris = []

# Searches through Spotify for the song titles and stores their corresponding URIs in the array above.
for song in song_titles:
    search = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = search["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped!")

# Creates a private playlist of all the songs that were found on Spotify.
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
