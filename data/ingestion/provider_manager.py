from yahoo_ingestor import YahooIngestor
from alpha_vantage_ingestor import AlphaVantageIngestor
from twelve_data_ingestor import TwelveDataIngestor


class ProviderManager:

    def __init__(self):

        self.yahoo = YahooIngestor()

        self.alpha_vantage = (
            AlphaVantageIngestor()
        )

        self.twelve_data = (
            TwelveDataIngestor()
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

        return providers