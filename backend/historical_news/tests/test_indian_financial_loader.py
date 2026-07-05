from historical_news.loaders.indian_financial_loader import (
    IndianFinancialLoader,
)


def test_indian_financial_loader():

    loader = IndianFinancialLoader()

    records = loader.load(
        "../datasets/historical_news/IndianFinancialNews.csv"
    )

    assert len(records) > 0

    assert records[0].source == "indian_financial_news"

    assert records[0].title