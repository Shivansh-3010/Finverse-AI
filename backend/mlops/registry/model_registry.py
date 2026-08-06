from pathlib import Path
from datetime import datetime
import json


REGISTRY_DIR = (
    Path(__file__)
    .resolve()
    .parent
)


class ModelRegistry:

    @staticmethod
    def _registry_file(
        model_name: str,
        symbol: str,
        horizon: str,
    ):

        return (
            REGISTRY_DIR
            /
            f"{model_name.lower()}_{symbol.upper()}_{horizon}.json"
        )

    @staticmethod
    def register(
        model_name: str,
        symbol: str,
        horizon: str,
        version: str,
        metrics: dict,
        artifact_path: str,
    ):

        registry = {

            "model_name": model_name,

            "symbol": symbol.upper(),

            "horizon": horizon,

            "version": version,

            "training_date":
                datetime.utcnow().isoformat(),

            "artifact_path": artifact_path,

            "metrics": metrics,
        }

        file_path = (
            ModelRegistry._registry_file(
                model_name,
                symbol,
                horizon,
            )
        )

        with open(
            file_path,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                registry,
                f,
                indent=4,
            )

        return registry

    @staticmethod
    def load(
        model_name: str,
        symbol: str,
        horizon: str,
    ):

        file_path = (
            ModelRegistry._registry_file(
                model_name,
                symbol,
                horizon,
            )
        )

        if not file_path.exists():
            return None

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as f:

            return json.load(f)

    @staticmethod
    def exists(
        model_name: str,
        symbol: str,
        horizon: str,
    ):

        return (
            ModelRegistry
            ._registry_file(
                model_name,
                symbol,
                horizon,
            )
            .exists()
        )

    @staticmethod
    def delete(
        model_name: str,
        symbol: str,
        horizon: str,
    ):

        file_path = (
            ModelRegistry._registry_file(
                model_name,
                symbol,
                horizon,
            )
        )

        if file_path.exists():
            file_path.unlink()

    @staticmethod
    def list_models():

        models = []

        for file in (
            REGISTRY_DIR.glob("*.json")
        ):

            with open(
                file,
                "r",
                encoding="utf-8",
            ) as f:

                models.append(
                    json.load(f)
                )

        return sorted(
            models,
            key=lambda x:
                (
                    x["model_name"],
                    x["symbol"],
                    x["horizon"],
                )
        )
        
    @staticmethod
    def get(
        model_name: str,
        symbol: str,
        horizon: str,
    ):

        registry = (
            ModelRegistry.list_models()
        )

        for model in registry:

            if (
                model["model_name"] == model_name
                and model["symbol"] == symbol
                and model["horizon"] == horizon
            ):
                return model

        return {}