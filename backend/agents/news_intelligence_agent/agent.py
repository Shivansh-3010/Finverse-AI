from backend.news.news_pipeline import (
    NewsPipeline
)


class NewsIntelligenceAgent:

    def __init__(self):

        self.pipeline = (
            NewsPipeline()
        )

    def analyze_news(
        self,
        headline: str
    ):

        return self.pipeline.analyze(
            headline
        )