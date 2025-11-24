"""Integration tests for Schelling model."""

import random
from agent.agent import Agent
from environment.environment import Environment
from helper import (create_agents, randomly_place_agents, calculate_segregation_index,
                    calculate_happiness_rate, get_unhappy_agents)
from config import AGENT_TYPE_A, AGENT_TYPE_B


class TestSimulationRun:
    """Test full simulation runs."""

    def test_simulation_converges(self):
        """Test that simulation reaches equilibrium."""
        random.seed(42)
        env = Environment()
        agents = create_agents(50, 50, 0.3)
        randomly_place_agents(agents, env)

        # Run simulation
        for step in range(100):
            unhappy = get_unhappy_agents(agents, env)
            if len(unhappy) == 0:
                break

            empty_cells = env.get_empty_cells()
            if len(empty_cells) == 0:
                break

            # Shuffle unhappy agents (in place)
            random.shuffle(unhappy)

            # Move all unhappy agents
            for agent in unhappy:
                if len(empty_cells) == 0:
                    break

                # Pick random empty cell
                new_x, new_y = random.choice(empty_cells)

                # Remove from empty cells list
                empty_cells.remove((new_x, new_y))

                # Add old position to empty cells
                empty_cells.append((agent.x, agent.y))

                # Move agent
                env.move_agent(agent, new_x, new_y)

        # Should converge (all happy or no moves possible)
        final_unhappy = get_unhappy_agents(agents, env)
        assert len(final_unhappy) == 0 or len(env.get_empty_cells()) == 0

    def test_segregation_increases_over_time(self):
        """Test that segregation typically increases."""
        random.seed(42)
        env = Environment()
        agents = create_agents(100, 100, 0.3)
        randomly_place_agents(agents, env)

        initial_seg = calculate_segregation_index(agents, env)

        # Run 50 steps
        for _ in range(50):
            unhappy = get_unhappy_agents(agents, env)
            if len(unhappy) == 0:
                break

            empty_cells = env.get_empty_cells()
            if len(empty_cells) == 0:
                break

            agent = random.choice(unhappy)
            new_x, new_y = random.choice(empty_cells)
            env.move_agent(agent, new_x, new_y)

        final_seg = calculate_segregation_index(agents, env)

        # Segregation should increase
        assert final_seg > initial_seg


class TestHappinessDynamics:
    """Test happiness evolution."""

    def test_happiness_increases_over_time(self):
        """Test that happiness rate increases as agents move."""
        random.seed(42)
        env = Environment()
        agents = create_agents(80, 80, 0.3)
        randomly_place_agents(agents, env)

        initial_happiness = calculate_happiness_rate(agents, env)

        # Run 30 steps
        for _ in range(30):
            unhappy = get_unhappy_agents(agents, env)
            if len(unhappy) == 0:
                break

            empty_cells = env.get_empty_cells()
            if len(empty_cells) == 0:
                break

            agent = random.choice(unhappy)
            new_x, new_y = random.choice(empty_cells)
            env.move_agent(agent, new_x, new_y)

        final_happiness = calculate_happiness_rate(agents, env)

        # Happiness should increase
        assert final_happiness > initial_happiness


class TestScenarios:
    """Test specific scenarios."""

    def test_mild_preference_leads_to_segregation(self):
        """Test Schelling's key insight: mild preferences → high segregation."""
        random.seed(42)
        env = Environment()
        agents = create_agents(150, 150, 0.3)  # Only want 30% similar
        randomly_place_agents(agents, env)

        # Run to convergence
        for _ in range(200):
            unhappy = get_unhappy_agents(agents, env)
            if len(unhappy) == 0:
                break

            empty_cells = env.get_empty_cells()
            if len(empty_cells) == 0:
                break

            agent = random.choice(unhappy)
            new_x, new_y = random.choice(empty_cells)
            env.move_agent(agent, new_x, new_y)

        final_seg = calculate_segregation_index(agents, env)

        # Despite only wanting 30% similar, segregation should be much higher
        assert final_seg > 0.5

    def test_high_preference_leads_to_extreme_segregation(self):
        """Test that strong preferences lead to extreme segregation."""
        random.seed(42)
        env = Environment()
        agents = create_agents(100, 100, 0.7)  # Want 70% similar
        randomly_place_agents(agents, env)

        # Run to convergence
        for _ in range(200):
            unhappy = get_unhappy_agents(agents, env)
            if len(unhappy) == 0:
                break

            empty_cells = env.get_empty_cells()
            if len(empty_cells) == 0:
                break

            agent = random.choice(unhappy)
            new_x, new_y = random.choice(empty_cells)
            env.move_agent(agent, new_x, new_y)

        final_seg = calculate_segregation_index(agents, env)

        # Strong preferences should lead to very high segregation
        assert final_seg > 0.75