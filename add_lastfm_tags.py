import pandas as pd
import pylast

username = "dummy_account_5"
password_hash = pylast.md5("dummypassword1!")
network = pylast.LastFMNetwork(
    api_key="52557fe79157ddf53597b835faa25f92",
    api_secret="3a018cc75468cadeaa9fbfa4604dba5e",
    username=username,
    password_hash=password_hash,
)

# returns dictionary of top 10 tags of artist and their weight
def get_tags(artist, song):
    track = network.get_track(artist, song)
    topItems = track.get_top_tags(limit=8)
    d = {}
    for topItem in topItems:
        if "".join((str(topItem.item.get_name()).lower()).split()) != "".join(
            (str(artist).lower()).split()
        ):
            item_clean = "".join(
                topItem.item.get_name().lower().replace("-", "").split()
            )
            d.update({item_clean: topItem.weight})
    return d


# adds the top tags to dataframe
def add_features_to_df(df):
    for i, row in df.iterrows():
        try:
            d = get_tags(row["artist"], row["track"])
        except:
            continue
        for key, value in d.items():
            df.at[i, key] = value
    # drops uncommon columns
    for column in df:
        if df[column].count() <= 1:
            df.drop(columns=column, inplace=True)
    return df.fillna(0)
