"""Mention_Streamer.py: Maintains a twitter stream listener."""

__author__      = "Jordan Summers"

import tweepy
import json
import sys


# Class for streaming all Tweets that mention the bot
class MentionStreamListener(tweepy.StreamListener):

    def __init__(self, api, article_handler, recipe_handler):
        super().__init__()
        self.ah = article_handler
        self.rh = recipe_handler
        self.api = api
        self.m_stream = None

    # When a new mention is seen, the tweet is parsed and replied to
    def on_data(self, raw_data):
        data = json.loads(raw_data)
        self.parse_tweet(data)

    # Exits the stream on an error and prints the status
    def on_error(self, status):
        print(status)
        return False

    # Parses a user's tweet and replies depending on if the request was for an article or recipe.
    # Returns False on an unsuccessful parse.
    def parse_tweet(self, tweet_data):
        text = tweet_data['text']
        text_data = text.split(" ", 2)

        if len(text_data) < 3:
            print("Not enough text in tweet:\n" + text)
            self.reply_error(tweet_data)
            return False

        # Identifies the tweet as an article and uses the Article Handler to respond
        if "article" in text_data[1].lower():
            print("Article Search: " + text_data[2])
            try:
                article = self.ah.search_article(text_data[2])
                self.reply_article(article, tweet_data)
            except:
                message = "Sorry, we couldn't find any articles that matched that search."
                self.reply_error(tweet_data, message)

        # Identifies the tweet as a recipe and uses the Recipe Handler to respond
        elif "recipe" in text_data[1].lower():
            print("Recipe Search:  " + text_data[2])
            try:
                recipe = self.rh.search_recipe(text_data[2])
                self.reply_recipe(recipe, tweet_data)
            except:
                message = "Sorry, we couldn't find any recipes that matched that search."
                self.reply_error(tweet_data, message)

        # Could not identify the content of the tweet
        else:
            print("Could not parse message text:\n" + text)
            self.reply_error(tweet_data)
            return False

        return True

    # Replies to a user's tweet if they have made a request for an article
    # Returns false if the tweet could not be replied to.
    def reply_article(self, article, tweet_data):
        try:
           self.api.update_status(status="@" + tweet_data['user']['screen_name'] + " " + article
                                  , in_reply_to_status_id=tweet_data['id'])

           return True
        except tweepy.TweepError:
            print("Could not reply to tweet.")
            return False

    # Replies to a user's tweet if they have made a request for a recipe
    # Returns false if the tweet could not be replied to.
    def reply_recipe(self, recipe, tweet_data):
        try:
            self.api.update_status(status='@' + tweet_data['user']['screen_name'] + " " + recipe,
                                   in_reply_to_status_id=tweet_data['id'])
            return True
        except tweepy.TweepError:
            print("Could not reply to tweet.")
            return False

    # Replies to a user's tweet with an error message if their tweet could not be parsed
    # Returns false if the tweet could not be replied to.
    def reply_error(self, tweet_data, message=None):
        try:
            if message == None:
                message = "Sorry, I couldn't quite catch that!" +\
                          "\nTry \"Article: [article keywords]\" or \"Recipe: [recipe keywords]\" for a better search experience"

            self.api.update_status(status="@" + tweet_data['user']['screen_name'] + " " + message, in_reply_to_status_id=tweet_data['id'])
            return True
        except tweepy.TweepError:
            print("Could not reply to tweet.")
            return False

    def start_streaming(self):
        self.m_stream = tweepy.Stream(auth=self.api.auth, listener=self)
        self.m_stream.filter(track=['@SuggestBot1'], is_async=True)

    def end_stream(self):
        self.m_stream.disconnect()
        sys.exit()
