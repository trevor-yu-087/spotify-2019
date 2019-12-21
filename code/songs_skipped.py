import json
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

with open('StreamingHistory0.json', encoding='utf8') as json_file:
    stream_history_0 = json.load(json_file)
with open('StreamingHistory1.json', encoding='utf8') as json_file:
    stream_history_1 = json.load(json_file)
with open('StreamingHistory2.json', encoding='utf8') as json_file:
    stream_history_2 = json.load(json_file)

df0 = pd.DataFrame.from_dict(stream_history_0)
df1 = pd.DataFrame.from_dict(stream_history_1)
df2 = pd.DataFrame.from_dict(stream_history_2)

df_sh = pd.concat([df0,df1,df2],ignore_index=True)
#print(df_sh)


df_2019 = df_sh[df_sh.endTime > '2019-01-01']
df_2019.reset_index(inplace=True,drop=True)
#print(df_2019)
listening_time_2019_o = df_2019['msPlayed'].astype('int').sum() / 1000 / 60
mean_playtime_o = df_2019['msPlayed'].astype('int').agg('mean') / 1000 / 60
unique_songs_o = df_2019[df_2019.endTime < '2019-12-07'].drop_duplicates(subset=['artistName', 'trackName']).shape[0]
print('Unique songs: ',unique_songs_o)
print('Mean playtime per song: {0:.2f} min'.format(mean_playtime_o))
print('Listening time in 2019: {0:.0f} min'.format(listening_time_2019_o))

print()
print('Removing songs played for less than 1 second: ')
print()
# Remove songs with less than 1 second play time
df_nskp = df_2019[df_2019.msPlayed > 1000].reset_index(drop=True)
unique_songs = df_nskp.drop_duplicates(subset=['artistName','trackName']).shape[0]
listening_time_2019 = df_nskp['msPlayed'].astype('int').sum() / 1000 / 60
mean_playtime = df_nskp.msPlayed.astype('int').agg('mean') / 1000 / 60
print('Unique songs: ',unique_songs)
print('Mean playtime per song: {0:.2f} min'.format(mean_playtime))
print('Listening time in 2019: {0:.0f} min'.format(listening_time_2019))

print()
print('Removing songs played for less than 5 seconds: ')
print()
# Remove songs with less than 5 second play time
df_nskp = df_2019[df_2019.msPlayed > 5000].reset_index(drop=True)
df_skp = df_2019[df_2019.msPlayed <= 5000].reset_index(drop=True)
unique_songs = df_nskp.drop_duplicates(subset=['artistName','trackName']).shape[0]
listening_time_2019 = df_nskp['msPlayed'].astype('int').sum() / 1000 / 60
mean_playtime = df_nskp.msPlayed.astype('int').agg('mean') / 1000 / 60
print('Unique songs: ',unique_songs)
print('Mean playtime per song: {0:.2f} min'.format(mean_playtime))
print('Listening time in 2019: {0:.0f} min'.format(listening_time_2019))
print('Number of songs skipped: {}'.format(df_skp.msPlayed.size))
print('Unique songs skipped: {}'.format(unique_songs_o-unique_songs))

# Find skipped songs that were not in my library
with open('YourLibrary.json', encoding='utf8') as json_file:
    library = json.load(json_file)

df_lib = pd.DataFrame.from_dict(library)
df_nlib = df_skp[~df_skp.trackName.isin(df_lib.track)].drop_duplicates(subset=['artistName', 'trackName']).reset_index(drop=True)
# print('Songs not in library: ')
# print(df_nlib.trackName)
# print()

# Find most skipped songs
skipped = df_skp.groupby(by=['trackName','artistName']).agg('count')['msPlayed'].sort_values(ascending=False)
print('Most skipped songs: ')
print(skipped[:20])
print(skipped.filter(like='Shawn Mendes')[:5])
print()

# For making distribution plot to find out where most songs are skipped
# df_skp = df_nskp[df_nskp.msPlayed < 600000]
# ax = sns.distplot(df_skp.msPlayed)
# plt.show()

df_lib_artists = df_lib.drop_duplicates(subset=['track', 'artist']).reset_index(drop=True)
print(df_lib_artists[df_lib_artists.artist == 'Shawn Mendes'].head(10))
df_2019['inLibrary'] = False
df_2019.loc[(df_2019.trackName.isin(df_lib_artists.track)) & (df_2019.artistName.isin(df_lib_artists.artist)),'inLibrary'] = True

df_nlib = df_2019[df_2019.inLibrary == False].groupby(by=['trackName', 'artistName']).agg('count')['msPlayed'].sort_values(ascending=False)
print('Songs not in library by playcount: ')
print(df_nlib[:20])
print()

# Adding albums to dataframe
df_2019 = pd.merge(df_2019, df_lib_artists[['artist','track','album']],how='left', left_on=['artistName','trackName'], right_on=['artist','track'])
# Consolidate all the musicals into the same artist / album
df_2019.loc[df_2019.album == 'Dear Evan Hansen (Original Broadway Cast Recording)','album'] = 'Dear Evan Hansen (Broadway Cast Recording)'
df_2019.loc[df_2019.album == 'Dear Evan Hansen (Broadway Cast Recording)','artist'] = 'Dear Evan Hansen Original Broadway Cast'
df_2019.loc[df_2019.album == 'Hamilton', 'artist'] = 'Hamilton Original Broadway Cast'

top_albums = df_2019.groupby(by=['album', 'artist']).agg('sum')['msPlayed'].sort_values(ascending=False) /1000 / 60 / 60
print('Top albums by play time (hours) ')
print(top_albums[:20])

