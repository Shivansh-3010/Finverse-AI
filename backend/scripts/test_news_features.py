from database.session import SessionLocal

from forecasting.feature_builder import (
    FeatureBuilder,
)

db = SessionLocal()

try:

    features = (
        FeatureBuilder.build(
            db=db,
            symbol="RELIANCE",
            timeframe="1d",
        )
    )

    print(
        "Feature Count:",
        len(features)
    )

    print(
        "Last 7 News Features:"
    )

    print(
        features[-7:]
    )

finally:

    db.close()