
import twitter_keys as tk
import tweepy

def get_api():
    auth = tweepy.OAuthHandler(tk._CONSUMER_KEY, tk._CONSUMER_SECRET)
    auth.set_access_token(tk._ACCESS_KEY, tk._ACCESS_SECRET)
    return tweepy.API(auth)


def get_recent_tweets():
    api = get_api()
    timeline = api.user_timeline(screen_name=tk._SCREEN_NAME)
    return timeline[0].text

def post_tweet():
    pass


def set_log():
    pass


def get_log():
    pass

if __name__ == '__main__':
    get_recent_tweets()
