"""Article_Handler.py: Retrieves Articles."""

__author__      = "Roland Bell"
# Imports
import requests
import datetime
import json
import re

#an object to hold a date range for search queries
#defaults are begin = 2 days ago, end = today
#Date format is y-m-d in with the full year so 2019-04-20
sources = (
           "abc-news,\
            associated-press,\
            axios,\
            breitbart-news,\
            cbs-news,\
            cnn,\
            fox-news,\
            msnbc,\
            national-review,\
            nbc-news,\
            newsweek,\
            politico,\
            reuters,\
            the-hill,\
            the-new-york-times,\
            the-washington-post,\
            the-washington-times,\
            time,\
            usa-today,\
            vice-news"
            )
class Date_Range():
    def __init__(self,begin = None, end = None):
        if begin is None:
            self.begin = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
        else:
            self.begin = begin
        if end is None:
            self.end =  datetime.datetime.now().strftime("%Y-%m-%d")
        else:
            self.end = begin



#Estimate of read times
class Estimate():
    def __init__(self,words,mins,secs):
        self.words = words
        self.mins = mins
        self.secs = secs

class Article_Handler():

    # Variables
    def __init__(self):
        self.NEWS_KEY = ""
        self.BASE_QUERY =  ("https://newsapi.org/v2/everything?"
                            "language=en&"
                            "pageSize=10&"
                            "apiKey="+ self.NEWS_KEY)
        self.search_response=""

    # Searches for articles from the NewsAPI that will be considered for posting.
    def search_article(self, keyword_string=None, date_range=Date_Range(), catagories=None):

        search_query = self.BASE_QUERY + "&sortBy=relevancy"
        if keyword_string != None:
            keywords = keyword_string.split(",")
            search_query += str('&q=' + ' OR '.join(keywords))
        if date_range != None:
            search_query += ('&from='+date_range.begin+'&to=' + date_range.end)
        if catagories != None:
            search_query += '&catagories='+catagories
        
        response = requests.get(search_query)
        parsed_resp = json.loads(response.text)

        if parsed_resp["status"] == "error":
            #print("error: "+parsed_resp["code"]+": "+parsed_resp["message"])
            raise ValueError(parsed_resp["message"])
        elif parsed_resp["articles"] is None:
            #print("error: no articles found.")
            raise ValueError("error: no articles found.")
        else: 
            self.store_article(article=parsed_resp["articles"][0] )
            return self.summerize(article=parsed_resp["articles"][0])


    # Stores an article that has been selected into the selected_articles file.
    def store_article(self, article):
        f = open("posted_articles.txt","a+")
        f.write(article["title"] + "\n")
        f.close()
        return

    # Rates the articles from the pulled_articles list and chooses which ones to post.
    def rate_article(self):
        return

    # Produces a brief summary of an article.
    def summerize(self,article):
        readtime = self.estimate(article["content"])
        return "" + article["title"] \
                  + " (" + str(readtime.words) + " words, " \
                  + "{:d}:{:02d}".format(readtime.mins, readtime.secs) + ")\n" \
                  + article["url"]
                  #+ "Description: " + article["description"] + "\n"\
                  #+ "Source: " + article["source"]["name"] + " " \

    # Estimates the time it will take to read an article.
    def estimate(self,content):
        if content == None:
            return Estimate(words=0, mins=0, secs=0)
        try:
            xChars = re.search(r"\[\+[0-9]+ chars\]", content).group()
            xChars = int(xChars[2:len(xChars)-6])
        except:
            xChars = 0
        wordc = int(len(content.split()) + xChars /4.79)#rough
        minutes = int(wordc/275.0) #avg WPM
        seconds = int(wordc/275.0 % 1 * 60)
        if seconds > 45:
            minutes += 1
            seconds = 0
        elif seconds > 30:
            seconds = 45
        elif seconds > 15:
            seconds = 30
        else:
            seconds = 15

        return Estimate(words=wordc, mins=minutes, secs=seconds)

    # Retrieves articles in the selected_articles file.
    def get_selected(self, article_number, page_number_str):
        select_query = self.BASE_QUERY + "&sortBy=popularity"
        date_range = Date_Range(begin=(datetime.datetime.now() - datetime.timedelta(hours=2)).strftime("%Y-%m-%d"),
                                end= datetime.datetime.now().strftime("%Y-%m-%d") )
        select_query += ('&from='+date_range.begin+'&to=' + date_range.end)
        select_query += ('&sources='+ sources + '&page=' + page_number_str)
        response = requests.get(select_query)
        parsed_resp = json.loads(response.text)

        if parsed_resp["status"] == "error":
            print("error: "+parsed_resp["code"]+": "+parsed_resp["message"])
            raise ValueError(parsed_resp["message"])
        elif parsed_resp["articles"][article_number] is None:
            print("error: no articles found.")
            raise ValueError("error: no articles found.")
        else:
            self.store_article(article=parsed_resp["articles"][article_number])
            return self.summerize(article=parsed_resp["articles"][article_number])
