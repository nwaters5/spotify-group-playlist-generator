import scrape_user_library as scrape

def get_user_data(username):
    s = scrape.ScrapeUserLibrary(username)
    library = s.get_library_df()
    top_tracks = s.get_top_tracks()
    return library, top_tracks



