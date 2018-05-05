import tweepy
from DataFetcher.models import User,Tweet
from django.core.exceptions import ValidationError
from tweepy.binder import TweepError


class TweetsRetreiver:
    """Retreives user's twitter profile data using twitter api and Tweepy lib.

    :saves: User's profile data in User table in db,
    :saves: User's tweets in Tweet table in db.
    """
    def __init__(self,handle):
        """TweetsRetreiver Class Constructor.

        :param handle: String carrying user's twitter username.
        """
        self.consumer_key = "2Vikr8XyYV4jtwgVhzet1Z1SR"
        self.consumer_secret = open('D:/TwitterScraper/ConsumerSecret.txt','r').read()

        self.auth = tweepy.OAuthHandler(self.consumer_key,self.consumer_secret)
        self.api = tweepy.API(self.auth)
        self.handle = handle

        self.tweets = []
        # Pass TweepError, where empty tweets list isn't processed in save_user_data()
        try:
            #Get user timeline data as list of JSON responses
            self.tweets = self.api.user_timeline(screen_name=self.handle, tweet_mode='extended',count=20)
        except TweepError:
            pass


    def save_user_data(self):
        """Fetches user's profile data and saves them in User table in database.

        :returns: a refrence to the user database object if it's saved, or
        :returns: Dictionary containing error_message if the user couldn't be saved to database.
        """

        # Return error if user isn't fetched or desn't have any tweets
        if len(self.tweets) == 0:
            return {'error_message': 'User does not exist or has zero tweets.'}

        name = self.tweets[0].user.name
        tweets_count = self.tweets[0].user.statuses_count
        followers_count = self.tweets[0].user.followers_count
        following_count = self.tweets[0].user.friends_count
        likes_count = self.tweets[0].user.favourites_count

        # Create object of User database table
        user = User(
            name = name,
            handle = self.handle,
            all_tweets_count = tweets_count,
            following_count = following_count,
            followers_count = followers_count,
            likes_count = likes_count
        )

        # Validate and save user data to database
        try:
            user.full_clean()
            user.save()
            return user
        except ValidationError:
            return {'error_message': 'User already exists.'}


    def save_user_tweets(self,user):
        """Saves given user's last 21 tweets in Tweet table in database.

        :param user: refrence to an object of User database table.
        """
        for tweet in self.tweets:
            text = tweet.full_text
            likes_count = tweet.favorite_count
            retweets_count = tweet.retweet_count
            date_created = tweet.created_at

            #Create object of Tweet database table
            my_tweet = Tweet(
                user = user,
                text = text,
                favorites_count = likes_count,
                retweets_count = retweets_count,
                replies_count = 0,
                date_created = date_created
            )

            #Validate and save Fetched tweet data to database
            try:
                my_tweet.full_clean()
                my_tweet.save()
            except ValidationError:
                pass

        return self.tweets
