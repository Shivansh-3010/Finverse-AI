import pandas as pd


class EventFeatureBuilder:

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
    }

    TRACKED_EVENTS = [

        "earnings",

        "funding",

        "regulatory",

        "macro",

        "mergers_acquisitions",
    ]

    @classmethod
    def build(
        cls,
        group: pd.DataFrame,
    ):

        result = {}

        event_score = 0

        events_series = (
            group["events"]
            .fillna("")
        )

        exploded_events = (
            events_series
            .str.split(",")
            .explode()
            .str.strip()
        )

        exploded_events = exploded_events[
            exploded_events != ""
        ]

        event_counts = (
            exploded_events
            .value_counts()
            .to_dict()
        )

        for event_name in cls.TRACKED_EVENTS:

            result[
                f"{event_name}_count"
            ] = int(
                event_counts.get(
                    event_name,
                    0
                )
            )

        for event_name, count in (
            event_counts.items()
        ):

            impact = (
                cls.EVENT_IMPACT.get(
                    event_name,
                    0
                )
            )

            event_score += (
                impact * count
            )

        event_score = max(
            -40,
            min(
                40,
                event_score
            )
        )

        result["event_score"] = float(
            event_score
        )

        return result