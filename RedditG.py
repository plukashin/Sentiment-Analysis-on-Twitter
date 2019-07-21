from IPython import display
import math
from pprint import pprint
import pandas as pd
import numpy as np
import nltk
import csv
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='darkgrid', context='talk', palette='Dark2')
import praw
import os.path
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

#All this information can be obtained on reddit.com
reddit = praw.Reddit(client_id='YOUR CLIENT ID',
                     client_secret='YOUR SECRET KEY',
                     user_agent='YOUR USER AGENT')

headline = set()


for submission in reddit.subreddit('CryptoCurrency').new(limit=None):
    headline.add(submission.title)
    display.clear_output()
    print(len(headline))

sia = SIA()
results = []

file_path = "Path to csv file that you are going to create and write headlines and analysis to"

#Here we check if the file exist. If that is the case we check for duplicate headlines and skip those.
#Otherwise we append result to a list. Analysis calculates polarization score
if os.path.exists(file_path) == True:
    with open('reddit_headlines_labels.csv', 'rt', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter = ',')
        for line in headline:
            for row in reader:
              if line == row[0]:
                  print("is in file")
                  pass
              else:
                  pol_score = sia.polarity_scores(line)
                  pol_score['headline'] = line
                  results.append(pol_score)
else:
    for line in headline:
        pol_score = sia.polarity_scores(line)
        pol_score['headline'] = line
        results.append(pol_score)


#Put analysis in data frame and set new colummn "label" that is based on compound rate.
#This value varies depending on your preferences
df = pd.DataFrame.from_records(results)
df['label'] = 0
df.loc[df['compound'] > 0.2, 'label'] = 1
df.loc[df['compound'] < -0.2, 'label'] = -1
df.head()

#Append new rows to existing file or create a new one
if os.path.exists(file_path) == True:
    with open('reddit_headlines_labels.csv','a') as fd:
        for line in df:
            if line.startswith('compound') or line.startswith('headline') or line.startswith('neg') or line.startswith('neu') or line.startswith('pos') or line.startswith('label'):
                pass
            else:
                fd.write(line)
else:
    df2 = df[['headline', 'label']]
    df2.to_csv('reddit_headlines_labels.csv', mode='a', encoding='utf-8', index=False)

#Now we read the file and plot the results and percentage of all the headlines
data = pd.read_csv("reddit_headlines_labels.csv",sep=',')

print(data)
print(data.label.value_counts)
fig, ax = plt.subplots(figsize=(8, 8))

counts = data.label.value_counts(normalize=True) * 100

sns.barplot(x=counts.index, y=counts, ax=ax)

ax.set_xticklabels(['Negative', 'Neutral', 'Positive'])
ax.set_ylabel("Percentage")

plt.show()
