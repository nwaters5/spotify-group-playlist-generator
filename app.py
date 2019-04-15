import pickle
#import spotify_requests
import pandas as pd
from flask import Flask, request, render_template, jsonify, redirect, g, session
import create_two_user_playlist
import json
import requests
from urllib.parse import quote
from spotipyxx import get_token

app = Flask(__name__, static_url_path="")


#  Client Keys
CLIENT_ID = "d29da1b2960d474b81e33a87e9ad8cc2"
CLIENT_SECRET = "851d00bc1b714cc38ec62a301b8b8eae"

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8081
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}


@app.route('/')
def index():
    """Return the main page."""
    return render_template('index.html')



@app.route('/auth')
def auth():
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    print(auth_url)
    return redirect(auth_url, code=307)



@app.route("/callback/q")
def callback():
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Return a random prediction."""
    print("creating...")
    data = request.json
    create_two_user_playlist.create(user1=data['user_input'], user2=data['user_input2'], playlist_name=data['user_input3'])
    return jsonify({'pred': 'Done!'})
    # return jsonify({'prob': 100 * round(prediction[0][1], 1)})

# import random
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.pipeline import Pipeline
if __name__ == "__main__":
    app.run(debug=True, port=PORT)