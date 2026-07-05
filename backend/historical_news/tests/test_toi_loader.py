from historical_news.loaders.toi_loader import TOILoader


def test_toi_loader():

    loader = TOILoader()

    records = loader.load(
        "../datasets/historical_news/india-news-headlines.csv"
    )

    assert len(records) > 100000

    assert records[0].source == "toi_business"

    assert records[0].title