import pickle
import pandas as pd
from flask import Flask, request, render_template, jsonify
import create_two_user_playlist
#with open('spam_model.pkl', 'rb') as f:
#    model = pickle.load(f)
app = Flask(__name__, static_url_path="")


@app.route('/')
def index():
    """Return the main page."""
    hello_message = 'hello welcome to the spam thing'
    return render_template('index.html', hello_message=hello_message)

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
