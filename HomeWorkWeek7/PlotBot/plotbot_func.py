
# coding: utf-8

# In[1]:


import tweepy, re, csv, time
import matplotlib.pyplot as plt
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# In[2]:


class Twitter_Validator(object):

    def __init__(self, api):

        self.api = api

    def check_request(self):
        for tweet in tweepy.Cursor(self.api.search, q='@PlotBot5').items():
            tweet_id = tweet.id
            tweet_user_sn = tweet.user.screen_name
            tweet_user_name = tweet.user.name
            tweet_text = tweet.text

            match = re.match('@plotbot5 analyze: @[a-z0-9_]*', tweet_text.lower())

            if match:
                return True
            else:
                try:
                    self.api.update_status(status="@{} Sorry {}, the query was not in the proper format, please send your query in the following format: [at]PlotBot5 Analyze: [at][screen_name to be analyzed]".format(tweet_user_sn, tweet_user_name), in_reply_to_status_id=tweet_id)
                    return False
                except tweepy.TweepError:
                    pass


# In[3]:


class Twitter_Checker(object):

    def __init__(self, api):

        self.api = api

    def append_csv(self, add_row):
        with open('data/tweet_logs.csv', mode='a') as file:
            writer = csv.writer(file)

            for item in add_row:
                    writer = csv.writer(file)
                    writer.writerow(item)

    def check_tweet(self, tweet_id, tweet_user_sn, tweet_user_name, tweet_analyze_sn, add_row):
        with open('data/tweet_logs.csv', mode='r') as file:
            reader = csv.reader(file)

            not_exist = True

            for row in reader:
                if str(tweet_id) in row:
                    not_exist = False
                    return not_exist

            if not_exist:
                self.append_csv(add_row)
                return tweet_analyze_sn

    def search_request(self):
        for tweet in tweepy.Cursor(self.api.search, q='@PlotBot5').items():
            tweet_id = tweet.id
            tweet_user_sn = tweet.user.screen_name
            tweet_user_name = tweet.user.name
            tweet_text = tweet.text
            tweet_analyze_sn = "@{}".format(tweet.entities['user_mentions'][1]['screen_name'])

            add_row = [[tweet_id, "@" + tweet_user_sn, tweet_text, tweet_analyze_sn]]

            result = self.check_tweet(tweet_id, tweet_user_sn, tweet_user_name, tweet_analyze_sn, add_row)
            return result, tweet_user_sn, tweet_id


# In[4]:


class Twitter_Plotter(object):

    def __init__(self, api, screen_name, user_name, tweet_id):

        self.api = api
        self.screen_name = screen_name
        self.user_name = user_name
        self.tweet_id = tweet_id

    def analyze_it(self):

        store = []
        for tweet in tweepy.Cursor(self.api.user_timeline, id=self.screen_name).items(500):
            try:
                analyzer = SentimentIntensityAnalyzer()
                store.append(analyzer.polarity_scores(tweet.text)['compound'])
            except tweepy.RateLimitError:
                time.sleep(60 * 15)

        return store

    def plot_it(self):

        store = self.analyze_it()

        fig, ax = plt.subplots(figsize=(10.24, 5.12), dpi=100)
        ax.plot(np.arange(len(store)), store, marker='o', lw=.5, color='c', zorder=3, label=self.screen_name[1:])
        ax.set_title('Sentiment Analysis of Tweets ({} GMT)'.format(time.strftime("%m/%d/%y %H%M", time.gmtime())))
        ax.set_xlabel('Tweets Ago')
        ax.set_ylabel('Tweet Polarity (Avg={:.4f})'.format(np.mean(store)))

        ax.set_xlim(-1.5, len(store) * 1.005)
        ax.set_ylim(-1, 1)

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        ax.legend(loc=3, bbox_to_anchor=(1, .86), title='Tweets')
        ax.grid(ls='dashed', zorder=0)

        img_file = "data/plots/{}_{}.png".format(self.screen_name[1:], time.strftime("%Y%m%d%H%M", time.gmtime()))

        plt.savefig(img_file, dpi=100, bbox_inches='tight')

        return img_file

    def send_it(self):

        img_file = self.plot_it()
        self.api.update_with_media(img_file, status="New Tweet Analysis: {} (Thanks @{})".format(self.screen_name[1:], self.user_name), in_reply_to_status_id=self.tweet_id)

