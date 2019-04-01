import spotipy
import spotipy.util as util
import pandas as pd
import spotipyxx
token = spotipyxx.get_token()
sp = spotipy.Spotify(auth=token)


class ScrapeUserLibrary(object):
    
    #initialize tokens
    def __init__(self):
        token = spotipyxx.get_token()
        sp = spotipy.Spotify(auth=token)
    #return all saved tracks
    def get_library_df(self):
        #sp = spotipy.Spotify(auth=self.token)
        results = sp.current_user_saved_tracks(limit=50, offset=0)
        i = -50
        library_df = pd.DataFrame({'artist': [], 'artist_uri': [], 'track': [], 'track_uri': []})
        while len(results['items']) > 0:
            artists = []
            artist_uris = []
            tracks = []
            track_uris = []
            i +=50
            results = sp.current_user_saved_tracks(limit=50, offset=i)
            for item in results['items']:
                track = item['track']
                artists.append(track['artists'][0]['name'])
                artist_uris.append(track['artists'][0]['uri'])
                tracks.append(track['name'])
                track_uris.append(track['uri'])
            library_df = pd.concat([library_df, pd.DataFrame({'artist': artists, 'artist_uri': artist_uris, 'track': tracks, 'track_uri': track_uris})])
        library_df = library_df.reset_index()
        return library_df

    #return all tracks from all playlists
    def get_playlist_df(self):
        #sp = spotipy.Spotify(auth=self.token)
        def show_tracks(tracks):
            for item in tracks['items']:
                track = item['track']
                p_artists.append(track['artists'][0]['name'])
                p_artist_uris.append(track['artists'][0]['uri'])
                p_tracks.append(track['name'])
                p_track_uris.append(track['uri'])
        p_artists = []
        p_artist_uris = []
        p_tracks = []
        p_track_uris = []
        playlists = sp.user_playlists('nwaters5')
        for playlist in playlists['items']:
            if playlist['owner']['id'] == 'nwaters5':
                results = sp.user_playlist('nwaters5',  playlist['id'],
                            fields="tracks,next")
                tracks = results['tracks']
                show_tracks(tracks)
                while tracks['next']:
                    tracks = sp.next(tracks)
                    show_tracks(tracks)
        playlist_df = pd.DataFrame({'artist': p_artists, 'artist_uri': p_artist_uris, 'track': p_tracks, 'track_uri': p_track_uris})
        return playlist_df

    #return df with new features: dance, energy, valence
    def get_feature_columns(self, df, column_name='track_uri'):
        #sp = spotipy.Spotify(auth=self.token)
        features = ['danceability', 'energy', 'valence']
        for i in features:
            df[i] = df[column_name].apply(lambda x: get_audio_features(x, i))
        return df
    
    #return a track's audio features
    def get_audio_features(x, key):
        return sp.audio_features(x)[0][key]

    
    #return top 98 artists
    def get_top_artists(self):
        #sp = spotipy.Spotify(auth=self.token)
        artists = []
        artist_uris = []
        results = sp.current_user_top_artists(limit=49, offset=0, time_range="long_term")
        i = 0
        while len(results['items']) > 0:
            for item in results['items']:
                artists.append(item['name'])
                artist_uris.append(item['uri'])
            i += 49
            results = sp.current_user_top_artists(limit=49, offset=i, time_range="long_term")
        return pd.DataFrame({'artists': artists, 'artist_uris': artist_uris})

    #return top 98 tracks
    def get_top_tracks(self):
        #sp = spotipy.Spotify(auth=self.token)
        tracks = []
        track_uris = []
        results = sp.current_user_top_tracks(limit=49, offset=0, time_range="long_term")
        i = 0
        while len(results['items']) > 0:
            for item in results['items']:
                tracks.append(item['name'])
                track_uris.append(item['uri'])
            i +=49
            results = sp.current_user_top_tracks(limit=49, offset=i, time_range="long_term")
        return pd.DataFrame({'tracks': tracks, 'track_uris': track_uris})



