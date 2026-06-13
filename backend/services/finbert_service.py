from transformers import pipeline


class FinBERTService:

    def __init__(self):

        self.classifier = pipeline(
            "text-classification",
            model="ProsusAI/finbert"
        )

    def analyze(
        self,
        text: str
    ):

        result = self.classifier(text)[0]

        return {
            "sentiment": result["label"].lower(),
            "confidence": float(
                result["score"]
            )
        }