import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


with open('../library/StreamingHistory0.json', encoding='utf8') as json_file:
    stream_history_0 = json.load(json_file)
with open('../library/StreamingHistory1.json', encoding='utf8') as json_file:
    stream_history_1 = json.load(json_file)
with open('../library/StreamingHistory2.json', encoding='utf8') as json_file:
    stream_history_2 = json.load(json_file)

df0 = pd.DataFrame.from_dict(stream_history_0)
df1 = pd.DataFrame.from_dict(stream_history_1)
df2 = pd.DataFrame.from_dict(stream_history_2)

df_sh = pd.concat([df0,df1,df2],ignore_index=True)
#print(df_sh)

unique_songs = df_sh[df_sh.endTime < '2019-12-07'].drop_duplicates(subset=['artistName', 'trackName']).shape[0]
print('Unique songs: ',unique_songs)
listening_time = df_sh['msPlayed'].astype('int').sum() / 1000 / 60
print('Listening time: {0:.0f} min'.format(listening_time))

df_2019 = df_sh[df_sh.endTime > '2019-01-01']
df_2019.reset_index(inplace=True,drop=True)
#print(df_2019)
listening_time_2019 = df_2019['msPlayed'].astype('int').sum() / 1000 / 60
#mean_playtime = listening_time_2019/df_2019.shape[0]
mean_playtime = df_2019['msPlayed'].astype('int').agg('mean') / 1000 / 60
print('Mean playtime per song: {0:.2f} min'.format(mean_playtime))
print('Listening time in 2019: {0:.0f} min'.format(listening_time_2019))
#print(df_2019.iloc[-2980])
lt_spotify = df_2019['msPlayed'].iloc[0:-2980].astype('int').sum() / 1000 / 60
print('Listening time up to {0}: {1:.0f} min'.format(df_2019.endTime.iloc[-2980],lt_spotify))
print('\n')

top_listened = df_2019.groupby(by=['artistName']).agg('sum')['msPlayed'].sort_values(ascending=False)[:20]
top_listened = top_listened / 1000 / 60 / 60
print(top_listened)
print('\n')

top_artists_by_count = df_2019.groupby(by=['artistName']).agg('count')['trackName'].sort_values(ascending=False)[:20]
print(top_artists_by_count)
print('\n')

top_songs = df_2019.groupby(by=['trackName','artistName']).agg('count')['msPlayed'].sort_values(ascending=False)[:30]
#top_100_songs = top_songs = df_2019.groupby(by=['trackName','artistName']).agg('count')['msPlayed'].sort_values(ascending=False)[:100]
#export_csv = top_100_songs.to_csv(r'C:\Users\trevo\Documents\my_spotify_data\top_100.csv',index=True,header=True)
print(top_songs)

# Looking at Jan 1 to Oct 31 as time where spotify does analysis
print()
print('--------------------------------')
print()
print('Stats according to Spotify from Jan 1 2019 to Oct 31 2019: \n')
df_spotify = df_2019[df_2019.endTime < '2019-11-01']
# print(df_spotify)
listening_time = df_spotify['msPlayed'].astype('int').sum() / 1000 / 60
#mean_playtime = listening_time_2019/df_spotify.shape[0]
mean_playtime = df_spotify['msPlayed'].astype('int').agg('mean') / 1000 / 60
print('Mean playtime per song: {0:.2f} min'.format(mean_playtime))
print('Listening time in 2019 according to Spotify: {0:.0f} min'.format(listening_time_2019))

top_listened = df_spotify.groupby(by=['artistName']).agg('sum')['msPlayed'].sort_values(ascending=False)
top_listened = top_listened / 1000 / 60 / 60
print(top_listened[:30])
print('\n')

top_artists_by_count = df_spotify.groupby(by=['artistName']).agg('count')['trackName'].sort_values(ascending=False)[:20]
print(top_artists_by_count)
print('\n')

top_songs = df_2019.groupby(by=['trackName','artistName']).agg('count')['msPlayed'].sort_values(ascending=False)[:30]
#top_100_songs = top_songs = df_2019.groupby(by=['trackName','artistName']).agg('count')['msPlayed'].sort_values(ascending=False)[:100]
#export_csv = top_100_songs.to_csv(r'C:\Users\trevo\Documents\my_spotify_data\top_100.csv',index=True,header=True)
print(top_songs)
