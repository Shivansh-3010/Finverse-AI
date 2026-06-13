from data.ingestion.yahoo_ingestor import (
    YahooIngestor,
)

from data.ingestion.alpha_vantage_ingestor import (
    AlphaVantageIngestor,
)

from data.ingestion.twelve_data_ingestor import (
    TwelveDataIngestor,
)

from data.ingestion.news.newsapi_ingestor import (
    NewsAPIIngestor,
)

from data.ingestion.news.finnhub_ingestor import (
    FinnhubIngestor,
)

from data.ingestion.news.marketaux_ingestor import (
    MarketauxIngestor,
)


class ProviderManager:

    def __init__(self):

        self.yahoo = YahooIngestor()

        self.alpha_vantage = (
            AlphaVantageIngestor()
        )

        self.twelve_data = (
            TwelveDataIngestor()
        )

        self.newsapi = (
            NewsAPIIngestor()
        )

        self.finnhub = (
            FinnhubIngestor()
        )

        self.marketaux = (
            MarketauxIngestor()
        )

    def available_providers(self):

        providers = ["Yahoo Finance"]

        if self.alpha_vantage.is_configured():
            providers.append(
                "Alpha Vantage"
            )

        if self.twelve_data.is_configured():
            providers.append(
                "Twelve Data"
            )

        if self.newsapi.is_configured():
            providers.append(
                "NewsAPI"
            )

        if self.finnhub.is_configured():
            providers.append(
                "Finnhub"
            )

        if self.marketaux.is_configured():
            providers.append(
                "Marketaux"
            )

        return providers