"""
Environment module for Schelling segregation model.
Contains the Environment class representing the grid world.
"""

import numpy as np
from config import GRID_SIZE, EMPTY_CELL, AGENT_TYPE_A, AGENT_TYPE_B


class Environment:
    """
    Represents the grid environment for the Schelling segregation model.

    The environment is a 2D grid where each cell can be empty or contain
    an agent of a specific type. Tracks agent positions and provides
    methods for agent movement.

    Attributes:
        grid (np.ndarray): 2D array representing the grid (GRID_SIZE x GRID_SIZE).
                          Values: 0=empty, 1=type A, 2=type B
    """

    def __init__(self):
        """Initialize an empty grid."""
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

    def get_empty_cells(self):
        """
        Get list of all empty cell coordinates.

        Returns:
            list: List of (x, y) tuples for empty cells.
        """
        empty_cells = []
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if self.grid[x, y] == EMPTY_CELL:
                    empty_cells.append((x, y))
        return empty_cells

    def place_agent(self, agent, x, y):
        """
        Place an agent at specified coordinates.

        Args:
            agent (Agent): The agent to place.
            x (int): X-coordinate.
            y (int): Y-coordinate.

        Raises:
            ValueError: If cell is already occupied.
        """
        if self.grid[x, y] != EMPTY_CELL:
            raise ValueError(f"Cell ({x}, {y}) is already occupied")

        self.grid[x, y] = agent.agent_type
        agent.x = x
        agent.y = y

    def remove_agent(self, agent):
        """
        Remove an agent from the grid.

        Args:
            agent (Agent): The agent to remove.
        """
        self.grid[agent.x, agent.y] = EMPTY_CELL

    def move_agent(self, agent, new_x, new_y):
        """
        Move an agent to a new location.

        Args:
            agent (Agent): The agent to move.
            new_x (int): New x-coordinate.
            new_y (int): New y-coordinate.

        Raises:
            ValueError: If destination cell is occupied.
        """
        if self.grid[new_x, new_y] != EMPTY_CELL:
            raise ValueError(f"Cannot move to occupied cell ({new_x}, {new_y})")

        # Remove from old position
        self.grid[agent.x, agent.y] = EMPTY_CELL

        # Place at new position
        self.grid[new_x, new_y] = agent.agent_type
        agent.x = new_x
        agent.y = new_y

    def count_neighbors(self, x, y, radius=1):
        """
        Count neighbors of each type around a position.

        Args:
            x (int): X-coordinate of center position.
            y (int): Y-coordinate of center position.
            radius (int): Neighborhood radius (default 1 = Moore neighborhood).

        Returns:
            dict: Dictionary with counts {'type_a': int, 'type_b': int, 'empty': int}
        """
        counts = {'type_a': 0, 'type_b': 0, 'empty': 0}

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                # Skip center
                if dx == 0 and dy == 0:
                    continue

                # Handle wrapping
                nx = (x + dx) % GRID_SIZE
                ny = (y + dy) % GRID_SIZE

                cell_value = self.grid[nx, ny]

                if cell_value == EMPTY_CELL:
                    counts['empty'] += 1
                elif cell_value == AGENT_TYPE_A:
                    counts['type_a'] += 1
                elif cell_value == AGENT_TYPE_B:
                    counts['type_b'] += 1

        return counts

    def get_occupancy_rate(self):
        """
        Calculate fraction of grid that is occupied.

        Returns:
            float: Occupancy rate (0-1).
        """
        occupied = np.sum(self.grid != EMPTY_CELL)
        total = GRID_SIZE * GRID_SIZE
        return occupied / total