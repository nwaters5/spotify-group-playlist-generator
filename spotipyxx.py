import os
import sys
import json
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError
import config2

def get_token(username):
    #Get username from terminal
    #username = sys.argv[1]


    #try:
    token = util.prompt_for_user_token(username, 
                                        scope='user-top-read user-library-read playlist-modify-public', 
                                        client_id=config2.client_id, 
                                        client_secret=config2.client_secret, 
                                        redirect_uri='http://127.0.0.1:5000/')
    return token
    #except:
    #    os.remove(f".cache-{username}")


    #spotifyObject = spotipy.Spotify(auth=token)