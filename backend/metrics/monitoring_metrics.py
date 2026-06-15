class MonitoringMetrics:

    articles_processed = 0

    embeddings_created = 0

    recommendations_generated = 0

    copilot_requests = 0

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
        }