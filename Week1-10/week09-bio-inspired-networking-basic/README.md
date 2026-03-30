# WEEK 9 – Bio-Inspired Networking

**Teaching Intent**: This lab simulates routing inspired by ant colonies. Nodes reinforce successful paths using pheromones and gradually forget unused paths through decay. Over time, the network learns the best routes automatically.

## Overview

This lab introduces **bio-inspired routing** using pheromone tables.  
Each node reinforces successful paths and decays old paths over time.  
Routing decisions become adaptive and self-optimizing.

The network learns which paths are best.

## Learning Outcomes

By completing this week, you will:
- Implement pheromone-based routing tables
- Reinforce successful routing paths
- Apply pheromone decay over time
- Simulate adaptive routing behavior
- Understand bio-inspired networking algorithms

## Key Concepts

| Concept | Description |
|--------|-------------|
| Pheromone Table | Stores path strength |
| Reinforcement | Increase pheromone when delivery succeeds |
| Decay | Reduce pheromone over time |
| Adaptive Routing | Network learns best path |
| Probabilistic Forwarding | Forward using pheromone strength |

## Repository Structure
week09-bio-inspired-networking-basic/
├── README.md
├── node.py
├── pheromone_table.py
├── config.py
└── docs/
    └── run_instructions.md

## Quick Start

Open 3 terminals and run:

Terminal 1:

python node.py 13000 13001 13002

Terminal 2:

python node.py 13001 13000 13002

Terminal 3:

python node.py 13002 13000 13001
