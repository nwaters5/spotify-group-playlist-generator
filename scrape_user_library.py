import spotipy
import spotipy.util as util
import pandas as pd
import spotipyxx
import add_lastfm_tags as tags
#token = spotipyxx.get_token()
#sp = spotipy.Spotify(auth=token)


class ScrapeUserLibrary(object):
    
    #initialize tokens
    def __init__(self, username):
        token = spotipyxx.get_token(username)
        self.sp = spotipy.Spotify(auth=token)
        self.user = username
    
    #return all saved tracks
    def get_library_df(self):
        #sp = spotipy.Spotify(auth=self.token)
        results = self.sp.current_user_saved_tracks(limit=50, offset=0)
        i = -50
        library_df = pd.DataFrame({'artist': [], 'track': []})
        while len(results['items']) > 0:
            artists = []
            #artist_uris = []
            tracks = []
            #track_uris = []
            i +=50
            results = self.sp.current_user_saved_tracks(limit=50, offset=i)
            for item in results['items']:
                track = item['track']
                artists.append(track['artists'][0]['name'])
                #artist_uris.append(track['artists'][0]['uri'])
                tracks.append(track['name'])
                #track_uris.append(track['uri'])
            library_df = pd.concat([library_df, pd.DataFrame({'artist': artists, 'track': tracks})])
        library_df.reset_index(inplace=True)
        library_df['track'] = library_df['track'].str.split(" - ", expand=True)[0]
        library_df.drop(columns='index', inplace=True)
        return tags.add_features_to_df(library_df)

    #return all tracks from all playlists
    def get_playlist_df(self):
        #sp = spotipy.Spotify(auth=self.token)
        def show_tracks(tracks):
            for item in tracks['items']:
                track = item['track']
                p_artists.append(track['artists'][0]['name'])
                #p_artist_uris.append(track['artists'][0]['uri'])
                p_tracks.append(track['name'])
                p_track_uris.append(track['uri'])
        p_artists = []
        #p_artist_uris = []
        p_tracks = []
        p_track_uris = []
        playlists = self.sp.user_playlists(self.user)
        for playlist in playlists['items']:
            if playlist['owner']['id'] == self.user:
                results = self.sp.user_playlist(self.user,  playlist['id'],
                            fields="tracks,next")
                tracks = results['tracks']
                show_tracks(tracks)
                while tracks['next']:
                    tracks = self.sp.next(tracks)
                    show_tracks(tracks)
        playlist_df = pd.DataFrame({'artist': p_artists, 'track': p_tracks, 'track_uri': p_track_uris})
        playlist_df['track'] = playlist_df['track'].str.split(" - ", expand=True)[0]
        repeats = playlist_df['track_uri'].value_counts()
        playlist_df['repeats'] = playlist_df['track_uri'].apply(lambda x: repeats[x])
        playlist_df.drop_duplicates(inplace=True)
        playlist_df.reset_index(inplace=True)
        playlist_df.drop(columns=['index', 'track_uri'], inplace=True)
        return tags.add_features_to_df(playlist_df)
    
    #return a track's audio features
    def get_audio_features(self, x, key):
        return self.sp.audio_features(x)[0][key]
    
    #return df with new features: dance, energy, valence
    def get_feature_columns(self, df, column_name='track_uri'):
        #sp = spotipy.Spotify(auth=self.token)
        features = ['danceability', 'energy', 'valence']
        for i in features:
            df[i] = df[column_name].apply(lambda x: self.get_audio_features(x, i))
        return df
    
    #return top 98 artists
    def get_top_artists(self):
        #sp = spotipy.Spotify(auth=self.token)
        artists = []
        artist_uris = []
        results = self.sp.current_user_top_artists(limit=49, offset=0, time_range="long_term")
        i = 0
        while len(results['items']) > 0:
            for item in results['items']:
                artists.append(item['name'])
                artist_uris.append(item['uri'])
            i += 49
            results = self.sp.current_user_top_artists(limit=49, offset=i, time_range="long_term")
        return pd.DataFrame({'artists': artists, 'artist_uri': artist_uris})

    #return top 98 tracks
    def get_top_tracks(self):
        #sp = spotipy.Spotify(auth=self.token)
        tracks = []
        #track_uris = []
        artists = []
        #artist_uris = []
        results = self.sp.current_user_top_tracks(limit=49, offset=0, time_range="long_term")
        i = 0
        while len(results['items']) > 0:
            for item in results['items']:
                tracks.append(item['name'])
                #track_uris.append(item['uri'])
                artists.append(item['artists'][0]['name'])
                #artist_uris.append(item['artists'][0]['uri'])
            i +=49
            results = self.sp.current_user_top_tracks(limit=49, offset=i, time_range="long_term")
        top_artists_df = pd.DataFrame({'artist': artists, 'track': tracks})
        top_artists_df['track'] = top_artists_df['track'].str.split(" - ", expand=True)[0]
        return tags.add_features_to_df(top_artists_df)

