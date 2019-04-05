import os
import sys
import json
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError


def get_token(username):
    #Get username from terminal
    #username = sys.argv[1]


    #try:
    token = util.prompt_for_user_token(username, 
                                        scope='user-top-read user-library-read playlist-modify-public', 
                                        client_id='87e89d824a3046ad9d2c6fcf05931cab', 
                                        client_secret='e9001d177fcb4071bad33987520f5f16', 
                                        redirect_uri='http://127.0.0.1:5000/')
    return token
    #except:
    #    os.remove(f".cache-{username}")


    #spotifyObject = spotipy.Spotify(auth=token)