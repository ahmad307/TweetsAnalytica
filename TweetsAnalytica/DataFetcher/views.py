from django.shortcuts import render
from DataFetcher.TweetsRetreiverApi import TweetsRetreiver

def index(request):
    if request.method == 'POST':
        handle = request.POST.get('user_name')

        obj = TweetsRetreiver(str(handle))
        user = obj.save_user_data()

        if user != False:
            obj.save_user_tweets(user)

    return render(request,'home.html')