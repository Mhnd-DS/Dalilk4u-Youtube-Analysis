#!/usr/bin/env python
# coding: utf-8

# # Packages

# In[1]:


# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

#YT_Api
from googleapiclient.discovery import build
from dateutil import parser

#JSON
from IPython.display import JSON

#Data preprocessing
import pandas as pd
# Data viz packages
import seaborn as sns
sns.set(style="darkgrid", color_codes=True)
sns.set(rc={'figure.figsize':(10,8)})


import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.pyplot import figure
plt.rcParams["figure.figsize"] = (10,6)

# NLP
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#nltk.download('stopwords')
#nltk.download('punkt')
from wordcloud import WordCloud


# In[ ]:





# In[ ]:





# # YT_Api analysis for channels

# ## Configurations

# In[2]:


api_key = 'AIzaSyAz2IRFGu0JHqjnQoRCQaAuujhhY1W5djk'

channel_ids = [
    'UCOEC9Au-L_ICEFaobn6dLCA' # jihad
    ,'UCdRGxujMEeoAMwofXkfyyng' #almoasyer
    ,'UCaaFAJcOy2mgLScpIn0WYyQ' #cypher
    ,'UCoMomfFxnGHBefSFvLMU5sg' #dalilk
    ,'UCMfas8yivQ5ly46haWXdSgw' # prac is the key
    ,'UCdz-Q0Sed_yWNLcRBpg4beg'
    ]

api_service_name = "youtube"
api_version = "v3"

# Get credentials and create an API client

youtube = build(
            api_service_name, api_version,
            developerKey =api_key)


# In[3]:


request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=','.join(channel_ids)
    )
response = request.execute()
        
    
JSON(response)


# In[ ]:





# ## Get the data from the channels
# 
# **As well we will try to observe these results**

# In[25]:


def get_channel_stats(youtube, channel_ids):
       
    all_data = []
    
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=','.join(channel_ids)
    )
    response = request.execute()
    
    JSON(response)
    YT_channel_Id_inside_loop = 0
    for i in range(len(response['items'])):
        data = {'channelName': response['items'][i]['snippet']['title'],
                'subscribers': response['items'][i]['statistics']['subscriberCount'] if 
                                                response['items'][i]['statistics']['hiddenSubscriberCount'] != True 
                                                else None ,
                'views': response['items'][i]['statistics']['viewCount'],
                'totalVideos': response['items'][i]['statistics']['videoCount'],
                'playlistId': response['items'][i]['contentDetails']['relatedPlaylists']['uploads']
        }

        all_data.append(data)
        YT_channel_Id_inside_loop = YT_channel_Id_inside_loop + 1
        
    return(pd.DataFrame(all_data))


# In[138]:


channel_data = get_channel_stats(youtube, channel_ids)
channel_data


# In[139]:


numeric_cols = ['subscribers' , 'totalVideos', 'views']

channel_data[numeric_cols] = channel_data[numeric_cols].apply(pd.to_numeric, axis = 1) # errors = 'coerce'


# In[140]:


channel_data.sort_values(by='subscribers', ascending=False, na_position='last')


# In[364]:


channel_data['totalVideos'].sum()


# ## Get the data of the videos
# 
# ** the goal of the next cell is to get the JSON **

# In[142]:


request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId= 'UUaaFAJcOy2mgLScpIn0WYyQ',
        maxResults = 50
    )
response = request.execute()
    
JSON(response)


# In[143]:


def get_video_ids(youtube, playlist_id):
    
    video_ids = []
           
    next_page_token = ''
    while next_page_token is not None:
        request = youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId = playlist_id,
                    maxResults = 50,
                    pageToken = next_page_token)
        response = request.execute()

        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])

        next_page_token = response.get('nextPageToken')
        
    return video_ids


# In[426]:


request = youtube.videos().list(
    part="snippet,contentDetails,statistics",
    id='sRvDFPnu_wQ'
)
response = request.execute()

response



# In[427]:




all_video_stats = []



video_stats = {}

for video in response['items']:
    
    video_stats = { 'id' :  video['id']
                    ,'channelTitle' :  video['snippet']['channelTitle']
                    ,'title': video['snippet']['title']
                    
                   
                    
                    ,'viewCount': video['statistics']['viewCount']
                    ,'duration' : video['contentDetails']['duration']
                    ,'publishedAt': video['snippet']['publishedAt']

                            }           
    try:  
        video_stats['tags'] = video['snippet']['tags']
    except:
        
        video_stats['tags'] = None
        
    try:
        video_stats['likeCount'] = video['statistics']['likeCount']
    except:
        
        video_stats['likeCount'] = None    
        
    try:
        video_stats['commentCount'] = video['statistics']['commentCount']
    except:
        
        video_stats['commentCount'] = None   

