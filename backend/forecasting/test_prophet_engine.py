from database.session import SessionLocal

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from utils.ohlcv_dataframe import (
    ohlcv_to_dataframe,
)

from forecasting.prophet_engine import (
    ProphetEngine,
)


def test():

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

        prophet_df = df[
            [
                "timestamp",
                "close"
            ]
        ].copy()

        prophet_df.columns = [
            "ds",
            "y"
        ]
        
        prophet_df["ds"] = (
            prophet_df["ds"]
            .dt.tz_localize(None)
        )

        model = (
            ProphetEngine.build_model()
        )

        model.fit(
            prophet_df
        )

        future = (
            model.make_future_dataframe(
                periods=5
            )
        )

        forecast = (
            model.predict(
                future
            )
        )

        print(
            forecast[
                [
                    "ds",
                    "yhat",
                    "yhat_lower",
                    "yhat_upper",
                ]
            ].tail()
        )

    finally:
        db.close()


if __name__ == "__main__":
    test()