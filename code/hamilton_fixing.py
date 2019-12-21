import json
import pandas as pd



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
df_2019 = df_sh[df_sh.endTime > '2019-01-01'].reset_index(drop=True)

with open('YourLibrary.json', encoding='utf8') as json_file:
    library = json.load(json_file)

df_lib = pd.DataFrame.from_dict(library)
# print(df_lib)
df_hamilton = df_lib[df_lib['album']=='Hamilton'].reset_index()
lst_hamilton_songs = df_hamilton['track'].values.tolist()

hamilton_artists = ['Leslie Odom Jr.', 'Lin-Manuel Miranda', 'Renée Elise Goldsberry','Thayne Jasperson','Jonathan Groff','Phillipa Soo','Anthony Ramos','Original Broadway Cast of Hamilton','Christopher Jackson','Daveed Diggs','Jasmine Cephas-Jones','José González']

# Replace hamilton songs with hamilton artist
#df_2019 = df_2019.replace(hamilton_artists,'Hamilton')
# df_2019.loc[df_2019.trackName.isin(lst_hamilton_songs)].artistName.replace(hamilton_artists,'Hamilton')
df_2019.loc[(df_2019.trackName.isin(lst_hamilton_songs) & (df_2019.artistName.isin(hamilton_artists))),'artistName'] = 'Hamilton'
# print(df_2019.artistName[-20:-10])
# df_hamilton = df_2019[df_2019['artistName'] == 'Hamilton']
# print(df_hamilton)
# hamilton_mins = df_hamilton.msPlayed.astype('int').agg('sum') / 1000 / 60
hamilton_mins = df_2019.loc[df_2019.artistName == 'Hamilton','msPlayed'].astype('int').agg('sum') / 1000 / 60
print('Minutes of Hamilton Listened to: {0:.0f} min'.format(hamilton_mins))
print()

top_listened = df_2019.groupby(by=['artistName']).agg('sum')['msPlayed'].sort_values(ascending=False)[:20]
top_listened = top_listened / 1000 / 60 / 60
print('Top artists by listening time (h):')
print(top_listened)
print()

top_artists_by_count = df_2019.groupby(by=['artistName']).agg('count')['trackName'].sort_values(ascending=False)[:20]
print('Top artists by play count:')
print(top_artists_by_count)
print()

print('--------------')
print()
print('Adjusting for Oct 31st stop time: ')

df_spotify = df_2019[df_2019.endTime < '2019-11-01']
# print(df_spotify)
listening_time = df_spotify['msPlayed'].astype('int').sum() / 1000 / 60
mean_playtime = df_spotify['msPlayed'].astype('int').agg('mean') / 1000 / 60
print('Mean playtime per song: {0:.2f} min'.format(mean_playtime))
print('Listening time in 2019 according to Spotify: {0:.0f} min'.format(listening_time))

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