import tweepy
from DataFetcher.models import User,Tweet
from django.core.exceptions import ValidationError

class TweetsRetreiver:
    """Retreives user's twitter profile data using twitter api and tweepy lib.

    :param handle: String carrying twitter username
    :saves: User's profile data in User table in db,
    :saves: User's tweets in Tweet table in db.
    """
    def __init__(self,handle):
        self.consumer_key = "2Vikr8XyYV4jtwgVhzet1Z1SR"
        self.consumer_secret = open('D:/TwitterScraper/ConsumerSecret.txt','r').read()

        self.auth = tweepy.OAuthHandler(self.consumer_key,self.consumer_secret)
        self.api = tweepy.API(self.auth)
        self.handle = handle

        #Get user timeline data as list of JSON responses
        self.tweets = self.api.user_timeline(self.handle, tweet_mode='extended')


    def save_user_data(self):
        """Fetches user's profile data and saves them in User table in database.

        :returns: a refrence to the user database object if it's saved, or
        :returns: False if the user couldn't be saved to database.
        """
        name = self.tweets[0].user.name
        tweets_count = self.tweets[0].user.statuses_count
        followers_count = self.tweets[0].user.followers_count
        following_count = self.tweets[0].user.friends_count
        likes_count = self.tweets[0].user.favourites_count

        user = User(
            name = name,
            handle = self.handle,
            all_tweets_count = tweets_count,
            following_count = following_count,
            followers_count = followers_count,
            likes_count = likes_count
        )

        try:
            user.full_clean()
            user.save()
            return user
        except ValidationError:
            return False


    def save_user_tweets(self,user):
        """Saves given user's last 21 tweets in Tweet table in database.

        :param user: refrence to an object of User database table.
        """
        for tweet in self.tweets:
            text = tweet.full_text
            likes_count = tweet.favorite_count
            retweets_count = tweet.retweet_count
            date_created = tweet.created_at

            #Create object of Tweet DB table
            my_tweet = Tweet(
                user = user,
                text = text,
                favorites_count = likes_count,
                retweets_count = retweets_count,
                replies_count = 0,
                date_created = date_created
            )

            #Validate Fetched tweet data
            try:
                my_tweet.full_clean()
                my_tweet.save()
            except ValidationError:
                pass
