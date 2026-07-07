import numpy as np
import pandas as pd
from risk.risk_score_engine import (
    RiskScoreEngine
)

class HistoricalRiskEngine:

    @staticmethod
    def build_features(
        close_prices: pd.Series
    ) -> pd.DataFrame:

        returns = (
            close_prices
            .pct_change()
        )

        df = pd.DataFrame(
            index=close_prices.index
        )

        # Volatility

        df["volatility_252d"] = (
            returns
            .rolling(252)
            .std()
            * np.sqrt(252)
            * 100
        )

        df["volatility_504d"] = (
            returns
            .rolling(504)
            .std()
            * np.sqrt(252)
            * 100
        )

        # Drawdown

        rolling_max_252 = (
            close_prices
            .rolling(252)
            .max()
        )

        rolling_max_504 = (
            close_prices
            .rolling(504)
            .max()
        )

        df["drawdown_252d"] = (
            (
                close_prices
                - rolling_max_252
            )
            / rolling_max_252
            * 100
        )

        df["drawdown_504d"] = (
            (
                close_prices
                - rolling_max_504
            )
            / rolling_max_504
            * 100
        )

        # VaR

        df["var95_252d"] = (
            returns
            .rolling(252)
            .quantile(0.05)
            .abs()
            * 100
        )

        df["var95_504d"] = (
            returns
            .rolling(504)
            .quantile(0.05)
            .abs()
            * 100
        )
        
        df["expected_shortfall_252d"] = (
            HistoricalRiskEngine
            .rolling_expected_shortfall(
                returns,
                252
            )
        )

        df["expected_shortfall_504d"] = (
            HistoricalRiskEngine
            .rolling_expected_shortfall(
                returns,
                504
            )
        )
        
        risk_scores = []

        risk_categories = []

        for _, row in df.iterrows():

            if pd.isna(
                row["volatility_252d"]
            ):

                risk_scores.append(
                    np.nan
                )

                risk_categories.append(
                    None
                )

                continue

            score = (
                RiskScoreEngine.calculate_score(
                    volatility=row[
                        "volatility_252d"
                    ],
                    drawdown=row[
                        "drawdown_252d"
                    ],
                    var_95=row[
                        "var95_252d"
                    ],
                    expected_shortfall=row[
                        "expected_shortfall_252d"
                    ]
                )
            )

            risk_scores.append(
                score
            )

            risk_categories.append(
                RiskScoreEngine
                .classify_risk(
                    score
                )
            )

        df["risk_score"] = (
            risk_scores
        )

        df["risk_category"] = (
            risk_categories
        )

        return df
    
    @staticmethod
    def rolling_expected_shortfall(
        returns: pd.Series,
        window: int
    ):

        values = []

        for i in range(len(returns)):

            if i < window:

                values.append(np.nan)

                continue

            sample = returns.iloc[
                i - window:i
            ]

            threshold = sample.quantile(
                0.05
            )

            tail_losses = sample[
                sample <= threshold
            ]

            if len(tail_losses) == 0:

                values.append(0.0)

            else:

                values.append(
                    abs(
                        tail_losses.mean()
                    ) * 100
                )

        return pd.Series(
            values,
            index=returns.index
        )