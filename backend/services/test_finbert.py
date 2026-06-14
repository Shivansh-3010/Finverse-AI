from services.finbert_service import (
    FinBERTService
)

service = FinBERTService()

headlines = [
    "Reliance Industries reports strong quarterly earnings growth",
    "Company announces routine management update",
    "SEBI launches investigation into accounting fraud allegations"
]

for headline in headlines:
    print("\nHeadline:", headline)
    print(service.analyze(headline))