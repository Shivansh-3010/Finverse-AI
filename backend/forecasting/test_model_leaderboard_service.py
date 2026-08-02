from services.model_leaderboard_service import (
    ModelLeaderboardService,
)


def test():

    assert (
        hasattr(
            ModelLeaderboardService,
            "leaderboard",
        )
    )