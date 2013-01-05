
import twitter_keys as tk
import tweepy

auth = tweepy.OAuthHandler(tk._CONSUMER_KEY, tk._CONSUMER_SECRET)
auth.set_access_token(tk._ACCESS_KEY, tk._ACCESS_SECRET)
_api = tweepy.API(auth)


def get_api():
    return _api


def get_recent_tweet():
    api = get_api()
    timeline = api.user_timeline(screen_name=tk._SCREEN_NAME)
    return timeline[0].text


def post_tweet(status):
    api = get_api()
    api.update_status(status=status)
    print 'Current Status: ' + status


def translate_tweet(status):
    result = "Wow how great!" + " " + status
    if (len(result) > 140):
        return result[:137] + "..."
    else:
        return result


def set_log():
    pass


def get_log():
    pass

if __name__ == '__main__':
    tweet = get_recent_tweet()
    robotskified = translate_tweet(tweet)
    post_tweet(robotskified)

