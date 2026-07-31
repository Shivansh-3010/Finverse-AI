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

        state_dict = torch.load(
            path,
            map_location="cpu",
        )

        model.load_state_dict(
            state_dict,
        )

        model.eval()

        return model