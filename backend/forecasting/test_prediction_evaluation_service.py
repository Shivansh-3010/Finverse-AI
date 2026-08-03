from database.session import SessionLocal

from services.prediction_evaluation_service import (
    PredictionEvaluationService,
)


def test():

    db = SessionLocal()

    try:

        result = (
            PredictionEvaluationService.summary(
                db=db,
                symbol="RELIANCE",
            )
        )

        assert "overall" in result
        assert "rolling" in result
        assert "models" in result
        assert "leaderboard" in result

        print(result)

    finally:

        db.close()