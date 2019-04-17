import pickle

# import spotify_requests
import pandas as pd
from flask import Flask, request, render_template, jsonify, redirect, g, session
import create_two_user_playlist
import json
import requests
import spotipy
from urllib.parse import quote
import config2

app = Flask(__name__, static_url_path="")


#  Client Keys
CLIENT_ID = config2.client_id
CLIENT_SECRET = config2.client_secret

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
SCOPE = "user-top-read user-library-read playlist-modify-public"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID,
}


@app.route("/home")
def home():
    with open("templates/user_info/status.txt", "w") as status:
        status.write("0")
    return render_template("index.html")


@app.route("/")
def index():
    """Return the main page."""
    return render_template("index.html")


@app.route("/auth")
def auth():
    url_args = "&".join(
        ["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()]
    )
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    # get_token('3z9j4o0pa8xlbipzbhgz9om44')
    # return get_token('nwaters5')
    return redirect(auth_url, code=307)


@app.route("/callback/q")
def callback():
    # Auth Step 4: Requests refresh and access tokens

    auth_token = request.args["code"]
    # print("http://127.0.0.1:8081/callback/q?code=" + auth_token)
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)
    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    sp = spotipy.Spotify(auth=response_data["access_token"])
    display_name = sp.current_user()["display_name"]
    with open("templates/user_info/status.txt", "r") as s:
        stat = s.read()
    if stat == "1":
        with open("templates/user_info/status.txt", "w") as status:
            status.write("2")
        with open("templates/user_info/token2.txt", "w") as text:
            text.write(response_data["access_token"])
        with open("templates/user_info/user2.txt", "w") as user:
            user.write(display_name)
    elif stat == "2":
        with open("templates/user_info/status.txt", "w") as status:
            status.write("3")
        with open("templates/user_info/token1.txt", "w") as text:
            text.write(response_data["access_token"])
        with open("templates/user_info/user1.txt", "w") as user:
            user.write(display_name)
    elif stat == "3":
        with open("templates/user_info/status.txt", "w") as status:
            status.write("2")
        with open("templates/user_info/token2.txt", "w") as text:
            text.write(response_data["access_token"])
        with open("templates/user_info/user2.txt", "w") as user:
            user.write(display_name)
    else:
        with open("templates/user_info/status.txt", "w") as status:
            status.write("1")
        with open("templates/user_info/token1.txt", "w") as text:
            text.write(response_data["access_token"])
        with open("templates/user_info/user1.txt", "w") as user:
            user.write(display_name)

    return redirect("http://127.0.0.1:8081/")


@app.route("/get_users", methods=["GET", "POST"])
def get_users():
    with open("templates/user_info/user2.txt", "r") as user:
        user2 = user.read()
    with open("templates/user_info/user1.txt", "r") as user:
        user1 = user.read()
    with open("templates/user_info/status.txt", "r") as s:
        stat = s.read()
    return jsonify({"user1": user1, "user2": user2, "status": stat})


@app.route("/predict", methods=["GET", "POST"])
def predict():
    """Return a random prediction."""
    with open("templates/user_info/token1.txt", "r") as x:
        tok1 = x.read()
    with open("templates/user_info/token2.txt", "r") as y:
        tok2 = y.read()

    print("creating...")
    data = request.json
    create_two_user_playlist.create(
        token1=tok1, token2=tok2, playlist_name=data["user_input3"]
    )
    with open("templates/user_info/status.txt", "w") as status:
        status.write("0")
    return jsonify({"pred": "Done!"})
    # return jsonify({'prob': 100 * round(prediction[0][1], 1)})


# import random
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.pipeline import Pipeline
if __name__ == "__main__":
    app.run(debug=True, port=PORT)
