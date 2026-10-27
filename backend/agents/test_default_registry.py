from agents.default_registry import create_default_registry


EXPECTED_AGENTS = {
    "candlestick_analysis",
    "news_intelligence",
    "portfolio_intelligence",
    "prediction",
    "risk_analysis",
    "support_resistance",
    "technical_analysis",
}


def test_default_registry_registers_all_existing_agents():
    registry = create_default_registry()

    assert set(registry.list_agents()) == EXPECTED_AGENTS
    assert len(registry) == 7


def test_default_registry_entries_are_callable():
    registry = create_default_registry()

    for name in EXPECTED_AGENTS:
        assert callable(registry.get(name))


def test_creating_default_registry_does_not_import_agent_modules():
    registry = create_default_registry()

    assert len(registry) == 7
