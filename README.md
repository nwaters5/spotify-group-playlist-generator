# Overlap: Spotify Two User Playlist Generator
Spotify is a great music streaming platform. It is especially great at recommending new music to the user based on his/her listening habits and musical taste. One thing Spotify lacks is this recommendation system, but for multiple users. Using data science and machine learning, Overlap finds the overlapping tastes of two Spotify users and creates a playlist of recommended songs.

## How it Works (Data Pipeline):
On the web app, two users log into their Spotify accounts. Both users’ libraries, playlists, and top tracks are scraped. A cosine similarity recommendation model is then built based on these songs. Based on his/her top tracks, user 1 is recommended songs from user 2’s playlists, and vice versa. From there, based on these recommended songs, more songs are recommended that neither user has heard before (the algorithm checks if each recommendation is already in either user’s library/playlists) . These recommendations are pulled from a Nearest Neighbors model derived from a self-built diverse dataset of 80,000 songs. 
Finally, a playlist of these tracks is created in both users’ Spotify accounts.

## Data Understanding:
Genre tags of the artists (provided by Spotify’s API) and user-generated genre tags for each track (from Last.fm’s API) were utilized as features. 
The following audio features were also used for each track (Spotify’s API): danceability, energy, valence, speechiness, tempo, instrumentalness, acousticness, liveness, popularity.

## Modeling
- Cosine similarity content-based recommendation system (between users’ libraries)
- Nearest Neighbors Model (for recommendations from the big dataset)

## In the Near Future:
At the moment, the app takes in two users. The next step is to integrate a third or fourth user, which is currently in the works.

