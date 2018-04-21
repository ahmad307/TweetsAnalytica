from django.shortcuts import render
from DataFetcher.TweetsScraper import TweetsScraper

def index(request):
    if request.method == 'POST':
        handle = request.POST.get('user_name')
        obj = TweetsScraper(str(handle))
        user = obj.get_user_data()
        if user != False:
            obj.get_user_tweets(user)

    return render(request,'home.html')