from services.monitoring_data_service import (
    MonitoringDataService,
)


def test():

    result = (
        MonitoringDataService.get_model_data(
            model_name="xgboost",
            symbol="RELIANCE",
            timeframe="1d",
            horizon="5d",
        )
    )

    print(
        {
            "model": result["model"],
            "symbol": result["symbol"],
            "horizon": result["horizon"],
            "training_date": result["training_date"],
            "training_rows": len(
                result["training_features"]
            ),
            "production_rows": len(
                result["production_features"]
            ),
            "historical_predictions":
                len(
                    result[
                        "historical_predictions"
                    ]
                ),
            "recent_predictions":
                len(
                    result[
                        "recent_predictions"
                    ]
                ),
            "feature_count":
                len(
                    result[
                        "training_features"
                    ].columns
                ),
        }
    )