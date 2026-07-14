from database.session import SessionLocal
from models.support_resistance import SupportResistance
from sqlalchemy import func

db = SessionLocal()

fields = [
    "nearest_support",
    "nearest_resistance",
    "support_strength",
    "resistance_strength",
    "distance_to_support_pct",
    "distance_to_resistance_pct",
    "breakout_zone_lower",
    "breakout_zone_upper",
    "breakdown_zone_lower",
    "breakdown_zone_upper",
    "signal_level",
]

total = (
    db.query(func.count())
    .select_from(SupportResistance)
    .scalar()
)

print(f"\nTotal rows: {total:,}\n")

for field in fields:

    count = (
        db.query(func.count())
        .filter(
            getattr(
                SupportResistance,
                field
            ).isnot(None)
        )
        .scalar()
    )

    pct = (count / total) * 100

    print(
        f"{field:<30}"
        f"{count:,} rows "
        f"({pct:.2f}%)"
    )

db.close()