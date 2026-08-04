from database.session import (
    SessionLocal,
)

from repositories.prediction_evaluation_repository import (
    PredictionEvaluationRepository,
)

from forecasting.backtest_engine import (
    BacktestEngine,
)


def test():

    db = SessionLocal()

    try:

        history = (
            PredictionEvaluationRepository(db)
            .get_history(
                symbol="RELIANCE",
                timeframe="1d",
            )
        )

        result = (
            BacktestEngine.run(
                history
            )
        )

        assert (
            "metrics"
            in result
        )

        assert (
            "equity_curve"
            in result
        )

        assert (
            result["trade_count"]
            == len(history)
        )

        print(result)

    finally:

        db.close()


if __name__ == "__main__":
    test()