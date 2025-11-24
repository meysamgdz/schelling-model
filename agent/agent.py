"""
Agent module for Schelling segregation model.
Contains the Agent class representing individual residents.
"""

from config import AGENT_TYPE_A, AGENT_TYPE_B, NEIGHBORHOOD_RADIUS, GRID_SIZE


class Agent:
    """
    Represents an agent (resident) in the Schelling segregation model.

    Agents have a type (e.g., red or blue) and a preference for living near
    similar agents. They move if their neighborhood doesn't meet their
    similarity threshold.

    Attributes:
        x (int): The x-coordinate of the agent's position.
        y (int): The y-coordinate of the agent's position.
        agent_type (int): Type identifier (1 or 2).
        similarity_threshold (float): Minimum fraction of similar neighbors desired (0-1).
    """

    def __init__(self, x, y, agent_type, similarity_threshold=0.3):
        """
        Initialize an agent with position, type, and preferences.

        Args:
            x (int): Initial x-coordinate (0 to GRID_SIZE-1).
            y (int): Initial y-coordinate (0 to GRID_SIZE-1).
            agent_type (int): Agent type (AGENT_TYPE_A or AGENT_TYPE_B).
            similarity_threshold (float): Desired fraction of similar neighbors (0-1).
        """
        self.x = x
        self.y = y
        self.agent_type = agent_type
        self.similarity_threshold = similarity_threshold

    def is_happy(self, env):
        """
        Check if agent is satisfied with current neighborhood composition.

        An agent is happy if the fraction of similar neighbors meets or exceeds
        their similarity threshold. Empty cells are ignored in the calculation.

        Args:
            env (Environment): The environment containing the grid.

        Returns:
            bool: True if agent is happy, False otherwise.
        """
        neighbor_positions = self.get_neighbor_positions()

        similar_count = 0
        total_count = 0

        for nx, ny in neighbor_positions:
            neighbor_type = env.grid[nx, ny]

            # Skip empty cells
            if neighbor_type == 0:
                continue

            total_count += 1
            if neighbor_type == self.agent_type:
                similar_count += 1

        # If no neighbors, agent is unhappy (isolated)
        if total_count == 0:
            return False

        # Calculate similarity fraction
        similarity = similar_count / total_count

        return similarity >= self.similarity_threshold

    def get_neighbor_positions(self):
        """
        Get list of neighboring cell positions (Moore neighborhood).

        Returns positions of all cells within NEIGHBORHOOD_RADIUS, excluding
        the agent's own position. Grid wraps around (toroidal).

        Returns:
            list: List of (x, y) tuples for neighboring positions.
        """
        neighbors = []

        for dx in range(-NEIGHBORHOOD_RADIUS, NEIGHBORHOOD_RADIUS + 1):
            for dy in range(-NEIGHBORHOOD_RADIUS, NEIGHBORHOOD_RADIUS + 1):
                # Skip self
                if dx == 0 and dy == 0:
                    continue

                # Handle grid wrapping
                nx = (self.x + dx) % GRID_SIZE
                ny = (self.y + dy) % GRID_SIZE

                neighbors.append((nx, ny))

        return neighbors