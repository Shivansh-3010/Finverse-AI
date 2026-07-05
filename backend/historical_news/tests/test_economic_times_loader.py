from historical_news.loaders.economic_times_loader import (
    EconomicTimesLoader,
)


def test_economic_times_loader():

    loader = EconomicTimesLoader()

    records = loader.load_directory(
        "../datasets/historical_news"
    )

    assert len(records) > 300000

    assert records[0].source == "economic_times"

    assert records[0].title