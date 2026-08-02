class MonitoringMetrics:

    articles_processed = 0

    embeddings_created = 0

    recommendations_generated = 0

    copilot_requests = 0

    prediction_mae = 0.0

    prediction_rmse = 0.0

    prediction_mape = 0.0

    prediction_smape = 0.0

    prediction_directional_accuracy = 0.0

    prediction_hit_rate = 0.0

    prediction_mean_bias = 0.0

    prediction_max_absolute_error = 0.0

    prediction_inference_latency_ms = 0.0

    prediction_model_drift = 0.0

    @classmethod
    def increment_articles_processed(cls):
        cls.articles_processed += 1

    @classmethod
    def increment_embeddings_created(cls):
        cls.embeddings_created += 1

    @classmethod
    def increment_recommendations(cls):
        cls.recommendations_generated += 1

    @classmethod
    def increment_copilot_requests(cls):
        cls.copilot_requests += 1

    @classmethod
    def update_prediction_metrics(
        cls,
        mae: float,
        rmse: float,
        mape: float,
        smape: float = 0.0,
        directional_accuracy: float = 0.0,
        hit_rate: float = 0.0,
        mean_bias: float = 0.0,
        max_absolute_error: float = 0.0,
        inference_latency_ms: float = 0.0,
        model_drift: float = 0.0,
    ):

        cls.prediction_mae = mae
        cls.prediction_rmse = rmse
        cls.prediction_mape = mape
        cls.prediction_smape = smape
        cls.prediction_directional_accuracy = directional_accuracy
        cls.prediction_hit_rate = hit_rate
        cls.prediction_mean_bias = mean_bias
        cls.prediction_max_absolute_error = max_absolute_error
        cls.prediction_inference_latency_ms = inference_latency_ms
        cls.prediction_model_drift = model_drift

    @classmethod
    def get_metrics(cls):

        return {
            "articles_processed": cls.articles_processed,
            "embeddings_created": cls.embeddings_created,
            "recommendations_generated": cls.recommendations_generated,
            "copilot_requests": cls.copilot_requests,
            "prediction_mae": cls.prediction_mae,
            "prediction_rmse": cls.prediction_rmse,
            "prediction_mape": cls.prediction_mape,
            "prediction_smape": cls.prediction_smape,
            "prediction_directional_accuracy": cls.prediction_directional_accuracy,
            "prediction_hit_rate": cls.prediction_hit_rate,
            "prediction_mean_bias": cls.prediction_mean_bias,
            "prediction_max_absolute_error": cls.prediction_max_absolute_error,
            "prediction_inference_latency_ms": cls.prediction_inference_latency_ms,
            "prediction_model_drift": cls.prediction_model_drift,
        }