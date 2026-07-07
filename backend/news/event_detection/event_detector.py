import re

class EventDetector:

    EVENT_PATTERNS = {

        "earnings": [
            "earnings",
            "quarterly results",
            "quarterly earnings",
            "annual results",
            "financial results",
            "revenue growth",
            "revenue increase",
            "profit",
            "net profit",
            "net income",
            "eps",
            "earnings beat",
            "earnings miss",
            "guidance raised",
            "guidance lowered",
            "record revenue",
            "strong results",
            "weak results",
        ],

        "management": [
            "ceo resigned",
            "ceo resigns",
            "ceo departure",
            "ceo change",
            "leadership change",
            "executive change",
            "management change",
            "chairman resigned",
            "cfo resigned",
            "new ceo",
            "new chairman",
            "board appointment",
            "board reshuffle",
        ],

        "corporate_action": [
            "buyback",
            "share buyback",
            "stock buyback",
            "dividend",
            "special dividend",
            "stock split",
            "bonus issue",
            "rights issue",
            "share issuance",
            "capital reduction",
        ],

        "regulatory": [
            "investigation",
            "regulatory investigation",
            "penalty",
            "fine",
            "compliance issue",
            "compliance violation",
            "regulatory action",
            "sebi",
            "sec",
            "warning notice",
            "regulatory approval",
            "approval received",
        ],

        "macro": [
            "inflation",
            "gdp",
            "interest rate",
            "rate hike",
            "rate cut",
            "central bank",
            "rbi",
            "federal reserve",
            "fed",
            "economic growth",
            "economic slowdown",
            "recession",
            "cpi",
            "monetary policy",
        ],

        "geopolitical": [
            "war",
            "sanction",
            "sanctions",
            "trade restriction",
            "trade ban",
            "military conflict",
            "border conflict",
            "political crisis",
            "geopolitical tension",
            "diplomatic dispute",
        ],

        "mergers_acquisitions": [
            "acquire",
            "acquires",
            "acquired",
            "acquisition",
            "acquisitions",
            "buyout",
            "takeover",
            "merger",
            "mergers",
            "merge",
            "merged",
            "purchase",
            "purchases",
            "purchased",
            "strategic acquisition",
        ],

        "partnerships": [
            "partnership",
            "partnerships",
            "strategic partnership",
            "collaboration",
            "collaborates",
            "joint venture",
            "joint ventures",
            "alliance",
            "strategic alliance",
            "agreement signed",
            "memorandum of understanding",
            "mou",
        ],

        "product_launch": [
            "introduces",
            "introduced",
            "unveils",
            "unveiled",
            "rollout",
            "product launch",
            "new product",
            "new service",
            "product unveiled",
            "service unveiled",
            "product introduced",
            "service introduced",
            "new platform",
            "new offering",
            "market debut",
            "commercial launch",
            "consumer launch",
        ],

        "funding": [
            "funding",
            "raises",
            "raised",
            "investment",
            "invests",
            "invested",
            "capital infusion",
            "venture funding",
            "seed funding",
            "series a",
            "series b",
            "series c",
            "private placement",
            "fund raising",
        ],

        "credit_rating": [
            "credit rating",
            "rating upgrade",
            "rating downgrade",
            "upgraded rating",
            "downgraded rating",
            "moody",
            "moody's",
            "fitch",
            "s&p",
            "credit outlook",
            "positive outlook",
            "negative outlook",
        ],

        "legal": [
            "lawsuit",
            "legal action",
            "court case",
            "litigation",
            "settlement",
            "class action",
            "class-action",
            "legal dispute",
            "sued",
            "court ruling",
            "judgment",
        ],

        "cybersecurity": [
            "data breach",
            "breach",
            "cyber attack",
            "cyberattack",
            "ransomware",
            "malware",
            "security incident",
            "security breach",
            "hack",
            "hacked",
            "data leak",
            "information leak",
            "compromised",
            "cybersecurity incident",
        ],

        "supply_chain": [
            "supply chain",
            "supply disruption",
            "factory shutdown",
            "production halt",
            "production disruption",
            "shortage",
            "inventory shortage",
            "logistics issue",
            "shipping delay",
            "raw material shortage",
            "plant closure",
        ],
    }

    def detect_events(
        self,
        text: str
    ):

        content = text.lower()

        detected_events = set()

        for event_type, keywords in (
            self.EVENT_PATTERNS.items()
        ):

            for keyword in keywords:

                pattern = rf"\b{re.escape(keyword)}\b"

                if re.search(pattern, content):

                    detected_events.add(
                        event_type
                    )

                    break

        return sorted(
            list(detected_events)
        )