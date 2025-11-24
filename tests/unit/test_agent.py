"""Unit tests for Agent class."""

from agent.agent import Agent
from environment.environment import Environment
from config import AGENT_TYPE_A, AGENT_TYPE_B, GRID_SIZE


class TestAgentInitialization:
    """Test agent creation."""

    def test_agent_creation(self):
        agent = Agent(x=10, y=20, agent_type=AGENT_TYPE_A, similarity_threshold=0.3)
        assert agent.x == 10
        assert agent.y == 20
        assert agent.agent_type == AGENT_TYPE_A
        assert agent.similarity_threshold == 0.3


class TestAgentHappiness:
    """Test happiness calculation."""

    def test_agent_happy_with_similar_neighbors(self):
        env = Environment()
        agent = Agent(x=25, y=25, agent_type=AGENT_TYPE_A, similarity_threshold=0.5)
        env.grid[25, 25] = AGENT_TYPE_A

        # Place similar neighbors
        env.grid[24, 25] = AGENT_TYPE_A
        env.grid[26, 25] = AGENT_TYPE_A
        env.grid[25, 24] = AGENT_TYPE_A

        assert agent.is_happy(env) == True

    def test_agent_unhappy_with_different_neighbors(self):
        env = Environment()
        agent = Agent(x=25, y=25, agent_type=AGENT_TYPE_A, similarity_threshold=0.5)
        env.grid[25, 25] = AGENT_TYPE_A

        # Place different neighbors
        env.grid[24, 25] = AGENT_TYPE_B
        env.grid[26, 25] = AGENT_TYPE_B
        env.grid[25, 24] = AGENT_TYPE_B

        assert agent.is_happy(env) == False

    def test_agent_unhappy_when_isolated(self):
        env = Environment()
        agent = Agent(x=25, y=25, agent_type=AGENT_TYPE_A, similarity_threshold=0.3)
        env.grid[25, 25] = AGENT_TYPE_A

        # All neighbors empty
        assert agent.is_happy(env) == False


class TestAgentNeighborhood:
    """Test neighborhood detection."""

    def test_get_neighbor_positions_count(self):
        agent = Agent(x=25, y=25, agent_type=AGENT_TYPE_A, similarity_threshold=0.3)
        neighbors = agent.get_neighbor_positions()
        assert len(neighbors) == 8  # Moore neighborhood

    def test_neighbor_positions_wrapping(self):
        agent = Agent(x=0, y=0, agent_type=AGENT_TYPE_A, similarity_threshold=0.3)
        neighbors = agent.get_neighbor_positions()

        # Should wrap around grid
        assert (GRID_SIZE - 1, GRID_SIZE - 1) in neighbors
        assert (0, GRID_SIZE - 1) in neighbors
        assert (GRID_SIZE - 1, 0) in neighbors