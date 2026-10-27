from importlib import import_module
from typing import Any, Callable

from agents.registry import AgentRegistry


def _lazy_agent_call(
    module_path: str,
    class_name: str,
    method_name: str,
) -> Callable[..., Any]:
    """Load an agent implementation only when it is called."""

    def invoke(*args: Any, **kwargs: Any) -> Any:
        module = import_module(module_path)
        agent_class = getattr(module, class_name)
        agent = agent_class()
        method = getattr(agent, method_name)
        return method(*args, **kwargs)

    return invoke


def create_default_registry() -> AgentRegistry:
    """Build a registry of existing FinVerse agent entry points."""

    registry = AgentRegistry()

    agent_definitions = {
        "candlestick_analysis": (
            "agents.candlestick_analysis_agent.agent",
            "CandlestickAnalysisAgent",
            "analyze",
        ),
        "news_intelligence": (
            "agents.news_intelligence_agent.agent",
            "NewsIntelligenceAgent",
            "analyze_news",
        ),
        "portfolio_intelligence": (
            "agents.portfolio_intelligence_agent.agent",
            "PortfolioIntelligenceAgent",
            "analyze",
        ),
        "prediction": (
            "agents.prediction_agent.agent",
            "PredictionAgent",
            "predict",
        ),
        "risk_analysis": (
            "agents.risk_analysis_agent.agent",
            "RiskAnalysisAgent",
            "analyze",
        ),
        "support_resistance": (
            "agents.support_resistance_agent.agent",
            "SupportResistanceAgent",
            "analyze",
        ),
        "technical_analysis": (
            "agents.technical_analysis_agent.agent",
            "TechnicalAnalysisAgent",
            "analyze",
        ),
    }

    for name, (module_path, class_name, method_name) in agent_definitions.items():
        registry.register(
            name,
            _lazy_agent_call(module_path, class_name, method_name),
        )

    return registry
