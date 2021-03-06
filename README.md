# TweetsAnalytica
A web application that analyzes user's public Twitter profile.

**Check it out at:**
*https://tweets-analytica.herokuapp.com/*

**Built with:**
* Django.
* Twitter API through Tweepy library.
* Beautiful Soup.
* Matplotlib.

*The project is built for learning purposes.*

## How It Works
* TweetsAnalytica offers the user a personalized plot categorizing his most recent tweets based on emotion.
* User's profile data were initially scraped using Beautiful Soup library, but Twitter API was then used as a more authorized and stable way to fetch data.
* Data saved in the database is processed using ParallelDots API and plotted using Matplotlib library.
