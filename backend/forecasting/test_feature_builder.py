from database.session import SessionLocal

from forecasting.feature_builder import (
    FeatureBuilder,
)


def test_feature_builder():

    db = SessionLocal()

    try:

        features = (
            FeatureBuilder.build(
                db=db,
                symbol="RELIANCE",
                timeframe="1d"
            )
        )

        print(
            "Feature Count:",
            len(features)
        )

        print(
            "Features:",
            features
        )

    finally:
        db.close()


if __name__ == "__main__":
    test_feature_builder()