#!/usr/bin/python

import codecs
import cPickle
from collections import namedtuple
import tweepy
import random
import urllib2
import json

import twitter_keys as tk

StatusTuple = namedtuple('StatusTuple', 'text, id')


def get_api(consumer_key, consumer_secret, access_key, access_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return tweepy.API(auth)


def get_recent_status():
    api = get_api(tk._CONSUMER_KEY_CONSUMER, tk._CONSUMER_SECRET_CONSUMER, tk._ACCESS_KEY_CONSUMER, tk._ACCESS_SECRET_CONSUMER)
    timeline = api.user_timeline(screen_name=tk._SCREEN_NAME, include_rts=True)
    return timeline[0]


def friend_followers():
    api = get_api(tk._CONSUMER_KEY_BOT, tk._CONSUMER_SECRET_BOT, tk._ACCESS_KEY_BOT, tk._ACCESS_SECRET_BOT)
    followers = api.followers_ids(screen_name=tk._BOT_NAME)
    friends = set(api.friends_ids(screen_name=tk._BOT_NAME))
    for person in followers:
        if person not in friends:
            api.create_friendship(user_id=person, follow=True)


def post_status(status):
    api = get_api(tk._CONSUMER_KEY_BOT, tk._CONSUMER_SECRET_BOT, tk._ACCESS_KEY_BOT, tk._ACCESS_SECRET_BOT)
    api.update_status(status=status)
    print 'Current Status: ' + status


def translate_status(phrase, status):
    result = phrase + " " + status
    if (len(result) > 140):
        return result[:137] + "..."
    else:
        return result


def get_phrase():
    try:
        with open(r'robotski.pkl', 'r') as robotski_pickle:
            robotski_list = cPickle.load(robotski_pickle)
            return random.choice(robotski_list)
    except 'SomeError':
        print '''I dont think that this file exists.
                try running robotski_generator.py'''


def get_status_text(status):
    return unicode(status.get('text', 'No message'))


def get_status_id(status):
    return unicode(status.get('id', '0'))


def check_unique_tweet(status):
    log = get_log()
    return len(log) == 0 or log[0].id != status.get('id', '0')


def set_log(status, id):
    #todo append to top of file
    try:
        with codecs.open(r'robotski_log.txt', 'w', 'utf-8') as csv_log:
            csv_log.write(status + " | " + id)
    except IOError:
        print 'Writing to the log didnt work!'


def get_log():
    result = []
    try:
        with codecs.open(r'robotski_log.txt', 'r', 'utf-8') as csv_log:
                row = csv_log.read().split('|')
                result.append(StatusTuple(unicode(row[0]), int(row[1])))
    except IOError:
        print "Couldn't read from the log"
    return result

if __name__ == '__main__':
    status = get_recent_status()
    friend_followers()
    should_create_tweet = check_unique_tweet(status)
    if (should_create_tweet):
        status_text = get_status_text(status)
        status_id = get_status_id(status)
        phrase = get_phrase()
        robotskified = translate_status(phrase, status_text)
        set_log(robotskified, status_id)
        post_status(robotskified)
    else:
        print 'There wasnt a new tweet!'

