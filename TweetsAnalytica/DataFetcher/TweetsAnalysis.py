from paralleldots import set_api_key,get_api_key
from paralleldots import similarity, ner, taxonomy, sentiment, keywords, intent, emotion, abuse
import tweepy
import re


def clean_tweet(tweet):
    """Cleans tweet text from unwanted additions (i.e. urls), using a regular expression."""

    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


class TweetsAnalysis:
    """Analyzes given tweets using Parallel Dots API."""

    def __init__(self,tweets):
        """TweetsAnalysis Class Constructor.

        :param tweets: List of JSON objects containing certain user's tweets.
        """

        self.tweets = tweets

        # Setting ParalleDots API keys
        set_api_key(open('D:/TweetsSraper/ParallelDotsKey.txt','r').read())
        get_api_key()

        #Dictionary to save analysis results
        self.emotions = {}


    def get_emotions(self):
        """Analyzes every tweet using ParallelDots API and adds result to Emotion Dic.

        :returns: Dictionary containing number of each emotion occurrences in all tweets.
        """

        for tweet in self.tweets:
            tweet = clean_tweet(tweet.full_text)

            # Increment in emotions the tweet analysis' result
            if emotion(tweet)['emotion']['emotion'] in self.emotions:
                self.emotions[emotion(tweet)['emotion']['emotion']] += 1
            else:
                self.emotions[emotion(tweet)['emotion']['emotion']] = 1

        return self.emotions
