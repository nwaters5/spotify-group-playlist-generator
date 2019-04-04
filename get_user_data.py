import scrape_user_library as scrape

def get_user_data(username):
    s = scrape.ScrapeUserLibrary(username)
    #library = s.get_library_df()
    playlists = s.get_playlist_df()
    top_tracks = s.get_top_tracks()
    return playlists, top_tracks



