"""
Schelling Segregation Model - Streamlit Application

Interactive visualization demonstrating how individual preferences for similar
neighbors lead to emergent residential segregation patterns.

Based on Thomas Schelling's segregation model (1971).
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.colors import ListedColormap

from agent.agent import Agent
from environment.environment import Environment
from helper import (create_agents, randomly_place_agents, calculate_segregation_index,
                    calculate_happiness_rate, get_unhappy_agents)
from config import (GRID_SIZE, AGENT_TYPE_A, AGENT_TYPE_B,
                    COLOR_EMPTY, COLOR_TYPE_A, COLOR_TYPE_B)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.running = False
    st.session_state.step = 0
    st.session_state.segregation_history = []
    st.session_state.happiness_history = []
    st.session_state.agents = []
    st.session_state.env = None


def initialize_simulation(num_type_a, num_type_b, similarity_threshold):
    """Initialize or reset the simulation."""
    st.session_state.env = Environment()

    # Create agents
    st.session_state.agents = create_agents(num_type_a, num_type_b, similarity_threshold)

    # Place agents randomly
    randomly_place_agents(st.session_state.agents, st.session_state.env)

    # Reset statistics
    st.session_state.step = 0
    st.session_state.segregation_history = []
    st.session_state.happiness_history = []
    st.session_state.initialized = True


def run_step():
    """Execute one simulation step."""
    if len(st.session_state.agents) == 0:
        return

    # Get unhappy agents
    unhappy = get_unhappy_agents(st.session_state.agents, st.session_state.env)

    # Move unhappy agents to random empty cells
    empty_cells = st.session_state.env.get_empty_cells()

    if len(empty_cells) > 0 and len(unhappy) > 0:
        # Shuffle unhappy agents
        random.shuffle(unhappy)

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
            st.session_state.env.move_agent(agent, new_x, new_y)

    # Update statistics
    segregation = calculate_segregation_index(st.session_state.agents, st.session_state.env)
    happiness = calculate_happiness_rate(st.session_state.agents, st.session_state.env)

    st.session_state.segregation_history.append(segregation)
    st.session_state.happiness_history.append(happiness)
    st.session_state.step += 1


# ============================================================================
# Streamlit UI
# ============================================================================

st.set_page_config(layout="wide", page_title="Schelling Segregation Model")
st.title("🏘️ Schelling Segregation Model")
st.markdown("How individual preferences lead to emergent segregation")

# Create tabs
tab1, tab2 = st.tabs(["Simulation", "Sensitivity Analysis"])


# Sidebar controls
with st.sidebar:
    st.header("⚙️ Model Parameters")

    st.subheader("Population")
    col1, col2 = st.columns(2)
    num_type_a = col1.slider("Number of Red Agents", 50, 1500, 1000, 50)
    num_type_b = col2.slider("Number of Blue Agents", 50, 1500, 1000, 50)

    st.subheader("Preferences")
    similarity_threshold = st.slider(
        "Similarity Threshold",
        0.0, 1.0, 0.3, 0.05,
        help="Minimum fraction of similar neighbors desired (e.g., 0.3 = want 30%+ similar)"
    )

    # Control buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎬 Start", use_container_width=True):
            if not st.session_state.initialized:
                initialize_simulation(num_type_a, num_type_b, similarity_threshold)
            st.session_state.running = True

    with col2:
        if st.button("⏸️ Pause", use_container_width=True):
            st.session_state.running = False

    with col3:
        if st.button("🔄 Reset", use_container_width=True):
            initialize_simulation(num_type_a, num_type_b, similarity_threshold)
            st.session_state.running = False

    steps_per_update = st.slider("Steps per Update", 1, 20, 1, 1)


# ============================================================================
# TAB 1: SIMULATION
# ============================================================================

with tab1:
    # Main content
    if not st.session_state.initialized:
        st.info("👈 Configure parameters and click **Start** to begin simulation")
    else:
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Step", st.session_state.step)

        with col2:
            occupancy = st.session_state.env.get_occupancy_rate()
            st.metric("Occupancy", f"{occupancy:.1%}")

        with col3:
            if len(st.session_state.segregation_history) > 0:
                seg = st.session_state.segregation_history[-1]
                st.metric("Segregation", f"{seg:.3f}")
            else:
                st.metric("Segregation", "N/A")

        with col4:
            if len(st.session_state.happiness_history) > 0:
                happy = st.session_state.happiness_history[-1]
                st.metric("Happy Agents", f"{happy:.1%}")
            else:
                st.metric("Happy Agents", "N/A")

        # Visualizations
        col1, col2 = st.columns(2)

        with col1:
            # Grid visualization
            fig1, ax1 = plt.subplots(figsize=(8, 8), dpi=100)

            # Create custom colormap
            cmap = ListedColormap([COLOR_EMPTY, COLOR_TYPE_A, COLOR_TYPE_B])

            # Plot grid
            ax1.imshow(st.session_state.env.grid.T, cmap=cmap, origin='lower',
                       interpolation='nearest', vmin=0, vmax=2)

            ax1.set_title("Residential Grid", fontsize=14, fontweight='bold')
            ax1.set_xlabel("X Position")
            ax1.set_ylabel("Y Position")
            ax1.grid(False)

            # Add legend
            from matplotlib.patches import Patch

            legend_elements = [
                Patch(facecolor=COLOR_TYPE_A, label='Red Agents'),
                Patch(facecolor=COLOR_TYPE_B, label='Blue Agents'),
                Patch(facecolor=COLOR_EMPTY, label='Empty')
            ]
            ax1.legend(handles=legend_elements, loc='upper right')

            st.pyplot(fig1)
            plt.close()

        with col2:
            # Metrics over time
            fig2, (ax2, ax3) = plt.subplots(2, 1, figsize=(8, 8), dpi=100)

            # Segregation over time
            if len(st.session_state.segregation_history) > 0:
                ax2.plot(st.session_state.segregation_history, color='#FF6B6B', linewidth=2)
                ax2.fill_between(range(len(st.session_state.segregation_history)),
                                 st.session_state.segregation_history, alpha=0.3, color='#FF6B6B')

            ax2.set_title("Segregation Index Over Time", fontsize=14, fontweight='bold')
            ax2.set_xlabel("Step")
            ax2.set_ylabel("Segregation Index")
            ax2.set_ylim([0, 1])
            ax2.grid(alpha=0.3)
            ax2.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='50% threshold')
            ax2.legend()

            # Happiness over time
            if len(st.session_state.happiness_history) > 0:
                ax3.plot(st.session_state.happiness_history, color='#4ECDC4', linewidth=2)
                ax3.fill_between(range(len(st.session_state.happiness_history)),
                                 st.session_state.happiness_history, alpha=0.3, color='#4ECDC4')

            ax3.set_title("Agent Happiness Over Time", fontsize=14, fontweight='bold')
            ax3.set_xlabel("Step")
            ax3.set_ylabel("Fraction Happy")
            ax3.set_ylim([0, 1])
            ax3.grid(alpha=0.3)

            plt.tight_layout()
            st.pyplot(fig2)
            plt.close()

    # Auto-run logic
    if st.session_state.running:
        for _ in range(steps_per_update):
            run_step()
        st.rerun()

    # Information panel
    with st.expander("ℹ️ About This Model"):
        st.markdown("""
        ### Schelling's Segregation Model
    
        This model demonstrates Thomas Schelling's famous insight: even mild preferences 
        for similar neighbors can lead to dramatic residential segregation.
    
        **Key Concepts:**
        - **Agents**: Residents of two types (red and blue)
        - **Preferences**: Each agent wants a minimum fraction of similar neighbors
        - **Happiness**: Agent is happy if their neighborhood meets their preference
        - **Movement**: Unhappy agents move to random empty locations
    
        **Segregation Index:**
        - Measures average similarity of each agent's neighborhood
        - 0 = perfectly integrated (50/50 mix everywhere)
        - 1 = perfectly segregated (only same-type neighbors)
    
        **Key Finding:**
        Even when agents only want 30% similar neighbors (quite tolerant!), 
        the system often evolves to 70%+ segregation.
    
        **Experiment Ideas:**
        - What happens at threshold = 0.5? (want 50% similar)
        - What if one group is much smaller? (try 100 vs 700 agents)
        - Can you prevent segregation with low thresholds? (try 0.2)
        """)

# ============================================================================
# TAB 2: SENSITIVITY ANALYSIS
# ============================================================================

with tab2:
    st.header("📊 Sensitivity Analysis")
    analysis_type = st.radio(
        "Select Analysis Type:",
        ["Tolerance Sensitivity", "Population Ratio Sensitivity"],
        horizontal=True
    )

    if analysis_type == "Tolerance Sensitivity":
        st.subheader("🎚️ Tolerance Sensitivity Analysis")
        st.markdown("How does segregation change as agents become more/less tolerant?")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("**Parameters:**")
            sa_pop_a = st.number_input("Red Agents", 50, 1500, 1000, 50)
            sa_pop_b = st.number_input("Blue Agents", 50, 1500, 1000, 50)
            sa_steps = st.slider("Steps per Run", 50, 500, 100, 50)

            if st.button("🚀 Run Analysis", use_container_width=True):
                with st.spinner("Running simulations..."):
                    thresholds = np.linspace(0.1, 0.9, 9)
                    segregation_results = []
                    happiness_results = []

                    progress_bar = st.progress(0)

                    for i, threshold in enumerate(thresholds):
                        # Run simulation
                        env = Environment()
                        agents = create_agents(sa_pop_a, sa_pop_b, threshold)
                        randomly_place_agents(agents, env)

                        # Run to convergence
                        for step in range(sa_steps):
                            unhappy = get_unhappy_agents(agents, env)
                            if len(unhappy) == 0:
                                break

                            empty_cells = env.get_empty_cells()
                            if len(empty_cells) == 0:
                                break

                            random.shuffle(unhappy)

                            for agent in unhappy:
                                if len(empty_cells) == 0:
                                    break
                                new_x, new_y = random.choice(empty_cells)
                                empty_cells.remove((new_x, new_y))
                                empty_cells.append((agent.x, agent.y))
                                env.move_agent(agent, new_x, new_y)

                        # Record results
                        seg = calculate_segregation_index(agents, env)
                        hap = calculate_happiness_rate(agents, env)
                        segregation_results.append(seg)
                        happiness_results.append(hap)

                        progress_bar.progress((i + 1) / len(thresholds))

                    # Store in session state
                    st.session_state.sa_thresholds = thresholds
                    st.session_state.sa_segregation = segregation_results
                    st.session_state.sa_happiness = happiness_results

                    st.success("✅ Analysis complete!")

        with col2:
            if 'sa_thresholds' in st.session_state:
                # Plot results
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

                # Segregation vs Threshold
                ax1.plot(st.session_state.sa_thresholds, st.session_state.sa_segregation,
                         'o-', color='#FF6B6B', linewidth=2, markersize=8)
                ax1.fill_between(st.session_state.sa_thresholds, st.session_state.sa_segregation,
                                 alpha=0.3, color='#FF6B6B')
                ax1.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
                ax1.set_xlabel("Similarity Threshold", fontsize=12)
                ax1.set_ylabel("Final Segregation Index", fontsize=12)
                ax1.set_title("Segregation vs Tolerance", fontsize=14, fontweight='bold')
                ax1.grid(alpha=0.3)
                ax1.set_ylim([0, 1])

                # Happiness vs Threshold
                ax2.plot(st.session_state.sa_thresholds, st.session_state.sa_happiness,
                         'o-', color='#4ECDC4', linewidth=2, markersize=8)
                ax2.fill_between(st.session_state.sa_thresholds, st.session_state.sa_happiness,
                                 alpha=0.3, color='#4ECDC4')
                ax2.set_xlabel("Similarity Threshold", fontsize=12)
                ax2.set_ylabel("Final Happiness Rate", fontsize=12)
                ax2.set_title("Happiness vs Tolerance", fontsize=14, fontweight='bold')
                ax2.grid(alpha=0.3)
                ax2.set_ylim([0, 1])

                plt.tight_layout()
                st.pyplot(fig)
                plt.close()

                # Key insights
                st.markdown("**💡 Key Insights:**")
                max_seg_idx = np.argmax(st.session_state.sa_segregation)
                st.markdown(
                    f"- **Highest segregation** ({st.session_state.sa_segregation[max_seg_idx]:.3f}) at threshold {st.session_state.sa_thresholds[max_seg_idx]:.2f}")
                st.markdown(
                    f"- **Lowest segregation** ({min(st.session_state.sa_segregation):.3f}) at threshold {st.session_state.sa_thresholds[np.argmin(st.session_state.sa_segregation)]:.2f}")
                st.markdown(
                    f"- Even mild preferences (0.3) lead to segregation ≈ {st.session_state.sa_segregation[2]:.3f}")

    else:  # Population Ratio Sensitivity
        st.subheader("👥 Population Ratio Sensitivity Analysis")
        st.markdown("How does the minority/majority ratio affect segregation?")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("**Parameters:**")
            sa_total_pop = st.number_input("Total Population", 100, 2000, 1000, 100)
            sa_threshold = st.slider("Similarity Threshold", 0.1, 0.9, 0.3, 0.1)
            sa_steps_ratio = st.number_input("Steps per Run", 50, 500, 200, 50, key='ratio_steps')

            if st.button("🚀 Run Ratio Analysis", use_container_width=True):
                with st.spinner("Running simulations..."):
                    # Test different ratios from 10% to 50% minority
                    minority_fractions = np.linspace(0.1, 0.5, 9)
                    segregation_results = []
                    happiness_results = []

                    progress_bar = st.progress(0)

                    for i, minority_frac in enumerate(minority_fractions):
                        num_minority = int(sa_total_pop * minority_frac)
                        num_majority = sa_total_pop - num_minority

                        # Run simulation
                        env = Environment()
                        agents = create_agents(num_minority, num_majority, sa_threshold)
                        randomly_place_agents(agents, env)

                        # Run to convergence
                        for step in range(sa_steps_ratio):
                            unhappy = get_unhappy_agents(agents, env)
                            if len(unhappy) == 0:
                                break

                            empty_cells = env.get_empty_cells()
                            if len(empty_cells) == 0:
                                break

                            random.shuffle(unhappy)

                            for agent in unhappy:
                                if len(empty_cells) == 0:
                                    break
                                new_x, new_y = random.choice(empty_cells)
                                empty_cells.remove((new_x, new_y))
                                empty_cells.append((agent.x, agent.y))
                                env.move_agent(agent, new_x, new_y)

                        # Record results
                        seg = calculate_segregation_index(agents, env)
                        hap = calculate_happiness_rate(agents, env)
                        segregation_results.append(seg)
                        happiness_results.append(hap)

                        progress_bar.progress((i + 1) / len(minority_fractions))

                    # Store in session state
                    st.session_state.ratio_fractions = minority_fractions
                    st.session_state.ratio_segregation = segregation_results
                    st.session_state.ratio_happiness = happiness_results

                    st.success("✅ Analysis complete!")

        with col2:
            if 'ratio_fractions' in st.session_state:
                # Plot results
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

                # Segregation vs Ratio
                ax1.plot(st.session_state.ratio_fractions * 100, st.session_state.ratio_segregation,
                         'o-', color='#FF6B6B', linewidth=2, markersize=8)
                ax1.fill_between(st.session_state.ratio_fractions * 100, st.session_state.ratio_segregation,
                                 alpha=0.3, color='#FF6B6B')
                ax1.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
                ax1.set_xlabel("Minority Population (%)", fontsize=12)
                ax1.set_ylabel("Final Segregation Index", fontsize=12)
                ax1.set_title("Segregation vs Population Ratio", fontsize=14, fontweight='bold')
                ax1.grid(alpha=0.3)
                ax1.set_ylim([0, 1])

                # Happiness vs Ratio
                ax2.plot(st.session_state.ratio_fractions * 100, st.session_state.ratio_happiness,
                         'o-', color='#4ECDC4', linewidth=2, markersize=8)
                ax2.fill_between(st.session_state.ratio_fractions * 100, st.session_state.ratio_happiness,
                                 alpha=0.3, color='#4ECDC4')
                ax2.set_xlabel("Minority Population (%)", fontsize=12)
                ax2.set_ylabel("Final Happiness Rate", fontsize=12)
                ax2.set_title("Happiness vs Population Ratio", fontsize=14, fontweight='bold')
                ax2.grid(alpha=0.3)
                ax2.set_ylim([0, 1])

                plt.tight_layout()
                st.pyplot(fig)
                plt.close()

                # Key insights
                st.markdown("**💡 Key Insights:**")
                max_seg_idx = np.argmax(st.session_state.ratio_segregation)
                st.markdown(
                    f"- **Highest segregation** ({st.session_state.ratio_segregation[max_seg_idx]:.3f}) at {st.session_state.ratio_fractions[max_seg_idx] * 100:.0f}% minority")
                st.markdown(
                    f"- **Lowest segregation** ({min(st.session_state.ratio_segregation):.3f}) at {st.session_state.ratio_fractions[np.argmin(st.session_state.ratio_segregation)] * 100:.0f}% minority")
                st.markdown(
                    f"- Balanced populations (50/50) show segregation ≈ {st.session_state.ratio_segregation[-1]:.3f}")
