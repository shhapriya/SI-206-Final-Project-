# Name: Nethra Vijayakumar
import requests
import json
import unittest
import os
import sqlite3
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Initialize Spotipy with OAuth2 authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="84c4c33c4693466f985310abe2bf7abb",
                                               client_secret="875adb71f2d343478342fcdc58f85f27",
                                               redirect_uri="https://github.com/shhapriya/SI-206-Final-Project-",
                                               scope="user-library-read"))



