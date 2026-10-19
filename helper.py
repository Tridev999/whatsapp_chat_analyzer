import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji
def fetch_stats(df, selected_user):
    if(selected_user != 'OverAll'):
        df = df[df["user"]==selected_user] 
    num_messages = df.shape[0]
    words = []
    for msg in df['message']:
        words.extend(msg.split())
    #media shared part
    total_media = df[df['message']=='<Media omitted>\n'].shape[0]
    #no of links shared
    extractor = URLExtract()
    links = []
    for msg in df['message']:
        links.extend(extractor.find_urls(msg))
    #return all statistics
    return num_messages , len(words) , total_media , len(links)
def most_busy_users(df):
    new_df = df['user'].value_counts().head(5)
    store = round(df['user'].value_counts()/df.shape[0],2).reset_index().rename(columns={"count":"Percentage","index":"Name"})
    return new_df, store
def word_cloud(df,selected_user):
    if(selected_user!='OverAll'):
        df = df[df['user']==selected_user]
    df = df[df['message']!='<Media omitted>\n']
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    text = df['message'].str.cat(sep=" ")
    frequencies = wc.process_text(text)
    if not frequencies:
        return None
    return wc.generate_from_frequencies(frequencies)
def most_common_words(df,selected_user):
    if(selected_user!='OverAll'):
        df = df[df['user']==selected_user]
    temp = df[df['user']!='group_notification']
    temp = temp[temp['message']!='<Media omitted>\n']
    file = open('stop_hinglish.txt','r')
    stop_words = file.read()
    words1 = []
    for message in temp['message']:
        for msg in message.lower().split():
            if msg not in stop_words:
                words1.append(msg)
    most_common_df = pd.DataFrame(Counter(words1).most_common(20))
    return most_common_df
def emoji_helper(df,selected_user):
    if(selected_user!='OverAll'):
        df = df[df['user']==selected_user]
    emojis = []
    for message in df['message']:
        for msg in message:
            if msg in emoji.EMOJI_DATA:
                emojis.append(msg)
    new_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))),columns=['Emoji','Frequency'])
    return new_df
def monthly_timeline(df,selected_user):
    if(selected_user!='OverAll'):
        df = df[df['user']==selected_user]
    timeline = df.groupby(['year','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" +  str(timeline['year'][i]))
    timeline['time'] = time
    return timeline
def dialy_timeline(df,selected_user):
    if(selected_user!='OverAll'):
        df = df[df['user']==selected_user]
    day_month = df.groupby(['day','month','year']).count()['message'].sort_values(ascending=False).reset_index()
    daytime = []
    for i in range(day_month.shape[0]):
        daytime.append(str(day_month.iloc[i]['day']) + "-" + day_month.iloc[i]['month'] + '-' + str(day_month.iloc[i]['year']))
    day_month['daytime'] = daytime
    return day_month
def most_busy_month(df,selected_user):
    if(selected_user!='OverAll'):
        df = df[df['user']==selected_user]
    new_month = df['date'].dt.month_name()
    df['month_name'] = new_month
    grouped_df = df.groupby('month_name').count()['message'].reset_index()
    return grouped_df
def most_busy_day(df,selected_user):
    if(selected_user!='OverAll'):
        df = df[df['user']==selected_user]
    new_day = df['date'].dt.day_name()
    df['day_name'] = new_day
    grouped_df = df.groupby('day_name').count()['message'].reset_index()
    return grouped_df
def activity_heatmap(df,selected_user):
    if(selected_user!='OverAll'):
        df = df[df['user']==selected_user]
    activity_map = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return activity_map
