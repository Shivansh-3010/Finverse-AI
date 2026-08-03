class ConfidenceEngine:

    MAE_WEIGHT = 0.25
    RMSE_WEIGHT = 0.20
    MAPE_WEIGHT = 0.10
    DIRECTIONAL_WEIGHT = 0.25
    HIT_RATE_WEIGHT = 0.10
    AGREEMENT_WEIGHT = 0.10

    @staticmethod
    def calculate(
        mae: float,
        directional_accuracy: float,
        rmse: float = 0.0,
        mape: float = 0.0,
        hit_rate: float = 100.0,
        agreement_score: float = 100.0,
    ) -> float:

        mae_score = max(
            0.0,
            100.0 - (mae * 20.0),
        )

        rmse_score = max(
            0.0,
            100.0 - (rmse * 20.0),
        )

        mape_score = max(
            0.0,
            100.0 - mape,
        )

        confidence = (

            mae_score
            * ConfidenceEngine.MAE_WEIGHT

            +

            rmse_score
            * ConfidenceEngine.RMSE_WEIGHT

            +

            mape_score
            * ConfidenceEngine.MAPE_WEIGHT

            +

            directional_accuracy
            * ConfidenceEngine.DIRECTIONAL_WEIGHT

            +

            hit_rate
            * ConfidenceEngine.HIT_RATE_WEIGHT

            +

            agreement_score
            * ConfidenceEngine.AGREEMENT_WEIGHT
        )

        return round(
            max(
                0.0,
                min(
                    confidence,
                    100.0,
                ),
            ),
            2,
        )