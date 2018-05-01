from django.shortcuts import render
from DataFetcher.TweetsRetreiverApi import TweetsRetreiver
from DataFetcher.TweetsAnalysis import TweetsAnalysis
from DataFetcher.models import User,Tweet


def home(request):
    response = {}
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

            # Save figure in static folder as png
            figure.savefig('static/analysis_figures/figure.png')

            # Inject html with figure path
            response['analysis_figure'] = 'analysis_figures/figure.png'

    return render(request, 'home.html', response)


def index(request):
    response = {}

    # Get number of saved users and number of saved tweets from database
    users_count = User.objects.count()
    tweets_count = Tweet.objects.count()

    response['users_count'] = users_count
    response['tweets_count'] = tweets_count

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

            # Save figure in static folder as png
            figure.savefig('static/analysis_figures/figure.png')

            # Inject html with figure path
            response['analysis_figure'] = 'analysis_figures/figure.png'

    return render(request, 'landing_page/index.html', response)
