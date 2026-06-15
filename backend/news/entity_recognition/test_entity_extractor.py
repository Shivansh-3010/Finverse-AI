from news.entity_recognition.entity_extractor import (
    EntityExtractor,
)

extractor = EntityExtractor()

headlines = [
    "Reliance Industries reports strong quarterly earnings growth",

    "SEBI launches investigation into accounting fraud allegations",

    "Mukesh Ambani announces major Jio expansion across India",
]

for headline in headlines:

    print("\nHeadline:")
    print(headline)

    print(
        extractor.extract(
            headline
        )
    )