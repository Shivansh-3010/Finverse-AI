from database.session import SessionLocal

from agents.prediction_agent.agent import (
    PredictionAgent,
)

from services.model_comparison_service import (
    ModelComparisonService,
)

from services.prediction_evaluation_service import (
    PredictionEvaluationService,
)

from services.model_leaderboard_service import (
    ModelLeaderboardService,
)

from repositories.prediction_evaluation_repository import (
    PredictionEvaluationRepository,
)

from forecasting.backtest_engine import (
    BacktestEngine,
)


class PredictionDashboardService:

    @staticmethod
    def dashboard(
        symbol: str,
        timeframe: str = "1d",
        horizon: str = "1d",
    ):

        db = SessionLocal()

        try:

            prediction = (
                PredictionAgent.predict(
                    symbol=symbol,
                    timeframe=timeframe,
                    horizon=horizon,
                )
            )

            comparison = (
                ModelComparisonService.compare(
                    db=db,
                    symbol=symbol,
                    timeframe=timeframe,
                    horizon=horizon,
                )
            )

            evaluation = (
                PredictionEvaluationService.summary(
                    db=db,
                    symbol=symbol,
                    timeframe=timeframe,
                )
            )

            leaderboard = (
                ModelLeaderboardService.leaderboard(
                    db=db,
                    symbol=symbol,
                    timeframe=timeframe,
                )
            )

            history = (
                PredictionEvaluationRepository(db)
                .get_history(
                    symbol=symbol,
                    timeframe=timeframe,
                )
            )

            backtest = (
                BacktestEngine.run(
                    history
                )
            )

            bullish = sum(

                1

                for model

                in comparison.values()

                if (
                    model.get(
                        "direction"
                    )
                    == "bullish"
                )

            )

            bearish = sum(

                1

                for model

                in comparison.values()

                if (
                    model.get(
                        "direction"
                    )
                    == "bearish"
                )

            )

            total_models = len(
                comparison
            )

            return {

                "forecast_card": {

                    "forecast":
                        prediction["forecast"],

                    "predicted_return_pct":
                        prediction[
                            "predicted_return_pct"
                        ],

                    "confidence":
                        prediction[
                            "confidence"
                        ],

                    "direction":
                        prediction[
                            "direction"
                        ],

                },

                "confidence_meter": {

                    "score":
                        prediction[
                            "confidence"
                        ],

                    "label":
                        prediction[
                            "confidence_label"
                        ],

                },

                "model_consensus": {

                    "bullish":
                        bullish,

                    "bearish":
                        bearish,

                    "total":
                        total_models,

                    "agreement":
                        prediction[
                            "agreement_score"
                        ],

                },

                "forecast_range": {

                    "prophet":

                        comparison.get(
                            "prophet",
                            {},
                        )

                },

                "leaderboard":
                    leaderboard,

                "evaluation":
                    evaluation,

                "backtest": {

                    "return":
                        backtest[
                            "metrics"
                        ][
                            "total_return"
                        ],

                    "sharpe":
                        backtest[
                            "metrics"
                        ][
                            "sharpe_ratio"
                        ],

                    "drawdown":
                        backtest[
                            "metrics"
                        ][
                            "max_drawdown"
                        ],

                    "trades":
                        backtest[
                            "trade_count"
                        ],

                },

                "models":
                    comparison,

            }

        finally:

            db.close()