import pandas as pd

df = pd.read_csv(
    r"C:\Projects\Finverse-AI\datasets\company_news\reliance_industries_ri_news.csv"
)

dates = pd.to_datetime(
    df["Date"],
    dayfirst=True,
)

print(
    "Rows:",
    len(df)
)

print(
    "Earliest:",
    dates.min()
)

print(
    "Latest:",
    dates.max()
)