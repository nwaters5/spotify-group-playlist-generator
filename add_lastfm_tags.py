import pandas as pd
import pylast

def get_tags(artist, song):
    track = network.get_track(artist, song)
    topItems = track.get_top_tags(limit=None)
    d = {}
    for topItem in topItems:
        d.update({topItem.item.get_name(): topItem.weight})    
    return d

def add_features_to_df(df):
    for i, row in df.iterrows():
        d = get_tags(row['artist'], row['track'])
        for key, value in d.items():
            df.at[i, key] = value
    return df
