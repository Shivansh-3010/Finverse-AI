from forecasting.adaptive_weight_engine import (
    AdaptiveWeightEngine,
)

from forecasting.ensemble_engine import (
    EnsembleEngine,
)

from services.model_comparison_service import (
    ModelComparisonService,
)

from services.model_leaderboard_service import (
    ModelLeaderboardService,
)


class EnsembleForecastService:

    REQUIRED_MODELS = (
        "xgboost",
        "prophet",
        "lstm",
        "transformer",
    )

    @staticmethod
    def forecast(
        db,
        symbol: str,
        timeframe: str = "1d",
        horizon: str = "1d",
        adaptive_weights: bool = True,
        leaderboard_window: int = 100,
    ):

        comparison = (
            ModelComparisonService.compare(
                db=db,
                symbol=symbol,
                timeframe=timeframe,
                horizon=horizon,
            )
        )

        predictions = {}

        for model_name in (
            EnsembleForecastService.REQUIRED_MODELS
        ):

            model_result = comparison.get(
                model_name,
            )

            if (
                not model_result
                or "predicted_return_pct"
                not in model_result
            ):
                continue

            predictions[model_name] = (
                model_result[
                    "predicted_return_pct"
                ]
            )

        if len(predictions) < 2:
            raise ValueError(
                "At least two model predictions are required "
                "to generate an ensemble forecast."
            )

        weights = None

        if adaptive_weights:

            leaderboard = (
                ModelLeaderboardService.leaderboard(
                    db=db,
                    symbol=symbol,
                    timeframe=timeframe,
                    window=leaderboard_window,
                )
            )

            if leaderboard:

                adaptive = (
                    AdaptiveWeightEngine.calculate(
                        leaderboard
                    )
                )

                if len(adaptive) >= 2:
                    weights = adaptive

        return EnsembleEngine.combine(
            predictions=predictions,
            comparison=comparison,
            weights=weights,
        )