class EventScoring:

    EVENT_IMPACT = {

        "earnings": 15,

        "management": -8,

        "corporate_action": 10,

        "regulatory": -20,

        "macro": 5,

        "geopolitical": -10,

        "mergers_acquisitions": 12,

        "partnerships": 8,

        "product_launch": 10,

        "funding": 12,

        "credit_rating": 15,

        "legal": -15,

        "cybersecurity": -18,

        "supply_chain": -10,

        "unknown": 0,
    }

    @classmethod
    def get_score(
        cls,
        events: list
    ) -> int:

        total_score = 0

        for event in events:

            total_score += (
                cls.EVENT_IMPACT.get(
                    event,
                    0
                )
            )

        total_score = max(
            -40,
            min(
                40,
                total_score
            )
        )

        return total_score