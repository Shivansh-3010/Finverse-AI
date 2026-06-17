from database.session import SessionLocal

from services.ensemble_forecast_service import (
    EnsembleForecastService,
)


def test():

    db = SessionLocal()

    try:

        result = (
            EnsembleForecastService.forecast(
                db=db,
                symbol="RELIANCE",
                timeframe="1d"
            )
        )

        print(result)

    finally:
        db.close()


if __name__ == "__main__":
    test()