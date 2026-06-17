from database.session import (
    SessionLocal,
)

from services.lstm_prediction_service import (
    LSTMPredictionService,
)


def test():

    db = SessionLocal()

    try:

        result = (
            LSTMPredictionService.predict(
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