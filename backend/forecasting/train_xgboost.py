from database.session import SessionLocal

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from utils.ohlcv_dataframe import (
    ohlcv_to_dataframe,
)

from forecasting.dataset_builder import (
    DatasetBuilder,
)

from forecasting.xgboost_engine import (
    XGBoostEngine,
)
from sklearn.model_selection import (
    train_test_split,
)
from forecasting.metrics_engine import (
    MetricsEngine,
)

def train():

    db = SessionLocal()

    try:

        records = (
            OHLCVRepository(db)
            .get_history_by_symbol_and_timeframe(
                symbol="RELIANCE",
                timeframe="1d"
            )
        )

        df = ohlcv_to_dataframe(
            records
        )

        dataset = (
            DatasetBuilder.build(df)
        )

        X = dataset[
            [
                "rsi",
                "macd",
                "macd_signal",
                "atr",
                "adx",
                "mfi",
                "obv",
                "vwap",
                "bb_upper",
                "bb_middle",
                "bb_lower",
            ]
        ]

        y = dataset["target"]

        model = (
            XGBoostEngine.build_model()
        )

        X_train, X_test, y_train, y_test = (
            train_test_split(
                X,
                y,
                test_size=0.2,
                shuffle=False
            )
        )

        model.fit(
            X_train,
            y_train
        )

        predictions = model.predict(
            X_test
        )
        
        mae = MetricsEngine.mae(
            y_test,
            predictions
        )

        rmse = MetricsEngine.rmse(
            y_test,
            predictions
        )

        mape = MetricsEngine.mape(
            y_test,
            predictions
        )

        directional_accuracy = (
            MetricsEngine.directional_accuracy(
                y_test.values,
                predictions
            )
        )

        print(
            "Training complete"
        )

        print(
            "Train Rows:",
            len(X_train)
        )

        print(
            "Test Rows:",
            len(X_test)
        )

        print(
            "MAE:",
            round(mae, 4)
        )

        print(
            "RMSE:",
            round(rmse, 4)
        )

        print(
            "MAPE:",
            round(mape, 4)
        )

        print(
            "Directional Accuracy:",
            round(
                directional_accuracy,
                2
            ),
            "%"
        )

    finally:
        db.close()


if __name__ == "__main__":
    train()