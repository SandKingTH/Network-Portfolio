# WEEK 8 – Opportunistic Routing

**Teaching Intent**: Not all networks have stable paths. In opportunistic networks, nodes forward messages when a good opportunity appears — not when a fixed route exists. Nodes decide forwarding based on delivery probability rather than certainty.

## Overview

This lab introduces **opportunistic routing**. Nodes maintain delivery probabilities for peers and forward messages opportunistically when they encounter a node with a higher probability of delivering the message.

Instead of retrying blindly like store-and-forward, nodes **make probabilistic forwarding decisions**.

Probability becomes the routing table.

## Learning Outcomes

By completing this week, you will:
- ✅ Maintain delivery probability tables
- ✅ Forward packets opportunistically
- ✅ Store messages when delivery not possible
- ✅ Forward only to good candidates
- ✅ Train traits: probabilistic reasoning, adaptive decision-making, opportunistic networking

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Delivery Probability** | Likelihood a peer can deliver a message |
| **Opportunistic Forwarding** | Forward only when a good opportunity appears |
| **Encounter-Based Routing** | Nodes forward when they meet useful peers |
| **Message Queue** | Store messages until forwarding opportunity |
| **Forward Threshold** | Minimum probability required to forward |
| **Adaptive Routing** | Routing decisions change over time |

## Repository Structure

week08-opportunistic-routing-basic/
├── README.md
├── node.py
├── delivery_table.py
├── config.py
└── docs/
    └── run_instructions.md

## Quick Start

1. เปิดหลาย terminal แล้วรัน node.py พร้อมระบุ port และ peers เช่น

   python node.py 12000 12001 12002
   python node.py 12001 12000 12002
   python node.py 12002 12000 12001

2. พิมพ์ข้อความเพื่อส่ง message
