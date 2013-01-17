#!/usr/bin/python

import csv
import cPickle
from collections import namedtuple
import tweepy
import random
import urllib2
import json

import twitter_keys as tk

auth = tweepy.OAuthHandler(tk._CONSUMER_KEY, tk._CONSUMER_SECRET)
auth.set_access_token(tk._ACCESS_KEY, tk._ACCESS_SECRET)
_api = tweepy.API(auth)

StatusTuple = namedtuple('StatusTuple', 'text, id')


def get_api():
    return _api


def get_recent_status():
    target_url = 'https://api.twitter.com/1/statuses/user_timeline.json?include_entities=true&include_rts=true&screen_name={0}&count=1'.format(tk._SCREEN_NAME)
    result = json.load(urllib2.urlopen(target_url))
    return result[0]


def post_status(status):
    api = get_api()
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
        with open(r'robotski_log.txt', 'w') as csv_log:
            csv_log.write(status + " | " + id)
    except IOError:
        print 'Writing to the log didnt work!'


def get_log():
    result = []
    try:
        with open(r'robotski_log.txt', 'r') as csv_log:
            reader = csv.reader(csv_log, delimiter='|', quotechar='|')
            line = reader.next()
            result.append(StatusTuple(unicode(line[0]), int(line[1])))
    except IOError:
        pass
    return result

if __name__ == '__main__':
    status = get_recent_status()
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

