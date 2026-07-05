class MonitoringMetrics:

    articles_processed = 0

    embeddings_created = 0

    recommendations_generated = 0

    copilot_requests = 0

    prediction_mae = 0.0

    prediction_rmse = 0.0

    prediction_mape = 0.0

    prediction_directional_accuracy = 0.0

    prediction_inference_latency_ms = 0.0

    prediction_model_drift = 0.0

    @classmethod
    def increment_articles_processed(
        cls
    ):
        cls.articles_processed += 1

    @classmethod
    def increment_embeddings_created(
        cls
    ):
        cls.embeddings_created += 1

    @classmethod
    def increment_recommendations(
        cls
    ):
        cls.recommendations_generated += 1

    @classmethod
    def increment_copilot_requests(
        cls
    ):
        cls.copilot_requests += 1

    @classmethod
    def update_prediction_metrics(
        cls,
        mae: float,
        rmse: float,
        mape: float,
        directional_accuracy: float,
        inference_latency_ms: float = 0.0,
        model_drift: float = 0.0,
    ):

        cls.prediction_mae = mae
        cls.prediction_rmse = rmse
        cls.prediction_mape = mape
        cls.prediction_directional_accuracy = (
            directional_accuracy
        )
        cls.prediction_inference_latency_ms = (
            inference_latency_ms
        )
        cls.prediction_model_drift = (
            model_drift
        )

    @classmethod
    def get_metrics(
        cls
    ):

        return {

            "articles_processed":
                cls.articles_processed,

            "embeddings_created":
                cls.embeddings_created,

            "recommendations_generated":
                cls.recommendations_generated,

            "copilot_requests":
                cls.copilot_requests,

            "prediction_mae":
                cls.prediction_mae,

            "prediction_rmse":
                cls.prediction_rmse,

            "prediction_mape":
                cls.prediction_mape,

            "prediction_directional_accuracy":
                cls.prediction_directional_accuracy,

            "prediction_inference_latency_ms":
                cls.prediction_inference_latency_ms,

            "prediction_model_drift":
                cls.prediction_model_drift,
        }