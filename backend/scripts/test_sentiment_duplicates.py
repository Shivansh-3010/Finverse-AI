# backend/scripts/test_sentiment_duplicates.py

import pandas as pd

df = pd.read_csv(
    r"C:\Projects\Finverse-AI\datasets\historical_news\News_sentiment_Jan2017_to_Apr2021.csv"
)

print("Rows:", len(df))

print(
    "Unique URLs:",
    df["URL"].nunique()
)

print(
    "Duplicate URLs:",
    len(df) - df["URL"].nunique()
)