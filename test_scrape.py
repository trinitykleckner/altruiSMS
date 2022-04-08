from pprint import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import praw
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

user_agent = "Scraper 1.0 by /u/Reimann_Xheta"
reddit = praw.Reddit(
    client_id="UN3TZUSopOgkP8wnEbtfqQ",
    client_secret="xga026JZat_Orx2HKImnGbb7hPe5ug",
    user_agent=user_agent
)

posts = []


def subreddit_scrape(altruisms: list) -> pd.DataFrame:
    for sub in altruisms:
        ml_subreddit = reddit.subreddit(sub)
        for post in ml_subreddit.new(limit=1):
            posts.append(
                [post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext,
                 post.created])
    return pd.DataFrame(posts, columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])


df = subreddit_scrape(['freebies', 'Freefood'])
print(df)
