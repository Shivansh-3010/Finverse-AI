from database.session import SessionLocal

from repositories.prediction_evaluation_repository import (
    PredictionEvaluationRepository,
)

from forecasting.evaluation_metrics_engine import (
    EvaluationMetricsEngine,
)


def test():

    db = SessionLocal()

    try:

        evaluations = (
            PredictionEvaluationRepository(db)
            .get_history(
                "RELIANCE",
                "1d"
            )
        )

        print(
            "Evaluation Count:",
            len(evaluations)
        )

        print(
            "MAE:",
            round(
                EvaluationMetricsEngine.mae(
                    evaluations
                ),
                4
            )
        )

        print(
            "RMSE:",
            round(
                EvaluationMetricsEngine.rmse(
                    evaluations
                ),
                4
            )
        )

        print(
            "Directional Accuracy:",
            round(
                EvaluationMetricsEngine.directional_accuracy(
                    evaluations
                ),
                2
            ),
            "%"
        )

    finally:
        db.close()


if __name__ == "__main__":
    test()