from database.session import SessionLocal

from services.model_comparison_service import (
    ModelComparisonService,
)


def test():

    db = SessionLocal()

    try:

        result = (
            ModelComparisonService.compare(
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