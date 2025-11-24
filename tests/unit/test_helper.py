"""Unit tests for helper functions."""

from agent.agent import Agent
from environment.environment import Environment
from helper import (create_agents, randomly_place_agents, calculate_segregation_index,
                    calculate_happiness_rate, get_unhappy_agents, get_agent_counts_by_type)
from config import AGENT_TYPE_A, AGENT_TYPE_B


class TestCreateAgents:
    """Test agent creation."""

    def test_create_agents_count(self):
        agents = create_agents(10, 15, 0.3)
        assert len(agents) == 25

    def test_create_agents_types(self):
        agents = create_agents(10, 15, 0.3)

        type_a = sum(1 for a in agents if a.agent_type == AGENT_TYPE_A)
        type_b = sum(1 for a in agents if a.agent_type == AGENT_TYPE_B)

        assert type_a == 10
        assert type_b == 15

    def test_create_agents_threshold(self):
        agents = create_agents(10, 10, 0.7)

        for agent in agents:
            assert agent.similarity_threshold == 0.7


class TestRandomPlacement:
    """Test random agent placement."""

    def test_randomly_place_agents(self):
        env = Environment()
        agents = create_agents(20, 20, 0.3)

        randomly_place_agents(agents, env)

        # Check all agents placed
        for agent in agents:
            assert env.grid[agent.x, agent.y] == agent.agent_type

    def test_placement_raises_error_if_too_many_agents(self):
        import pytest

        env = Environment()
        # Try to place more agents than cells
        agents = create_agents(2000, 2000, 0.3)

        with pytest.raises(ValueError):
            randomly_place_agents(agents, env)


class TestSegregationIndex:
    """Test segregation calculation."""

    def test_segregation_empty(self):
        env = Environment()
        agents = []

        seg = calculate_segregation_index(agents, env)
        assert seg == 0.0

    def test_segregation_complete_separation(self):
        env = Environment()
        agents = []

        # All type A on left, type B on right
        for x in range(25):
            for y in range(10):
                agent = Agent(x=x, y=y, agent_type=AGENT_TYPE_A, similarity_threshold=0.3)
                env.place_agent(agent, x, y)
                agents.append(agent)

        for x in range(25, 50):
            for y in range(10):
                agent = Agent(x=x, y=y, agent_type=AGENT_TYPE_B, similarity_threshold=0.3)
                env.place_agent(agent, x, y)
                agents.append(agent)

        seg = calculate_segregation_index(agents, env)
        assert seg > 0.9  # High segregation

    def test_segregation_complete_separation(self):
        env = Environment()
        agents = []

        # All type A on left, type B on right
        for x in range(25):
            for y in range(10):
                agent = Agent(x=x, y=y, agent_type=AGENT_TYPE_A, similarity_threshold=0.3)
                env.place_agent(agent, x, y)
                agents.append(agent)

        for x in range(25, 50):
            for y in range(10):
                agent = Agent(x=x, y=y, agent_type=AGENT_TYPE_B, similarity_threshold=0.3)
                env.place_agent(agent, x, y)
                agents.append(agent)

        seg = calculate_segregation_index(agents, env)
        assert seg > 0.8  # High segregation


class TestHappinessRate:
    """Test happiness calculation."""

    def test_happiness_rate_empty(self):
        env = Environment()
        agents = []

        happiness = calculate_happiness_rate(agents, env)
        assert happiness == 0.0

    def test_happiness_rate_all_happy(self):
        env = Environment()
        agents = []

        # Cluster type A agents
        for x in range(5):
            for y in range(5):
                agent = Agent(x=x, y=y, agent_type=AGENT_TYPE_A, similarity_threshold=0.3)
                env.place_agent(agent, x, y)
                agents.append(agent)

        happiness = calculate_happiness_rate(agents, env)
        assert happiness > 0.9  # Most should be happy


class TestUnhappyAgents:
    """Test unhappy agent identification."""

    def test_get_unhappy_agents(self):
        env = Environment()

        # Create one unhappy agent surrounded by different type
        agent_a = Agent(x=25, y=25, agent_type=AGENT_TYPE_A, similarity_threshold=0.5)
        env.place_agent(agent_a, 25, 25)

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                agent_b = Agent(x=25 + dx, y=25 + dy, agent_type=AGENT_TYPE_B, similarity_threshold=0.3)
                env.place_agent(agent_b, 25 + dx, 25 + dy)

        agents = [agent_a]
        unhappy = get_unhappy_agents(agents, env)

        assert len(unhappy) == 1
        assert unhappy[0] == agent_a


class TestAgentCounts:
    """Test agent counting by type."""

    def test_get_agent_counts_by_type(self):
        agents = create_agents(30, 70, 0.3)

        counts = get_agent_counts_by_type(agents)

        assert counts['type_a'] == 30
        assert counts['type_b'] == 70

    def test_counts_empty_list(self):
        agents = []

        counts = get_agent_counts_by_type(agents)

        assert counts['type_a'] == 0
        assert counts['type_b'] == 0