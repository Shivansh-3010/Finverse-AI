import pandas as pd

from database.session import SessionLocal

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from agents.risk_analysis_agent.agent import (
    RiskAnalysisAgent,
)
from datetime import datetime, timezone

from repositories.risk_metric_repository import (
    RiskMetricRepository,
)

from models.risk_metric import (
    RiskMetric,
)


class RiskAnalysisService:

    @staticmethod
    def analyze(
        symbol: str,
        timeframe: str = "1d"
    ):

        db = SessionLocal()

        try:

            repository = OHLCVRepository(db)

            records = (
                repository
                .get_history_by_symbol_and_timeframe(
                    symbol=symbol,
                    timeframe=timeframe
                )
            )

            close_prices = pd.Series(
                [record.close for record in records]
            )

            analysis = (
                RiskAnalysisAgent.analyze(
                    close_prices
                )
            )

            risk_repository = (
                RiskMetricRepository(db)
            )

            risk_repository.save(
                RiskMetric(
                    symbol=symbol,
                    timeframe=timeframe,
                    timestamp=datetime.now(
                        timezone.utc
                    ),
                    volatility=analysis[
                        "volatility"
                    ],
                    drawdown=analysis[
                        "drawdown"
                    ],
                    var_95=analysis[
                        "var_95"
                    ],
                    expected_shortfall=analysis[
                        "expected_shortfall"
                    ],
                    risk_score=analysis[
                        "risk_score"
                    ],
                    risk_category=analysis[
                        "risk_category"
                    ]
                )
            )

            return analysis

        finally:
            db.close()