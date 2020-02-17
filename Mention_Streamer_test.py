"""Mention_Streamer.py: Mention_streamer tests."""

__author__      = "Jordan Summers"

import os, sys, inspect, tweepy, key
import Article_Handler, Recipe_Handler
import Mention_Streamer
import unittest, requests
from unittest.mock import patch

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

def get_auth():
    authenticate = tweepy.OAuthHandler(key.CONSUMER_KEY, key.CONSUMER_SECRET)
    authenticate.set_access_token(key.ACCESS_TOKEN, key.ACCESS_SECRET)
    return authenticate

# Retrieves the tweepy API object
def get_api():
    twitter_api = tweepy.API(get_auth())
    return twitter_api

ms = Mention_Streamer.MentionStreamListener(get_api(), Article_Handler.Article_Handler(), Recipe_Handler.Recipe_Handler())

class TestMentionStreamer(unittest.TestCase):

    #def test_recipe_parse(self):
    #    tweet_data = {
    #        "text": "@SuggestBot Recipe: steak"
    #    }
    #    with patch.object(ms, 'reply_recipe') as mock:
    #        try:
    #            ms.parse_tweet(tweet_data)
    #        except:
    #            print("Can't reply to tweets")

    #    self.assertTrue(mock.called)

    def test_article_parse(self):
        tweet_data = {
            "text": "@SuggestBot Article: world affairs"
        }
        with patch.object(ms, 'reply_article') as mock:
            try:
                ms.parse_tweet(tweet_data)
            except:
                print("Can't reply to tweets")

        self.assertTrue(mock.called)

    def test_error_parse(self):
        tweet_data = {
            "text": "@SuggestBot Arficle: world affairs"
        }
        with patch.object(ms, 'reply_error') as mock:
            try:
                ms.parse_tweet(tweet_data)
            except:
                print("Can't reply to tweets")

        self.assertTrue(mock.called)

if __name__ == '__main__':
    unittest.main()
