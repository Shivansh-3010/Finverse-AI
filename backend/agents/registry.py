from collections.abc import Callable
from typing import Any


class AgentRegistry:
    """Central registry for callable FinVerse AI agents."""

    def __init__(self) -> None:
        self._agents: dict[str, Callable[..., Any]] = {}

    def register(
        self,
        name: str,
        agent: Callable[..., Any],
        *,
        replace: bool = False,
    ) -> None:
        normalized_name = name.strip()

        if not normalized_name:
            raise ValueError("Agent name cannot be empty.")

        if not callable(agent):
            raise TypeError("Registered agent must be callable.")

        if normalized_name in self._agents and not replace:
            raise ValueError(
                f"Agent '{normalized_name}' is already registered."
            )

        self._agents[normalized_name] = agent

    def get(self, name: str) -> Callable[..., Any]:
        normalized_name = name.strip()

        try:
            return self._agents[normalized_name]
        except KeyError:
            raise KeyError(
                f"Agent '{normalized_name}' is not registered."
            ) from None

    def list_agents(self) -> list[str]:
        return list(self._agents.keys())

    def contains(self, name: str) -> bool:
        return name.strip() in self._agents

    def __len__(self) -> int:
        return len(self._agents)
