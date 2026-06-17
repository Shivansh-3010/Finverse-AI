import torch


class LSTMModelManager:

    @staticmethod
    def save(
        model,
        path: str,
    ):

        torch.save(
            model.state_dict(),
            path,
        )

    @staticmethod
    def load(
        model,
        path: str,
    ):

        model.load_state_dict(
            torch.load(
                path,
                map_location="cpu",
            )
        )

        model.eval()

        return model