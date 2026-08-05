from database.session import SessionLocal

from feature_store.prediction.prediction_features import (
    PredictionFeatureStore,
)


def test():

    db = SessionLocal()

    try:

        result = (
            PredictionFeatureStore.latest(
                db=db,
                symbol="RELIANCE",
            )
        )

        print(result)

        assert isinstance(
            result,
            dict,
        )

    finally:

        db.close()


if __name__ == "__main__":
    test()