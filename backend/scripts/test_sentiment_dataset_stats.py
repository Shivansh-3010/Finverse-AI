
import pandas as pd

df = pd.read_csv(
    r"C:\Projects\Finverse-AI\datasets\historical_news\News_sentiment_Jan2017_to_Apr2021.csv"
)

print("Rows:", len(df))

print(
    "Earliest:",
    pd.to_datetime(
        df["Date"],
        format="%d/%m/%y"
    ).min()
)

print(
    "Latest:",
    pd.to_datetime(
        df["Date"],
        format="%d/%m/%y"
    ).max()
)

print(
    "\nSentiment Distribution:"
)

print(
    df["sentiment"]
    .value_counts()
)