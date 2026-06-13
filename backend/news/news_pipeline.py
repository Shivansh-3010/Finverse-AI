from backend.news.event_detection.event_detector import (
    EventDetector
)

from backend.news.event_detection.event_scoring import (
    EventScoring
)

from backend.news.news_score_engine import (
    NewsScoreEngine
)

from backend.news.news_score_interpreter import (
    NewsScoreInterpreter
)

from backend.services.finbert_service import (
    FinBERTService
)


class NewsPipeline:

    def __init__(self):

        self.finbert = (
            FinBERTService()
        )

        self.event_detector = (
            EventDetector()
        )

    def analyze(
        self,
        headline: str
    ):

        sentiment_result = (
            self.finbert.analyze(
                headline
            )
        )

        events = (
            self.event_detector
            .detect_events(
                headline
            )
        )

        event_score = (
            EventScoring.get_score(
                events
            )
        )

        news_score = (
            NewsScoreEngine
            .calculate_score(
                sentiment=
                    sentiment_result[
                        "sentiment"
                    ],

                confidence=
                    sentiment_result[
                        "confidence"
                    ],

                event_score=
                    event_score
            )
        )

        interpretation = (
            NewsScoreInterpreter
            .interpret(
                news_score
            )
        )

        return {

            "headline": headline,

            "events": events,

            "sentiment":
                sentiment_result[
                    "sentiment"
                ],

            "confidence":
                sentiment_result[
                    "confidence"
                ],

            "event_score":
                event_score,

            "news_score":
                news_score,

            "interpretation":
                interpretation
        }