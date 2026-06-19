from pathlib import Path
import pandas as pd

folder = Path(
    r"C:\Projects\Finverse-AI\datasets\company_news"
)

total_rows = 0

for file in folder.glob("*.csv"):

    df = pd.read_csv(file)

    total_rows += len(df)

print(
    "Files:",
    len(
        list(
            folder.glob("*.csv")
        )
    )
)

print(
    "Total Articles:",
    total_rows
)