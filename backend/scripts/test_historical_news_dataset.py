import pandas as pd
from news.event_detection.event_detector import EventDetector

df = pd.read_csv(
    r"C:\Projects\Finverse-AI\datasets\historical_news\IndianFinancialNews.csv"
)

detector = EventDetector()

event_counts = {}

for _, row in df.head(1000).iterrows():

    text = (
        str(row["Title"])
        + " "
        + str(row["Description"])
    )

    events = detector.detect_events(
        text
    )

    for event in events:

        event_counts[event] = (
            event_counts.get(event, 0)
            + 1
        )

print(
    sorted(
        event_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )
)