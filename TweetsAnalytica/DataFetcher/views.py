from django.shortcuts import render, HttpResponse
from DataFetcher.TweetsRetreiverApi import TweetsRetreiver
from DataFetcher.TweetsAnalysis import TweetsAnalysis
from DataFetcher.models import User,Tweet


def index(request):
    response = {}
    response['figure_alt_msg'] = 'Enter username to get analyzed figure of your tweets'

    # Get number of saved users and number of saved tweets from database
    #       to display in template
    users_count = User.objects.count()
    tweets_count = Tweet.objects.count()
    response['users_count'] = users_count
    response['tweets_count'] = tweets_count

    if request.method == 'POST':
        handle = request.POST.get('user_name')

        retreiver = TweetsRetreiver(str(handle))
        user = retreiver.save_user_data()

        # Analyze tweets if returned user is valid
        if type(user) == User:
            # Get user tweets
            tweets = retreiver.save_user_tweets(user)

            # Create object from TweetsAnalysis to analyze tweets
            analyser = TweetsAnalysis(tweets)

            # Get dictionary containing analysis results
            emotions = analyser.get_emotions()
            
            # Get analysis visualization chart
            figure = analyser.visualize_tweets(emotions)

            # Save figure in static folder as png
            figure.savefig('static/analysis_figures/figure2.png')
            figure.close()

            # Inject html with dummy figure path
            response['analysis_figure'] = 'analysis_figures/figure2.png'

        elif user['error_message'] == 'User already exists.':
            response['figure_alt_msg'] = 'User with this username already exists!'

        elif user['error_message'] == 'User does not exist.':
            response['figure_alt_msg'] = 'Username does not exist, try another!'

        elif user['error_message'] == 'User does not exist or has zero tweets.':
            response['figure_alt_msg'] = 'User does not exist or has zero tweets.'

    return render(request, 'landing_page/index.html', response)