'''  except KeyError as k:
  #print(video_stats.get('tags' , 'meeow'))
  print(k)
  k = str(k).translate({ord(letter): None for letter in " '' "})
  video_stats[k] = 'meoow888'
  '''
        
        
        


# In[428]:


print('CURRENT' , video_stats)    
all_video_stats.append(video_stats)  
print('After' , all_video_stats) 


# In[372]:


def get_video_details(youtube, video_ids):

    all_video_stats = []
    
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute()
  
    
           
        #video_stats = {}
        
        for video in response['items']:
        
            video_stats = { 'id' :  video['id']
                            ,'channelTitle' :  video['snippet']['channelTitle']
                            ,'title': video['snippet']['title']
                            ,'viewCount': video['statistics']['viewCount']
                            ,'duration' : video['contentDetails']['duration']
                            ,'publishedAt': video['snippet']['publishedAt']
            
                                    }           
            try:  
                video_stats['tags'] = video['snippet']['tags']
            except:
                
                video_stats['tags'] = None
                
            try:
                video_stats['likeCount'] = video['statistics']['likeCount']
            except:
                
                video_stats['likeCount'] = None    
                
            try:
                video_stats['commentCount'] = video['statistics']['commentCount']
            except:
                
                video_stats['commentCount'] = None   
                
                
            all_video_stats.append(video_stats)
                                           
    return pd.DataFrame(all_video_stats)


# In[361]:


# Create a dataframe with video statistics and comments from all channels

video_df = pd.DataFrame()
#comments_df = pd.DataFrame()

for i in channel_data['channelName'].unique():
    print("Getting video information from channel: " + i)
    playlist_id = channel_data.loc[channel_data['channelName']== i, 'playlistId'].iloc[0]
    video_ids = get_video_ids(youtube, playlist_id)
    print(len(video_ids))
    
    # get video data
    video_data = get_video_details(youtube, video_ids)
    print(len(video_data))
    # get comment data
    #comments_data = get_comments_in_videos(youtube, video_ids)

    # append video data together and comment data toghether
    video_df = video_df.append(video_data, ignore_index=True)
    print(len(video_df))
    #comments_df = comments_df.append(comments_data, ignore_index=True)


# In[369]:


video_df


# In[70]:


sum(channel_data['totalVideos'])


# In[119]:


channel_data


# In[120]:


video_df


# ## Data pre-processing

# In[71]:


df = video_df.copy()


# In[76]:


numeric_cols = ['viewCount' , 'likeCount' ,'commentCount']


# In[77]:


df[:10][numeric_cols]


# In[78]:


df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, axis = 1) # errors = 'coerce'


# In[79]:


df[:10][numeric_cols]


# In[80]:


df['publishedAt'][:2]


# In[81]:


df['publishedAt'] = pd.to_datetime(df['publishedAt']).dt.date


# # Feature Engineering
# 
# I want to enrich the data for further analyses, for example:
# 
# create published date column with another column showing the day in the week the video was published, which will be useful for later analysis.
# 
# convert video duration to seconds instead of the current default string format
# 
# calculate number of tags for each video
# 
# calculate comments and likes per 1000 view ratio
# 
# calculate title character length

# In[83]:


# format Publish day in the week
df['pushblishDayName'] = df['publishedAt'].apply(lambda x: x.strftime("%A")) 


# In[85]:


# convert duration to seconds from the ISO date to redable time
import isodate
df['durationSecs'] = df['duration'].apply(lambda x: isodate.parse_duration(x))
df['durationSecs'] = df['durationSecs'].astype('timedelta64[s]')


# In[ ]:


df[['durationSecs', 'duration']][:5]


# In[ ]:





# In[86]:


# Add tag counter
df['tagCount'] = df['tags'].apply(lambda x: 0 if x is None else len(x))


# In[ ]:





# In[87]:


# Comments and likes per 1000 view ratio
df['likeRatio'] = df['likeCount']/ df['viewCount'] * 1000
df['commentRatio'] = df['commentCount']/ df['viewCount'] * 1000


# In[ ]:





# In[88]:


# Title character length
df['titleLength'] = df['title'].apply(lambda x: len(x))


# In[ ]:





# In[89]:


df['Month'] = pd.to_datetime(df['publishedAt']).dt.strftime('%b')


# In[ ]:





# In[90]:


df[:2]


# In[91]:


video_df = df.copy()


# # EDA

# In[92]:


from bidi.algorithm import get_display
import matplotlib.pyplot as plt
import arabic_reshaper
sns.set_theme(style="whitegrid")


# In[93]:


#video_df['title'] = video_df['title'].apply( lambda x :get_display(arabic_reshaper.reshape(x)))


# In[94]:


video_df['channelTitle'] = video_df['channelTitle'].apply( lambda x :get_display(arabic_reshaper.reshape(x)))


# In[95]:


video_df['channelTitle'].value_counts()


# ## Subscrivers

# In[96]:


