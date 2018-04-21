from DataFetcher.models import User,Tweet
from bs4 import BeautifulSoup
import urllib3
import requests
import datetime
from django.core.exceptions import ValidationError



class TweetsScraper:
    """Scrapes user twitter profile and returns public tweets data.

    Takes a twitter username as 'handle'
    Saves user profile data to User DB table
    Saves tweets data to Tweets DB table
    """

    def __init__(self,handle):
        self.handle = handle

        self.url = 'https://twitter.com/'
        self.url += handle

        # Fetching user's profile html
        self.page = requests.get(self.url)

        # Creating Beautiful Soup object of the page
        self.soup = BeautifulSoup(self.page.content, 'html.parser')


    def get_user_data(self):
        """Gets user's profile data from Beautiful Soup object and saves it to DB.

        Returns a refrence to user if it's saved
        Returns False if the user can't be saved to database
        """

        # Collecting user data
        name = self.soup.find('strong', attrs={'class':'fullname show-popup-with-id u-textTruncate '}).text

        # Creating an object with all span tags that carry user profile data
        profile_data = self.soup.find_all('span', attrs={'class': 'ProfileNav-value'})

        # Iterating to extract data from span tags
        profile_list = []
        for obj in profile_data:
            try:
                profile_list.append(int(obj.text.replace(',', '')))
            except ValueError:
                pass

        # Creating object of User DB table
        user = User(
            name = name,
            handle = self.handle,
            all_tweets_count = profile_list[0],
            following_count = profile_list[1],
            followers_count = profile_list[2],
            likes_count = profile_list[3]
        )

        try:
            user.full_clean()
            user.save()
            return user
        except ValidationError:
            return False



    def get_user_tweets(self,user):
        """Gets user's last 20 tweets from Beautiful Soup object and saves them to DB.

        Takes user object as parameter
        Saves tweets belonging to self.handle in the database as Tweet objects
        """

        # Creating an object with all 'li' tags carrying tweets data
        tweets = self.soup.find_all('li', attrs={'class': 'js-stream-item'})

        # Iterating over tweets object
        all_tweets = []
        for tweet in tweets:
            stats = tweet.find_all('span', attrs={'class': 'ProfileTweet-actionCountForAria'})

            tweet_data = []
            for stat in stats:
                stat = str(stat.text).split(' ')
                tweet_data.append(stat[0])

            date = tweet.find('span', attrs={'class': '_timestamp js-short-timestamp '}).text
            # Formatting date
            temp_count = date.count(' ')
            if temp_count == 1:
                date = date.split(' ')
                date = date[1] + ' ' + date[0] + ' ' + str(datetime.datetime.now().year)

            # Creating object of Tweet DB table
            my_tweet = Tweet(
                user = user,
                text = str(tweet.p.text).replace(',', ' '),
                replies_count = int(tweet_data[0].replace(',', '')),
                retweets_count = int(tweet_data[1].replace(',', '')),
                favorites_count = int(tweet_data[2].replace(',', '')),
                date_created = date
            )

            try:
                my_tweet.full_clean()
                my_tweet.save()
            except ValidationError:
                pass

