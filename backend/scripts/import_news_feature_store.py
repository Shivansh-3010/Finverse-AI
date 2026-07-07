import pandas as pd
from tqdm import tqdm

from database.session import SessionLocal
from models.news_feature_daily import (
    NewsFeatureDaily,
)


BATCH_SIZE = 1000


def main():

    df = pd.read_csv(
        "../datasets/historical_news_processed/news_features_daily_v2.csv"
    )

    df["date"] = pd.to_datetime(
        df["date"]
    ).dt.date

    db = SessionLocal()

    try:

        total_rows = len(df)

        for start in tqdm(
            range(
                0,
                total_rows,
                BATCH_SIZE
            )
        ):

            end = min(
                start + BATCH_SIZE,
                total_rows
            )

            batch = df.iloc[start:end]

            objects = []

            for row in batch.to_dict(
                orient="records"
            ):

                objects.append(
                    NewsFeatureDaily(**row)
                )

            db.bulk_save_objects(
                objects
            )

            db.commit()

        print(
            f"Imported {total_rows} rows"
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()