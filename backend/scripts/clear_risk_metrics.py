from database.session import SessionLocal
from sqlalchemy import text

db = SessionLocal()

try:
    result = db.execute(
        text("DELETE FROM risk_metrics")
    )

    db.commit()

    print(
        f"Deleted: {result.rowcount}"
    )

finally:
    db.close()