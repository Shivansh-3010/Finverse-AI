from datetime import datetime, timezone
from typing import Any

import pandas as pd

from database.session import SessionLocal

from forecasting.forecast_preprocessing_pipeline import (
    ForecastPreprocessingPipeline,
)

from mlops.registry.model_registry import (
    ModelRegistry,
)

from repositories.prediction_repository import (
    PredictionRepository,
)


class MonitoringDataService:

    @staticmethod
    def _parse_training_date(
        training_date: str,
    ) -> datetime:

        value = datetime.fromisoformat(
            training_date
        )

        if value.tzinfo is None:
            value = value.replace(
                tzinfo=timezone.utc
            )

        return value

    @staticmethod
    def _prepare_features(
        db,
        symbol: str,
        timeframe: str,
    ) -> pd.DataFrame:

        result = (
            ForecastPreprocessingPipeline.prepare(
                db=db,
                symbol=symbol,
                timeframe=timeframe,
                build_sequences=False,
            )
        )

        dataset = result["dataset"].copy()

        if "timestamp" not in dataset.columns:
            raise ValueError(
                "Forecast dataset does not contain timestamp column"
            )

        dataset["timestamp"] = pd.to_datetime(
            dataset["timestamp"],
            utc=True,
        )

        feature_columns = [
            column
            for column in dataset.columns
            if column not in {
                "timestamp",
                "target",
            }
        ]

        return dataset[
            ["timestamp"] + feature_columns
        ]

    @staticmethod
    def _split_features(
        dataset: pd.DataFrame,
        training_date: datetime,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:

        training = (
            dataset[
                dataset["timestamp"]
                <= training_date
            ]
            .copy()
        )

        production = (
            dataset[
                dataset["timestamp"]
                > training_date
            ]
            .copy()
        )

        training = training.drop(
            columns=["timestamp"]
        )

        production = production.drop(
            columns=["timestamp"]
        )

        return (
            training.reset_index(drop=True),
            production.reset_index(drop=True),
        )

    @staticmethod
    def _prediction_values(
        predictions,
    ) -> list[float]:

        return [
            float(
                prediction.prediction
            )
            for prediction in predictions
        ]

    @staticmethod
    def get_model_data(
        model_name: str,
        symbol: str,
        timeframe: str,
        horizon: str,
        recent_prediction_limit: int = 50,
    ) -> dict[str, Any]:

        registry = (
            ModelRegistry.get(
                model_name=model_name,
                symbol=symbol,
                horizon=horizon,
            )
        )

        if not registry:
            raise ValueError(
                f"Model registry entry not found: "
                f"{model_name}/{symbol}/{horizon}"
            )

        training_date = (
            MonitoringDataService
            ._parse_training_date(
                registry["training_date"]
            )
        )

        db = SessionLocal()

        try:

            feature_dataset = (
                MonitoringDataService
                ._prepare_features(
                    db=db,
                    symbol=symbol,
                    timeframe=timeframe,
                )
            )

            (
                training_features,
                production_features,
            ) = (
                MonitoringDataService
                ._split_features(
                    dataset=feature_dataset,
                    training_date=training_date,
                )
            )

            repository = (
                PredictionRepository(db)
            )

            historical_rows = (
                repository.get_history_by_model(
                    symbol=symbol,
                    timeframe=timeframe,
                    horizon=horizon,
                    model_name=model_name,
                )
            )

            recent_rows = (
                repository.get_recent_history_by_model(
                    symbol=symbol,
                    timeframe=timeframe,
                    horizon=horizon,
                    model_name=model_name,
                    limit=recent_prediction_limit,
                )
            )

            historical_predictions = (
                MonitoringDataService
                ._prediction_values(
                    historical_rows
                )
            )

            recent_predictions = (
                MonitoringDataService
                ._prediction_values(
                    recent_rows
                )
            )

            return {

                "model": model_name,

                "symbol": symbol,

                "timeframe": timeframe,

                "horizon": horizon,

                "training_date":
                    registry[
                        "training_date"
                    ],

                "training_features":
                    training_features,

                "production_features":
                    production_features,

                "historical_predictions":
                    historical_predictions,

                "recent_predictions":
                    recent_predictions,

                "prediction_count":
                    len(
                        historical_predictions
                    ),

                "recent_prediction_count":
                    len(
                        recent_predictions
                    ),
            }

        finally:
            db.close()

    @staticmethod
    def get_prediction_data(
        model_name: str,
        symbol: str,
        timeframe: str,
        horizon: str,
        recent_prediction_limit: int = 50,
    ) -> dict[str, Any]:

        db = SessionLocal()

        try:

            repository = (
                PredictionRepository(db)
            )

            historical_rows = (
                repository.get_history_by_model(
                    symbol=symbol,
                    timeframe=timeframe,
                    horizon=horizon,
                    model_name=model_name,
                )
            )

            recent_rows = (
                repository.get_recent_history_by_model(
                    symbol=symbol,
                    timeframe=timeframe,
                    horizon=horizon,
                    model_name=model_name,
                    limit=recent_prediction_limit,
                )
            )

            return {

                "model": model_name,

                "symbol": symbol,

                "timeframe": timeframe,

                "horizon": horizon,

                "historical_predictions":
                    MonitoringDataService
                    ._prediction_values(
                        historical_rows
                    ),

                "recent_predictions":
                    MonitoringDataService
                    ._prediction_values(
                        recent_rows
                    ),
            }

        finally:
            db.close()