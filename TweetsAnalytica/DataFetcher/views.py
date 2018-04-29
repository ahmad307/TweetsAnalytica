from django.shortcuts import render
from DataFetcher.TweetsRetreiverApi import TweetsRetreiver
from DataFetcher.TweetsAnalysis import TweetsAnalysis


def home(request):
    if request.method == 'POST':
        handle = request.POST.get('user_name')

        retreiver = TweetsRetreiver(str(handle))
        user = retreiver.save_user_data()

        # Analyze tweets if returned user is valid
        if user != False:
            # Get user tweets
            tweets = retreiver.save_user_tweets(user)

            # Create object from TweetsAnalysis to analyze tweets
            analyser = TweetsAnalysis(tweets)

            # Get dictionary containing analysis results
            emotions = analyser.get_emotions()

            # Get analysis visualization chart
            figure = analyser.visualize_tweets(emotions)

    return render(request, 'home.html')


def index(request):
    return render(request, 'landing_page/index.html')
