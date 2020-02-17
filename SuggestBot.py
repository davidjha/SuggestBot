"""SuggestBot.py: User interface to retrieve and post news and recipes to twitter."""

__author__      = "David Ha"

import tweepy
import time
import threading
import Article_Handler
import Mention_Streamer
import Recipe_Handler
import sys
from key import *


class SuggestBot:

    # variables
    last_post_time = 0
    boot_up_time = 0
    current_time = 0
    is_executing = False
    page_counter = "10"
    time_interval = 60

    # init method
    def __init__(self):
        self.ah = Article_Handler.Article_Handler()
        self.rh = Recipe_Handler.Recipe_Handler()
        self.auth = self.get_auth()
        self.api = self.get_api()
        self.ms = Mention_Streamer.MentionStreamListener(self.api, self.ah, self.rh)
        self.article_cache = self.load_data("posted_articles.txt")
        self.recipe_cache = self.load_data("posted_recipes.txt")

    # Cache data from file
    def load_data(self, cache_type):
        temp = []
        with open(cache_type, "a+") as file:
            for line in file:
                temp.append(line)
        file.close()
        return temp

    # Clean file of duplicates at startup
    def clean_file(self, cache_type):

        with open(cache_type, "r+") as file:
            lines = file.readlines()
            set_of_lines = set(lines)
        file.close()

        with open(cache_type, 'w') as output:
            for line in set_of_lines:
                output.write(line)
        file.close()

    # Retrieves the authorization for the SuggestBot account
    def get_auth(self):
        authenticate = tweepy.OAuthHandler(CONSUMER_KEY2, CONSUMER_SECRET2)
        authenticate.set_access_token(ACCESS_TOKEN2, ACCESS_SECRET2)
        return authenticate

    # Retrieves the tweepy API object
    def get_api(self):
        twitter_api = tweepy.API(self.auth)
        return twitter_api

    # Posts a news article
    def post_article(self):
        article = self.pull_article()

        if article is None:
            self.handle_duplicate_article()

        try:
            self.api.update_status(article)
            print('\n\n' + "------------------------------Article Post-------------------------------")
            print(self.article_cache[len(self.article_cache) - 1], '\n')
            print(" Article Posted @" + time.asctime(), '\n')
            print('-------------------------------------------------------------------------', '\n\n')
            self.log_posts("-Article Posted @ " + time.asctime() + " " + self.article_cache[len(self.article_cache) - 1] + '\n')
        except tweepy.TweepError as ex:
            if ex.api_code == 187:
                self.handle_duplicate_article()
            else:
                print(ex.reason + "Article Handler")

    # Duplicate status update handler
    def handle_duplicate_article(self):
        temp = int(self.page_counter) - 1
        self.page_counter = str(temp)
        print("page counter = " + self.page_counter)
        if temp == 5:
            self.page_counter = "10"
            self.article_cache.clear()
        self.post_article()

    # Make a request to the Article_Handler to pull an article
    def pull_article(self):
        for i in range(0, 9):
            article = self.ah.get_selected(i, self.page_counter)
            title = self.get_title(article)
            if title not in self.article_cache:
                self.article_cache.append(title)
                print('\n\n', "+Article Pulled @", time.asctime(), '\n')
                return article
        return None

    # Gets title from article
    def get_title(self, article):
        temp = article.split('(')
        title = temp[0]
        title = title[:-1]
        return title

    # Posts a recipe that Recipe_Handler selects
    def post_recipe(self):
        recipe = self.pull_recipe()
        try:
            self.api.update_status(recipe)
            print('\n\n' + "------------------------------Recipe Post-------------------------------")
            print(recipe, '\n')
            print(" Recipe Posted @ " + time.asctime(), '\n')
            print('-------------------------------------------------------------------------', '\n\n')
            self.log_posts("-Recipe Posted @" + time.asctime())
        except tweepy.TweepError as ex:
            if ex.api_code == 187:
                self.post_recipe()
            else:
                print(ex.reason + "Recipe Handler")

    # Makes a request to the Recipe_Handler to pull a recipe.
    def pull_recipe(self):
        recipe = self.rh.search_recipe()
        res_title = self.get_recipe_title(recipe)
        if res_title not in self.recipe_cache:
            self.recipe_cache.append(res_title)
        print('\n\n', "+Recipe Pulled @ ", time.asctime(), '\n')
        return recipe

    # Return recipe name to be cached and stored
    def get_recipe_title(self, recipe):
        temp = recipe.split(':')
        title = temp[1]
        title = title[1:]
        title = title.split("\n")
        return title[0]

    # Execute interval posting
    def interval_post(self):
        self.last_post_time = self.boot_up_time

        while self.is_executing:
            # Post to twitter if it has been more than 4 hours ( 14400 seconds)
            if self.current_time >= (self.last_post_time + self.time_interval):
                self.post_article()
                time.sleep(3)
                self.post_recipe()
                self.last_post_time = self.current_time
            else:
                self.current_time = self.get_time()

    # Listens for all tweets that mention SuggestBot
    def stream_mentions(self):
        self.ms.start_streaming()

    # Return localtime in seconds
    def get_time(self):
        temp = time.localtime()
        hour = temp.tm_hour * 59 * 59
        minute = temp.tm_min * 59
        second = temp.tm_sec

        return hour + minute + second

    # Executes SuggestBot functions continously
    def execute(self):
        if self.is_executing:
            print("SuggestBot is already executing!")
        else:
            self.is_executing = True
            print("Starting SuggestBot! Please Wait...")
            self.boot_up_time = self.get_time()
            self.log_posts("SuggestBot booted up @" + time.asctime())
            time.sleep(3)
            sb.t_interval_post.start()
            sb.t_mention_s.start()

    # Log all posts
    def log_posts(self, entry):
        f = open("post_log.txt", "a+")
        f.write(entry + '\n')
        f.close()

    # Main menu
    def main_menu(self):

        user_input = '0'
        while user_input != '9':
            self.menu_options()
            user_input = input("Enter Option: ")

            if user_input == '1':
                self.execute()

            elif user_input == '2':
                self.pull_article()

            elif user_input == '3':
                self.post_article()

            elif user_input == '4':
                self.pull_recipe()

            elif user_input == '5':
                self.post_recipe()

            elif user_input == '6':
                self.clean_file("posted_recipes.txt")
                self.clean_file("posted_articles.txt")

            elif user_input == '9':
                print("Exiting, Please wait...")
                self.log_posts("SuggestBot shutdown @" + time.asctime() + '\n')
                self.is_executing = False
                self.ms.end_stream()
                break

            else:
                print("\n\n\n")

    def menu_options(self):
        print('\n')
        print("----------------------Console-----------------------------")
        print("1) Execute: (Interval Posting and Stream Mention, pulling and posting)")
        print("2) Pull Article: ")
        print("3) Post Article: ")
        print("4) Pull Recipe: ")
        print("5) Post Recipe: ")
        print("6) Clean Files: ")
        print("9) Exit")
        print("*) Any Key to refresh the menu")
        print("----------------------------------------------------------")
        print('\n')


if __name__ == "__main__":
    sb = SuggestBot()

    # Threads
    sb.t_interval_post = threading.Thread(target=sb.interval_post, name='thread_time_post', daemon=True)
    sb.t_mention_s = threading.Thread(target=sb.stream_mentions, name='thread_mention_s', daemon=True)
    sb.t_main_menu = threading.Thread(target=sb.main_menu, name='thread_menu')

    if len(sys.argv) == 1:
        # Start main menu
        sb.t_main_menu.start()
        # Join all threads
        sb.t_main_menu.join()
        sb.t_mention_s.join()
        sb.t_interval_post.join()
    elif sys.argv[1] is "1":
        sb.execute()
        # Join all threads
        sb.t_mention_s.join()
        sb.t_interval_post.join()
    else:
        print("Invalid Arguments, Enter 1 as arg for menu-less execution")
