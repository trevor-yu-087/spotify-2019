import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

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


# Looking at time series for specific artists
df_shawn = df_2019[df_2019['artistName']=='Shawn Mendes'].reset_index()
#print(df_shawn)
df_shawn = df_shawn.set_index(pd.DatetimeIndex(df_shawn['endTime']))
time_series_shawn = df_shawn['endTime'].resample('D').count()
print(time_series_shawn.iloc[300:330])

df_wdw = df_2019[df_2019['artistName']=='Why Don\'t We'].reset_index()
df_wdw = df_wdw.set_index(pd.DatetimeIndex(df_wdw['endTime']))
time_series_wdw = df_wdw['endTime'].resample('D').count()

fig, ax = plt.subplots(figsize=(20,10))
ax = sns.lineplot(x=time_series_shawn.index, y=time_series_shawn.values, color='g', label='Shawn Mendes')
ax = sns.lineplot(x=time_series_wdw.index, y=time_series_wdw.values,color='r',label='Why Don\'t We')

for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(15)
for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(15)
plt.setp(ax.lines,linewidth=2)  # set lw for all lines of g axes
plt.ylabel("Times listened (daily)", fontsize=20)
plt.xlabel('Month of the year', fontsize=20)
plt.title('Daily scrobbles through the year by artist', fontsize=25)
plt.legend(prop={'size': 20}, loc='best')
sns.despine()
plt.show()

# Accumulation plots
time_series_shawn = df_shawn['endTime'].resample['D'].count().cumsum()
time_series_wdw = df_wdw['endTime'].resample['D'].count().cumsum()

# compensate for null days in the end if series is does not go to last date

# pictures function
def add_pic(path, xy, ax):
    arr_img = plt.imread(path, format='jpg')
    imagebox = OffsetImage(arr_img, zoom=0.2)
    imagebox.image.axes = ax
    ab = AnnotationBbox(imagebox, xy,
                        xybox=(120., -80.),
                        xycoords='data',
                        boxcoords="offset points",
                        pad=0.5,
                        frameon=False,
                        )
    ax.add_artist(ab)

