from database.session import (
    SessionLocal,
)

from services.transformer_prediction_service import (
    TransformerPredictionService,
)


def test():

    db = SessionLocal()

    try:

        result = (
            TransformerPredictionService.predict(
                db=db,
                symbol="RELIANCE",
                timeframe="1d",
            )
        )

        print(result)

    finally:
        db.close()


if __name__ == "__main__":
    test()