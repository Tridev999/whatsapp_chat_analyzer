import re
import pandas as pd
def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern,data)
    dframe = pd.DataFrame({'user_message':messages,'message_date':dates})
    dframe['message_date'] = pd.to_datetime(dframe['message_date'],format='%d/%m/%Y, %H:%M - ')
    dframe.rename(columns={'message_date' : 'date'},inplace=True)
    users = []
    messages = []
    for message in dframe['user_message']:
        entry = re.split('([\w\W]+?):\s',message)
        if entry[1:]: #username
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    dframe['user'] = users
    dframe['message'] = messages
    dframe.drop(columns=['user_message'],inplace=True)
    dframe['year'] = dframe['date'].dt.year
    dframe['month'] = dframe['date'].dt.month_name()
    dframe['day'] = dframe['date'].dt.day
    dframe['day_name'] = dframe['date'].dt.day_name()
    dframe['hour'] = dframe['date'].dt.hour
    dframe['min'] = dframe['date'].dt.minute
    period = []
    for i in dframe['hour']:
        if i=='00':
            period.append("00" + "-" + str(i+1))
        elif i=='23':
            period.append(str(i) + "-" + '00')
        else:
            period.append(str(i) + "-" + str(i+1))
    dframe['period'] = period
    return dframe