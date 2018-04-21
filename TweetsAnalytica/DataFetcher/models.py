from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50, unique=True)
    handle = models.CharField(max_length=50, unique=True)
    followers_count = models.IntegerField()
    all_tweets_count = models.IntegerField()
    following_count = models.IntegerField()
    likes_count = models.IntegerField()

    def __str__(self):
        return self.handle

class Tweet(models.Model):
    user = models.ForeignKey(User)
    text = models.TextField(max_length=260)
    favorites_count = models.IntegerField()
    retweets_count = models.IntegerField()
    replies_count = models.IntegerField()
    date_created = models.CharField(max_length=50)
