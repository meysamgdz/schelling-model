# 🏘️ Schelling Segregation Model

Interactive agent-based simulation demonstrating how individual preferences for similar neighbors lead to emergent residential segregation patterns.

Based on **Thomas Schelling's** classic segregation model (1971, Nobel Prize 2005).

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📖 Overview

The Schelling model reveals a counterintuitive insight: **even mild individual preferences can lead to dramatic collective segregation**. Agents want only 30% similar neighbors (quite tolerant!), yet neighborhoods often become 70%+ segregated.

### Key Features:
- ✅ Interactive visualization
- ✅ Real-time segregation tracking
- ✅ Adjustable preference thresholds
- ✅ Population controls
- ✅ Comprehensive metrics

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/schelling-model.git
cd schelling-model

# Install dependencies
pip install -r requirements.txt
```

### Run Simulation

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📁 Project Structure

```
schelling/
├── agent/
│   ├── __init__.py
│   └── agent.py          # Agent class (residents)
├── environment/
│   ├── __init__.py
│   └── environment.py    # Grid environment
├── tests/
│   ├── unit/
│   │   ├── test_agent.py
│   │   ├── test_environment.py
│   │   └── test_helper.py
│   └── integration/
│       └── test_integration.py
├── config.py             # Global constants
├── helper.py             # Utility functions & metrics
├── app.py                # Streamlit application
├── requirements.txt      # Dependencies
└── README.md            # This file
```

---

## How to Use

### 1. Configure Parameters

**Population:**
- Number of Red Agents (10-1000)
- Number of Blue Agents (10-1000)

**Preferences:**
- Similarity Threshold (0-1): Minimum fraction of similar neighbors desired

### 2. Run Simulation

- **Start**: Begin simulation
- **Pause**: Pause to examine current state
- **Reset**: Restart with new parameters

### 3. Observe Metrics

- **Segregation Index**: Average neighborhood similarity (0=integrated, 1=segregated)
- **Happiness Rate**: Fraction of satisfied agents
- **Occupancy**: Grid density

---

## 📊 Key Metrics

### Segregation Index

Measures average similarity in each agent's neighborhood:

```
SI = (1/N) × Σ (same-type neighbors / total neighbors)
```

**Interpretation:**
- 0.0-0.3: Low segregation (integrated)
- 0.3-0.6: Moderate segregation
- 0.6-1.0: High segregation

### Happiness Rate

Fraction of agents whose neighborhood meets their preference threshold:

```
Happiness = (# happy agents) / (# total agents)
```

---

## Example Experiments

### Experiment 1: Mild Preferences

**Setup:**
- 1000 Red, 1000 Blue agents
- Threshold = 0.3 (want 30%+ similar)

**Expected Result:**
- Segregation index rises to ~0.7
- Most neighborhoods 70%+ homogeneous
- Demonstrates Schelling's key insight!

### Experiment 2: Strong Preferences

**Setup:**
- 1000 Red, 1000 Blue agents
- Threshold = 0.6 (want 60%+ similar)

**Expected Result:**
- Segregation index approaches ~0.9
- Near-complete segregation emerges

### Experiment 3: Minority Population

**Setup:**
- 500 Red, 1500 Blue agents
- Threshold = 0.3

**Expected Result:**
- Red agents form small isolated clusters
- Blue agents spread more evenly

### Experiment 4: Can We Prevent Segregation?

**Setup:**
- 1000 Red, 1000 Blue agents
- Threshold = 0.15 (want only 20%+ similar)

**Expected Result:**
- Lower segregation (~0.5-0.6)
- But still substantial clustering!

---

## 🎓 Understanding the Model

### Agent Behavior

Each agent:
1. **Evaluates** current neighborhood
2. **Calculates** fraction of similar neighbors
3. **Compares** to their threshold
4. **Moves** if unhappy (to random empty cell)

### Neighborhood Definition

**Moore Neighborhood** (8 neighbors):
```
[ ][ ][ ]
[ ][A][ ]
[ ][ ][ ]
```

Empty cells are ignored in similarity calculation.

### Movement Rules

- **Unhappy agents** move first (random order)
- **Destination**: Random empty cell
- **One move per step** per agent

---

## 📈 Typical Dynamics

### Phase 1: Initial Mixing
- Random placement
- Many unhappy agents
- High movement rate

### Phase 2: Cluster Formation
- Agents find similar neighbors
- Segregation increases
- Movement slows

### Phase 3: Equilibrium 
- Stable clusters
- High happiness rate
- Minimal movement

---

## Mathematical Properties

### Convergence

The model **always converges** to a stable state where:
- All agents are happy, OR
- No empty cells remain

### Tipping Points

Critical thresholds where behavior changes dramatically:
- **< 0.3**: Low segregation possible
- **0.3-0.5**: Moderate segregation typical
- **> 0.5**: High segregation inevitable
- **> 0.75**: Agents always unhappy and move around

---


## Testing

Run tests:

```bash
# All tests
pytest tests/

# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# With coverage
pytest tests/ --cov
```

**Built for teaching and research in computational social science** 🏘️