from database.session import SessionLocal

from repositories.risk_metric_repository import (
    RiskMetricRepository,
)


def test_risk_history():

    db = SessionLocal()

    try:

        records = (
            RiskMetricRepository(db)
            .get_history(
                "RELIANCE",
                "1d"
            )
        )

        print(
            "Risk Count:",
            len(records)
        )

        if records:

            print(
                "First:",
                records[0].timestamp
            )

            print(
                "Last:",
                records[-1].timestamp
            )

            latest = records[-1]

            print(
                "Risk Score:",
                latest.risk_score
            )

            print(
                "Volatility 252d:",
                latest.volatility_252d
            )

            print(
                "Volatility 504d:",
                latest.volatility_504d
            )

    finally:
        db.close()


if __name__ == "__main__":
    test_risk_history()