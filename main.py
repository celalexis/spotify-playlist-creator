from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
SPOTIPY_REDIRECT_URI = os.environ["SPOTIPY_REDIRECT"]


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=SPOTIPY_REDIRECT_URI,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

travel_to = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{travel_to}")
billboard_webpage = response.text
soup = BeautifulSoup(billboard_webpage, "html.parser")
songs_span = soup.find_all(name="span", class_="chart-element__information__song")
song_titles = [song.getText() for song in songs_span]

song_uris = []
year = travel_to.split("-")[0]
for song in song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{travel_to} Radio Hits",
    public=False,
    collaborative=False,
    description="Time to boogie.")

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)









