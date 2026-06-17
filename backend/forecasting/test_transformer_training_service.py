from database.session import (
    SessionLocal,
)

from services.transformer_training_service import (
    TransformerTrainingService,
)


def test():

    db = SessionLocal()

    try:

        result = (
            TransformerTrainingService.train(
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