import pandas as pd
import pylast

username = "dummy_account_5"
password_hash = pylast.md5("dummypassword1!")
network = pylast.LastFMNetwork(api_key='81cc770a8ced77585a1b0b2dd5e453bd', api_secret='b3510a11c6c0a885f979545db0610e23',
                               username=username, password_hash=password_hash)

def get_tags(artist, song):
    track = network.get_track(artist, song)
    topItems = track.get_top_tags(limit=10)
    d = {}
    for topItem in topItems:
        if "".join((str(topItem.item.get_name()).lower()).split()) != "".join((str(artist).lower()).split()):
            d.update({topItem.item.get_name(): topItem.weight})    
    return d

def add_features_to_df(df):
    for i, row in df.iterrows():
        d = get_tags(row['artist'], row['track'])
        for key, value in d.items():
            df.at[i, key] = value
    return df.fillna(0)
