from database.session import SessionLocal

from forecasting.evaluation_engine import (
    EvaluationEngine,
)


def test():

    db = SessionLocal()

    try:

        result = (
            EvaluationEngine.evaluate(
                db=db,
                symbol="RELIANCE",
                timeframe="1d"
            )
        )

        print(result)

    finally:
        db.close()


if __name__ == "__main__":
    test()