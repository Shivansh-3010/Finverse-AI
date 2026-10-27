import pytest

from agents.registry import AgentRegistry


def sample_agent(value=1):
    return {"value": value}


def test_register_and_retrieve_agent():
    registry = AgentRegistry()
    registry.register("sample", sample_agent)

    assert registry.get("sample") is sample_agent
    assert registry.get("sample")(42) == {"value": 42}


def test_registration_normalizes_name_whitespace():
    registry = AgentRegistry()
    registry.register("  sample  ", sample_agent)

    assert registry.contains("sample")
    assert registry.get(" sample ") is sample_agent


def test_duplicate_registration_is_rejected():
    registry = AgentRegistry()
    registry.register("sample", sample_agent)

    with pytest.raises(ValueError, match="already registered"):
        registry.register("sample", sample_agent)


def test_explicit_replacement_is_supported():
    registry = AgentRegistry()
    replacement = lambda: {"replacement": True}
    registry.register("sample", sample_agent)
    registry.register("sample", replacement, replace=True)

    assert registry.get("sample") is replacement


def test_empty_name_is_rejected():
    registry = AgentRegistry()

    with pytest.raises(ValueError, match="cannot be empty"):
        registry.register("   ", sample_agent)


def test_non_callable_agent_is_rejected():
    registry = AgentRegistry()

    with pytest.raises(TypeError, match="must be callable"):
        registry.register("sample", 123)


def test_missing_agent_raises_clear_error():
    registry = AgentRegistry()

    with pytest.raises(KeyError, match="not registered"):
        registry.get("unknown")


def test_list_agents_and_length():
    registry = AgentRegistry()
    registry.register("first", sample_agent)
    registry.register("second", sample_agent)

    assert registry.list_agents() == ["first", "second"]
    assert len(registry) == 2


def test_contains_returns_false_for_unknown_agent():
    registry = AgentRegistry()

    assert not registry.contains("unknown")
