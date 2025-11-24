"""
Helper functions for Schelling segregation model.
Contains utility functions for metrics and agent creation.
"""

import random
import numpy as np
from agent.agent import Agent
from config import GRID_SIZE, AGENT_TYPE_A, AGENT_TYPE_B


def create_agents(num_agents_type_a, num_agents_type_b, similarity_threshold=0.3):
    """
    Create agents of two types with specified preferences.

    Args:
        num_agents_type_a (int): Number of type A agents.
        num_agents_type_b (int): Number of type B agents.
        similarity_threshold (float): Desired similarity fraction (0-1).

    Returns:
        list: List of Agent objects (not yet placed on grid).
    """
    agents = []

    # Create type A agents
    for _ in range(num_agents_type_a):
        agent = Agent(x=0, y=0, agent_type=AGENT_TYPE_A,
                     similarity_threshold=similarity_threshold)
        agents.append(agent)

    # Create type B agents
    for _ in range(num_agents_type_b):
        agent = Agent(x=0, y=0, agent_type=AGENT_TYPE_B,
                     similarity_threshold=similarity_threshold)
        agents.append(agent)

    return agents


def randomly_place_agents(agents, env):
    """
    Randomly place agents on empty cells in the environment.

    Args:
        agents (list): List of Agent objects to place.
        env (Environment): Environment with grid.

    Raises:
        ValueError: If not enough empty cells for all agents.
    """
    empty_cells = env.get_empty_cells()

    if len(agents) > len(empty_cells):
        raise ValueError(f"Not enough empty cells ({len(empty_cells)}) for {len(agents)} agents")

    # Shuffle for random placement
    random.shuffle(empty_cells)

    for i, agent in enumerate(agents):
        x, y = empty_cells[i]
        env.place_agent(agent, x, y)


def calculate_segregation_index(agents, env):
    """
    Calculate segregation index (average similarity experienced by agents).

    Segregation index ranges from 0 (perfectly integrated) to 1 (perfectly segregated).
    It measures the average fraction of same-type neighbors each agent has.

    Args:
        agents (list): List of Agent objects.
        env (Environment): Environment with grid.

    Returns:
        float: Segregation index (0-1). Returns 0 if no agents.
    """
    if len(agents) == 0:
        return 0.0

    total_similarity = 0.0
    valid_agents = 0

    for agent in agents:
        neighbor_positions = agent.get_neighbor_positions()

        similar_count = 0
        total_count = 0

        for nx, ny in neighbor_positions:
            neighbor_type = env.grid[nx, ny]

            # Skip empty cells
            if neighbor_type == 0:
                continue

            total_count += 1
            if neighbor_type == agent.agent_type:
                similar_count += 1

        # Only count agents with neighbors
        if total_count > 0:
            similarity = similar_count / total_count
            total_similarity += similarity
            valid_agents += 1

    if valid_agents == 0:
        return 0.0

    return total_similarity / valid_agents


def calculate_happiness_rate(agents, env):
    """
    Calculate fraction of agents that are happy.

    Args:
        agents (list): List of Agent objects.
        env (Environment): Environment with grid.

    Returns:
        float: Happiness rate (0-1). Returns 0 if no agents.
    """
    if len(agents) == 0:
        return 0.0

    happy_count = sum(1 for agent in agents if agent.is_happy(env))
    return happy_count / len(agents)


def get_unhappy_agents(agents, env):
    """
    Get list of agents that are currently unhappy.

    Args:
        agents (list): List of Agent objects.
        env (Environment): Environment with grid.

    Returns:
        list: List of unhappy Agent objects.
    """
    return [agent for agent in agents if not agent.is_happy(env)]


def get_agent_counts_by_type(agents):
    """
    Count agents by type.

    Args:
        agents (list): List of Agent objects.

    Returns:
        dict: Dictionary with counts {'type_a': int, 'type_b': int}
    """
    type_a_count = sum(1 for agent in agents if agent.agent_type == AGENT_TYPE_A)
    type_b_count = sum(1 for agent in agents if agent.agent_type == AGENT_TYPE_B)

    return {'type_a': type_a_count, 'type_b': type_b_count}