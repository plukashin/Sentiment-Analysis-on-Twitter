import tweepy
import re
import textblob
from nltk.tokenize import WordPunctTokenizer
import pandas as pd

#Download the csv file or choose your own
data = pd.read_csv('coingecko.csv', sep = ',')
ico = data['ICO'].head(50)

#Create an app on twitter and get your tokens and keys
acc_token = 'YOUR ACCCOUNT TOKEN'
acc_secret = 'YOUR ACCOUNT SECRET'
cons_key = 'YOUR CONSUMER KEY'
cons_secret = 'YOUR CONSUMER SECRET'

#Set authentication
auth = tweepy.OAuthHandler(cons_key, cons_secret)
auth.set_access_token(acc_token, acc_secret)

api = tweepy.API(auth)

cryptosentiment = []

#Go through every string in csv and search the tweets for an occurence of that
#word/sentence. Calculate polarity and subjectivity with sentiment analysis library
#and divide by the total number of tweets.
for crypto in ico:
    public_tweets = api.search(crypto)
    count = 0
    polarity = 0
    subjectivity = 0
    for tweet in public_tweets:
        count += 1
        print(tweet.text)
        analysis = textblob.TextBlob(tweet.text)
        polarity += analysis.sentiment[0]
        subjectivity += analysis.sentiment[1]
        print(analysis.sentiment)
    print(crypto)
    print(count)
    print(polarity)
    try:
        polarity = polarity / count
    except ZeroDivisionError:
        polarity = 0
    try:
        subjectivity = subjectivity / count
    except ZeroDivisionError:
        subjectivity = 0
    cryptosentiment.append([crypto,polarity,subjectivity])

#Put result in a data frame
res = pd.DataFrame(cryptosentiment, columns=['ICO', 'polarity', 'subjectivity'])
