from database.session import (
    SessionLocal,
)

from services.lstm_training_service import (
    LSTMTrainingService,
)


def test():

    db = SessionLocal()

    try:

        result = (
            LSTMTrainingService.train(
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