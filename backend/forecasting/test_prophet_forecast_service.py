from database.session import SessionLocal

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from utils.ohlcv_dataframe import (
    ohlcv_to_dataframe,
)

from services.prophet_forecast_service import (
    ProphetForecastService,
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

        result = (
            ProphetForecastService.forecast(
                prophet_df=prophet_df,
                periods=5
            )
        )

        print(result)

    finally:
        db.close()


if __name__ == "__main__":
    test()