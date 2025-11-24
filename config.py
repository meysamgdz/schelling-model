"""
Configuration file for Schelling segregation model.
Contains global constants used across modules.
"""

# Grid dimensions
GRID_SIZE = 50

# Agent types
AGENT_TYPE_A = 1  # Red agents
AGENT_TYPE_B = 2  # Blue agents
EMPTY_CELL = 0

# Neighborhood
NEIGHBORHOOD_RADIUS = 1  # Moore neighborhood (8 neighbors)

# Similarity preferences
DEFAULT_SIMILARITY_THRESHOLD = 0.3  # Want 30%+ similar neighbors

# Visualization colors
COLOR_EMPTY = '#FFFFFF'     # White
COLOR_TYPE_A = '#FF6B6B'    # Red
COLOR_TYPE_B = '#4ECDC4'    # Blue
COLOR_UNHAPPY = '#FFD93D'   # Yellow (for highlighting)