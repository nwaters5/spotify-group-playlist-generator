import pandas as pd
import pylast

username = "dummy_account_5"
password_hash = pylast.md5("dummypassword1!")
network = pylast.LastFMNetwork(api_key='ba7e56c3cc988219ffb50a6dede0093a', api_secret='4fcfea7e8068651b411f5e343ce718f5',
                               username=username, password_hash=password_hash)

#returns dictionary of top 10 tags of artist and their weight
def get_tags(artist):
    band = network.get_artist(artist)
    topItems = band.get_top_tags(limit=10)
    d = {}
    for topItem in topItems:
        if "".join((str(topItem.item.get_name()).lower()).split()) != "".join((str(artist).lower()).split()):
            item_clean = "".join(topItem.item.get_name().lower().replace("-", "").split())
            d.update({item_clean: topItem.weight})    
    return d

#adds the top tags to dataframe
def add_features_to_df(df):
    for i, row in df.iterrows():
        try:
            d = get_tags(row['artist'])
        except:
            continue    
        for key, value in d.items():
            df.at[i, key] = value
    #drops uncommon columns
    for column in df:
        if df[column].count() <= 1:
            df.drop(columns=column, inplace=True)
    return df.fillna(0)
