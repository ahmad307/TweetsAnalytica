from paralleldots import set_api_key,get_api_key
from paralleldots import similarity, ner, taxonomy, sentiment, keywords, intent, emotion, abuse
from random import randint
import matplotlib.pyplot as plt
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
        set_api_key(open('D:/TwitterScraper/ParallelDotsKey.txt', 'r').read())
        get_api_key()

        #Dictionary to save analysis results
        self.emotions = {}


    def get_emotions(self):
        """Analyzes every tweet using ParallelDots API and adds result to Emotion Dic.

        :returns: Dictionary containing number of each emotion occurrences in all tweets.
        """

        for tweet in self.tweets:
            tweet = clean_tweet(tweet.full_text)

            if len(tweet) == 0: continue

            # Get tweet analysis result
            tweet_emotion = emotion(tweet)['emotion']['emotion']

            # Increment in emotions the tweet analysis result
            if tweet_emotion in self.emotions:
                self.emotions[tweet_emotion] += 1
            else:
                self.emotions[tweet_emotion] = 1

        return self.emotions


    def visualize_tweets(self,emotions):
        """Draws a pie chart of ParallelDots analysis result using MatPlotLib.

        :param emotions: Dictionary of tweets analysis results.
        """

        # Extract keys and values from given Dictionary
        labels = list(emotions.keys())
        values = list(emotions.values())
        colors = []

        # Choose random color for every key in labels
        for _ in range(0, len(labels)):
            colors.append('#{:06x}'.format(randint(0, 256 ** 3)))

        # Set figure properties
        plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.axis('equal')

        return plt