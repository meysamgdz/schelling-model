"""Unit tests for Environment class."""

import pytest
from agent.agent import Agent
from environment.environment import Environment
from config import AGENT_TYPE_A, AGENT_TYPE_B, EMPTY_CELL, GRID_SIZE


class TestEnvironmentInitialization:
    """Test environment creation."""

    def test_environment_creation(self):
        env = Environment()
        assert env.grid.shape == (GRID_SIZE, GRID_SIZE)
        assert env.grid.sum() == 0  # All empty initially


class TestEmptyCells:
    """Test empty cell tracking."""

    def test_get_empty_cells_all_empty(self):
        env = Environment()
        empty = env.get_empty_cells()
        assert len(empty) == GRID_SIZE * GRID_SIZE

    def test_get_empty_cells_with_agents(self):
        env = Environment()
        env.grid[10, 10] = AGENT_TYPE_A
        env.grid[20, 20] = AGENT_TYPE_B

        empty = env.get_empty_cells()
        assert len(empty) == GRID_SIZE * GRID_SIZE - 2
        assert (10, 10) not in empty
        assert (20, 20) not in empty


class TestAgentPlacement:
    """Test agent placement."""

    def test_place_agent(self):
        env = Environment()
        agent = Agent(x=0, y=0, agent_type=AGENT_TYPE_A, similarity_threshold=0.3)

        env.place_agent(agent, 10, 10)

        assert env.grid[10, 10] == AGENT_TYPE_A
        assert agent.x == 10
        assert agent.y == 10

    def test_place_agent_on_occupied_cell_raises_error(self):
        env = Environment()
        agent1 = Agent(x=0, y=0, agent_type=AGENT_TYPE_A, similarity_threshold=0.3)
        agent2 = Agent(x=0, y=0, agent_type=AGENT_TYPE_B, similarity_threshold=0.3)

        env.place_agent(agent1, 10, 10)

        with pytest.raises(ValueError):
            env.place_agent(agent2, 10, 10)


class TestAgentMovement:
    """Test agent movement."""

    def test_remove_agent(self):
        env = Environment()
        agent = Agent(x=10, y=10, agent_type=AGENT_TYPE_A, similarity_threshold=0.3)
        env.place_agent(agent, 10, 10)

        env.remove_agent(agent)

        assert env.grid[10, 10] == EMPTY_CELL

    def test_move_agent(self):
        env = Environment()
        agent = Agent(x=0, y=0, agent_type=AGENT_TYPE_A, similarity_threshold=0.3)
        env.place_agent(agent, 10, 10)

        env.move_agent(agent, 20, 20)

        assert env.grid[10, 10] == EMPTY_CELL
        assert env.grid[20, 20] == AGENT_TYPE_A
        assert agent.x == 20
        assert agent.y == 20

    def test_move_to_occupied_cell_raises_error(self):
        env = Environment()
        agent1 = Agent(x=0, y=0, agent_type=AGENT_TYPE_A, similarity_threshold=0.3)
        agent2 = Agent(x=0, y=0, agent_type=AGENT_TYPE_B, similarity_threshold=0.3)

        env.place_agent(agent1, 10, 10)
        env.place_agent(agent2, 20, 20)

        with pytest.raises(ValueError):
            env.move_agent(agent1, 20, 20)


class TestNeighborCounting:
    """Test neighbor counting."""

    def test_count_neighbors_all_empty(self):
        env = Environment()
        counts = env.count_neighbors(25, 25)

        assert counts['type_a'] == 0
        assert counts['type_b'] == 0
        assert counts['empty'] == 8

    def test_count_neighbors_mixed(self):
        env = Environment()
        env.grid[24, 25] = AGENT_TYPE_A
        env.grid[26, 25] = AGENT_TYPE_A
        env.grid[25, 24] = AGENT_TYPE_B

        counts = env.count_neighbors(25, 25)

        assert counts['type_a'] == 2
        assert counts['type_b'] == 1
        assert counts['empty'] == 5


class TestOccupancy:
    """Test occupancy calculation."""

    def test_occupancy_empty(self):
        env = Environment()
        assert env.get_occupancy_rate() == 0.0

    def test_occupancy_full(self):
        env = Environment()
        env.grid[:, :] = AGENT_TYPE_A
        assert env.get_occupancy_rate() == 1.0

    def test_occupancy_half(self):
        env = Environment()
        half = GRID_SIZE * GRID_SIZE // 2
        env.grid.flat[:half] = AGENT_TYPE_A

        assert abs(env.get_occupancy_rate() - 0.5) < 0.01