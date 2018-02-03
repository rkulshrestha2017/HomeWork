
# coding: utf-8

# In[1]:


import tweepy, os, time, csv, json
from plotbot_func import Twitter_Checker, Twitter_Validator, Twitter_Plotter


# In[2]:


#api_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath('')))))
#file_name = os.path.join(api_dir, "api_keys.json")
file_name = os.path.join("keys/api_keys.json")
data = json.load(open(file_name))

consumer_key = data['twitter_consumer_key']
consumer_secret = data['twitter_consumer_secret']
access_token = data['twitter_access_token']
access_token_secret = data['twitter_access_token_secret']


# In[3]:


# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# In[ ]:


while True:
    time.sleep(60 * 2)
    trash_it = Twitter_Validator(api)
    change_it = Twitter_Checker(api)

    mail_upgrade_it = trash_it.check_request()

    if mail_upgrade_it:
        screen_name, user_name, tweet_id = change_it.search_request()
        if screen_name:
            success = Twitter_Plotter(api, screen_name, user_name, tweet_id)
            success.send_it()

