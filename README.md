# spotify-group-playlist-generator
App that recommends a playlist of songs for a group of people.

##Business Understanding

Compile a compatibility score for two or more people based on their Spotify accounts. Then make a playlist that the two or more people can listen to together. For this playlist, there would be customizable knobs for what kind of playlist they want.
Knobs include:
- energy (for chilling? for partying?)
- amount of new songs/songs they know

##Data Understanding
Use the following:
- Each accounts top songs/artists
- All songs in each account’s libraries and playlists
- Genres and song statistics of each song
	- Spotify provides these statistics of each song:
		- Energy, danceability, valence, etc.

##Data Preparation
Using Spotify’s API I can scrape the user’s account for the data above. I’d put this data into pandas dataframes: Top songs, Top artists, Library songs, playlist songs. I’d then add the stats of each song/artist to the dataframe.

##Modeling
I would use matrix factorization (SVD, UV) to recommend new songs that both users would like, as well as choose from the songs the users have in common. Also, songs from each other’s libraries that the other user would like and hasn’t heard before.

##Evaluation
Compare the user’s usage rates of using this playlist over spotify generated.

##Deployment
This model would be deployed through an app, through which different users can sign into Spotify. After they are signed in, the playlist and score would be generated.