# Convert count columns to numeric columns
numeric_cols = ['subscribers', 'views', 'totalVideos']
channel_data[numeric_cols] = channel_data[numeric_cols].apply(pd.to_numeric, errors='coerce')


# In[97]:


channel_data['channelName'] = channel_data['channelName'].apply( lambda x :get_display(arabic_reshaper.reshape(x)))


# In[98]:


sns.set(rc={'figure.figsize':(10,8)})
ax = sns.barplot(x='channelName', y='subscribers', data=channel_data.sort_values('subscribers', ascending=False))
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x/1000) + 'K'))
plot = ax.set_xticklabels(ax.get_xticklabels(),rotation = 90)


# In[99]:


ax = sns.barplot(x='channelName', y='views', data=channel_data.sort_values('views', ascending=False))
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x/10) + 'K'))
plot = ax.set_xticklabels(ax.get_xticklabels(),rotation = 90)


# In[100]:


ax = sns.barplot(x='channelName', y='totalVideos', data=channel_data.sort_values('totalVideos', ascending=False))
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x/10) + 'K'))
plot = ax.set_xticklabels(ax.get_xticklabels(),rotation = 90)


# ## Views distribution per channel
# 

# In[101]:


ax = sns.violinplot(video_df['channelTitle'], video_df['viewCount'], palette = 'pastel')
plt.title('Views per channel', fontsize = 14)
#ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos:'{:,.0f}'.format(x/10) + 'K'))
plt.show()


# ## Best performance

# In[102]:


video_df['title'] = video_df['title'].apply( lambda x :get_display(arabic_reshaper.reshape(x)))

ax = sns.barplot(x = 'viewCount' , y = 'title', data = video_df.sort_values('viewCount', ascending=False)[0:9], palette="Blues_d")
#plot = ax.set_yticklabels(ax.get_yticklabels(), rotation=90)
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos:'{:,.0f}'.format(x/1000) + 'K'))


# ## Worst performance

# In[103]:


ax = sns.barplot(x = 'viewCount' , y = 'title', data = video_df.sort_values('viewCount', ascending=True)[0:9], palette="Blues_d")
#plot = ax.set_yticklabels(ax.get_yticklabels(), rotation=90)
#ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos:'{:,.0f}'.format(x/200) + 'K'))


# ## View distribution per video
# 

# ## Views vs. likes and comments
# 

# In[104]:


fig, ax = plt.subplots(1,2)
sns.scatterplot(data = video_df, x = 'commentCount', y = 'viewCount', ax = ax[0])
sns.scatterplot(data = video_df, x = 'likeCount', y = 'viewCount', ax = ax[1])

ax[0].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos:'{:,.0f}'.format(x/8000) + 'K'))
ax[1].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos:'{:,.0f}'.format(x/8000) + 'K'))


# In[105]:


fig, ax =plt.subplots(1,2)
sns.scatterplot(data = video_df, x = "commentRatio", y = "viewCount", ax=ax[0])
sns.scatterplot(data = video_df, x = "likeRatio", y = "viewCount", ax=ax[1])


# In[106]:


sns.scatterplot(data = video_df, x = 'durationSecs' , y = 'viewCount' )


# In[107]:


sns.histplot(data=video_df[video_df['durationSecs'] < 10000], x="durationSecs", bins=30)


# In[108]:


fig, ax =plt.subplots(1,2)
sns.scatterplot(data = video_df, x = "durationSecs", y = "commentCount", ax=ax[0])
sns.scatterplot(data = video_df, x = "durationSecs", y = "likeCount", ax=ax[1])


# In[ ]:





# In[109]:



videos_per_month = pd.DataFrame(video_df['Month'].value_counts())
sort_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
videos_per_month = videos_per_month.reindex(sort_order)
ax = videos_per_month.reset_index().plot.bar(x='index', y='Month' , rot=0)




# In[111]:


day_df = pd.DataFrame(video_df['pushblishDayName'].value_counts())
weekdays = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_df = day_df.reindex(weekdays)
ax = day_df.reset_index().plot.bar(x='index', y='pushblishDayName', rot=0)


# In[ ]:





# In[113]:


stop_words = set(stopwords.words('english'))
video_df['title_no_stopwords'] = video_df['title'].apply(lambda x: [item for item in str(x).split() if item not in stop_words])

all_words = list([a for b in video_df['title_no_stopwords'].tolist() for a in b])
all_words_str = ' '.join(all_words) 

def plot_cloud(wordcloud):
    plt.figure(figsize=(30, 20))
    plt.imshow(wordcloud) 
    plt.axis("off");

wordcloud = WordCloud(width = 2000, height = 1000, random_state=1, background_color='white', 
                      colormap='tab20c', collocations=False, font_path='Tahoma').generate(all_words_str)
plot_cloud(wordcloud)


# In[114]:


wordcloud.to_file(video_df['channelTitle'][0]+".png")


# In[ ]:




