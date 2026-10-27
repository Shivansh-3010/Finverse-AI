from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from agents.contracts import AgentStatus
from agents.state import AgentState


class CommitteeEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    agent_name: str
    field: str
    observed_value: str
    interpretation: Literal["bullish", "bearish", "neutral"]


class InvestmentCommitteeDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    recommendation: Literal[
        "BUY", "SELL", "HOLD", "INSUFFICIENT_DATA"
    ]
    confidence: float = Field(ge=0.0, le=1.0)
    consensus: str
    rationale: str
    supporting_evidence: list[CommitteeEvidence] = Field(default_factory=list)
    conflicting_evidence: list[CommitteeEvidence] = Field(default_factory=list)
    analyzed_agents: list[str] = Field(default_factory=list)
    failed_agents: list[str] = Field(default_factory=list)
    abstaining_agents: list[str] = Field(default_factory=list)


class InvestmentCommittee:
    """Aggregate agent evidence into a deterministic, auditable decision."""

    SIGNAL_FIELDS = {
        "signal",
        "recommendation",
        "direction",
        "market_signal",
        "trend_signal",
    }

    BULLISH_VALUES = {
        "bullish", "buy", "strong_buy", "positive",
        "uptrend", "bullish_breakout",
    }
    BEARISH_VALUES = {
        "bearish", "sell", "strong_sell", "negative",
        "downtrend", "bearish_breakdown",
    }
    NEUTRAL_VALUES = {
        "neutral", "hold", "sideways", "no_signal",
    }

    def analyze(self, state: AgentState) -> InvestmentCommitteeDecision:
        evidence: list[CommitteeEvidence] = []
        analyzed_agents: list[str] = []
        failed_agents: list[str] = []
        abstaining_agents: list[str] = []
        agent_votes: dict[str, set[str]] = {}

        for agent_name, result in state.results.items():
            if result.status == AgentStatus.FAILED:
                failed_agents.append(agent_name)
                continue

            if result.status not in (AgentStatus.SUCCESS, AgentStatus.PARTIAL):
                abstaining_agents.append(agent_name)
                continue

            analyzed_agents.append(agent_name)
            agent_evidence: list[CommitteeEvidence] = []

            def inspect(value: Any, path: str = "") -> None:
                if isinstance(value, dict):
                    for key, nested_value in value.items():
                        field_path = f"{path}.{key}" if path else str(key)
                        if str(key).lower() in self.SIGNAL_FIELDS:
                            interpretation = self._interpret(nested_value)
                            if interpretation is not None:
                                agent_evidence.append(
                                    CommitteeEvidence(
                                        agent_name=agent_name,
                                        field=field_path,
                                        observed_value=str(nested_value),
                                        interpretation=interpretation,
                                    )
                                )
                        inspect(nested_value, field_path)
                elif isinstance(value, list):
                    for index, item in enumerate(value):
                        inspect(item, f"{path}[{index}]")

            inspect(result.data)

            labels = {item.interpretation for item in agent_evidence}
            if not labels:
                abstaining_agents.append(agent_name)
            else:
                agent_votes[agent_name] = labels
                evidence.extend(agent_evidence)

        bullish_votes = sum(
            labels == {"bullish"} for labels in agent_votes.values()
        )
        bearish_votes = sum(
            labels == {"bearish"} for labels in agent_votes.values()
        )
        neutral_votes = sum(
            labels == {"neutral"} for labels in agent_votes.values()
        )

        conflicted_agents = {
            name for name, labels in agent_votes.items()
            if len(labels) > 1
        }
        conflicting_evidence = [
            item for item in evidence
            if item.agent_name in conflicted_agents
        ]

        directional_votes = bullish_votes + bearish_votes
        total_votes = len(agent_votes)

        if directional_votes == 0:
            recommendation = "HOLD" if neutral_votes else "INSUFFICIENT_DATA"
            confidence = 1.0 if neutral_votes and total_votes == neutral_votes else 0.0
            consensus = "neutral" if neutral_votes else "insufficient"
            rationale = (
                "Available recognized signals are neutral."
                if neutral_votes
                else "No usable recognized signals were available."
            )
        elif bullish_votes == bearish_votes:
            recommendation = "HOLD"
            confidence = 0.5
            consensus = "conflicted"
            rationale = "Bullish and bearish agent votes are tied."
        else:
            winner_votes = max(bullish_votes, bearish_votes)
            recommendation = "BUY" if bullish_votes > bearish_votes else "SELL"
            confidence = round(winner_votes / max(total_votes, 1), 4)
            consensus = "bullish" if recommendation == "BUY" else "bearish"
            rationale = (
                f"{bullish_votes} bullish, {bearish_votes} bearish, "
                f"and {neutral_votes} neutral agent votes."
            )

        if conflicting_evidence:
            rationale += (
                f" {len(conflicted_agents)} agent(s) produced conflicting "
                "signals and were not counted as directional votes."
            )

        if failed_agents:
            rationale += (
                f" {len(failed_agents)} agent(s) failed; "
                "the decision may be incomplete."
            )

        return InvestmentCommitteeDecision(
            recommendation=recommendation,
            confidence=confidence,
            consensus=consensus,
            rationale=rationale,
            supporting_evidence=[
                item for item in evidence
                if item not in conflicting_evidence
            ],
            conflicting_evidence=conflicting_evidence,
            analyzed_agents=analyzed_agents,
            failed_agents=failed_agents,
            abstaining_agents=sorted(set(abstaining_agents)),
        )

    @classmethod
    def _interpret(cls, value: Any) -> str | None:
        if not isinstance(value, str):
            return None

        normalized = value.strip().lower().replace(" ", "_").replace("-", "_")

        if normalized in cls.BULLISH_VALUES:
            return "bullish"
        if normalized in cls.BEARISH_VALUES:
            return "bearish"
        if normalized in cls.NEUTRAL_VALUES:
            return "neutral"

        return None
