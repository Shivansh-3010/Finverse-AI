from database.session import SessionLocal

from repositories.news_article_repository import (
    NewsArticleRepository,
)
from news.event_detection.event_scoring import (
    EventScoring,
)
from services.technical_analysis_service import (
    TechnicalAnalysisService,
)
from metrics.monitoring_metrics import (
    MonitoringMetrics,
)

class RecommendationService:

    @staticmethod
    def get_news_metrics(
        symbol: str
    ):

        db = SessionLocal()

        try:

            repository = (
                NewsArticleRepository(db)
            )

            history = (
                repository.get_history(
                    symbol
                )
            )

            if not history:

                return {
                    "recent_news_average": 50,
                    "latest_news_score": 50,
                    "latest_events": []
                }

            recent_articles = (
                history[-10:]
            )

            recent_average = round(
                sum(
                    article.news_score
                    for article in recent_articles
                ) / len(recent_articles)
            )

            latest_article = (
                history[-1]
            )

            return {
                "recent_news_average":
                    recent_average,

                "latest_news_score":
                    latest_article.news_score,

                "latest_events":
                    latest_article.events.split(",")
                    if latest_article.events
                    else []
            }

        finally:
            db.close()
            
    @staticmethod
    def calculate_news_intelligence(
        recent_average: int,
        latest_score: int
    ):

        return round(
            (recent_average * 0.60)
            +
            (latest_score * 0.40)
        )
        
    @staticmethod
    def calculate_event_adjustment(
        events: list
    ):

        return EventScoring.get_score(
            events
        )
        
    @staticmethod
    def calculate_final_score(
        combined_score: int,
        news_intelligence_score: int,
        event_adjustment: int
    ):

        adjusted_news_score = (
            news_intelligence_score
            +
            round(event_adjustment * 0.5)
        )

        adjusted_news_score = max(
            0,
            min(
                100,
                adjusted_news_score
            )
        )

        final_score = round(
            (combined_score * 0.70)
            +
            (adjusted_news_score * 0.30)
        )

        return {
            "adjusted_news_score":
                adjusted_news_score,

            "final_score":
                final_score
        }

    @staticmethod
    def get_recommendation(
        final_score: int
    ):

        if final_score >= 80:
            return "BUY"

        if final_score >= 60:
            return "HOLD"

        return "SELL"
    
    @staticmethod
    def generate(
        symbol: str,
        timeframe: str = "1d"
    ):

        technical_result = (
            TechnicalAnalysisService.analyze(
                symbol=symbol,
                timeframe=timeframe
            )
        )
        if "combined_score" not in technical_result:

            return {
                "symbol": symbol,
                "recommendation": "UNKNOWN",
                "error": "No technical data available",
                "technical_result": technical_result
            }

        metrics = (
            RecommendationService
            .get_news_metrics(
                symbol
            )
        )

        news_intelligence = (
            RecommendationService
            .calculate_news_intelligence(
                metrics[
                    "recent_news_average"
                ],
                metrics[
                    "latest_news_score"
                ]
            )
        )

        event_adjustment = (
            RecommendationService
            .calculate_event_adjustment(
                metrics[
                    "latest_events"
                ]
            )
        )

        score_result = (
            RecommendationService
            .calculate_final_score(
                combined_score=
                    technical_result[
                        "combined_score"
                    ],

                news_intelligence_score=
                    news_intelligence,

                event_adjustment=
                    event_adjustment
            )
        )

        recommendation = (
            RecommendationService
            .get_recommendation(
                score_result[
                    "final_score"
                ]
            )
        )
        
        MonitoringMetrics.increment_recommendations()

        return {

            "technical_score":
                technical_result[
                    "technical_score"
                ],

            "candlestick_score":
                technical_result[
                    "candlestick_score"
                ],

            "combined_score":
                technical_result[
                    "combined_score"
                ],

            "recent_news_average":
                metrics[
                    "recent_news_average"
                ],

            "latest_news_score":
                metrics[
                    "latest_news_score"
                ],

            "news_intelligence_score":
                news_intelligence,

            "event_adjustment":
                event_adjustment,

            "adjusted_news_score":
                score_result[
                    "adjusted_news_score"
                ],

            "final_score":
                score_result[
                    "final_score"
                ],

            "recommendation":
                recommendation,

            "trend":
                technical_result[
                    "trend"
                ],

            "rsi":
                technical_result[
                    "rsi"
                ],

            "reasons":
                technical_result[
                    "reasons"
                ],

            "candlestick_patterns":
                technical_result[
                    "candlestick_patterns"
                ],

            "latest_events":
                metrics[
                    "latest_events"
                ]
        }