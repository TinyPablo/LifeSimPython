# 🧬 LifeSim — Evolution Simulator

> “You don’t tell life what to do — you just let it happen.”

**LifeSim** is an evolutionary life simulation where digital entities with simple neural “brains” evolve and adapt to survive in a dynamic environment.  
Inspired by [this YouTube video](https://www.youtube.com/watch?v=N3tRFayqVtk), it explores concepts like **artificial evolution**, **genome crossover**, and **emergent behavior** through agent-based simulation.

Each entity lives on a grid, controlled by a small neural network encoded in a digital genome.  
There are no predefined behaviors like `if x > 50: move_towards_food`.  
Instead, **creatures learn and evolve** through natural selection, reproduction, and mutation — forming unexpected, emergent patterns.

---

## 🌱 About the Project

This simulator started as a technical experiment — but quickly turned into a philosophical journey.

While watching small digital creatures evolve, I realized how powerful and unpredictable evolution is.  
It made me think differently about life itself:  
about emotions, body parts, shapes, and behaviors — all as products of survival through change.

Here, evolution isn’t programmed. It **discovers**.

---

## 🧠 How It Works (Conceptually)

1. **Entities** are small agents that live on a grid.  
   Each one has a *genome* — a list of encoded genes describing neural connections.

2. **Neural Networks (Brains)** are built dynamically from those genomes.  
   Neurons have types: `INPUT`, `INTERNAL`, and `OUTPUT`, connected according to the genetic code.

3. **Simulations** run for multiple generations:  
   - Entities move, sense obstacles, and sometimes survive if they meet the *selection condition*.  
   - The survivors reproduce — mixing and mutating their genomes to form the next generation.

4. **Emergent behavior** often appears — like all entities creating unexpected shapes, or synchronizing their movement through “evolved oscillations”.

---

## 🧩 Example: Evolved Behavior

In one run, after several generations, the population developed a collective behavior:  
most entities moved toward the **east border** of the map.  

Below are examples of their neural structures and movement patterns:

| Generation | Survival Rate (%) | Behavior Snapshot | Random Brain Visualization |
|-------------|------------------:|------------------|---------------------|
| 1  | 11.43 | <img src="https://github.com/user-attachments/assets/257fb15a-397d-4fc9-8b6b-dd0705fe76e6" width="260"/> | <img src="https://github.com/user-attachments/assets/3486d1f5-79f2-4070-8808-da411fde1526" width="260"/> |
| 5  | 54.30 | <img src="https://github.com/user-attachments/assets/f3371afa-08eb-4ec4-b863-06c7c785b66e" width="260"/> | <img src="https://github.com/user-attachments/assets/3d222e8e-8aaf-43dc-b78a-f60508dacd04" width="260"/> |
| 38 | 89.65 | <img src="https://github.com/user-attachments/assets/53dda159-f36d-4505-acb2-d2dc07e9d41d" width="260"/> | <img src="https://github.com/user-attachments/assets/de55529c-6ff4-41fb-9db7-6bcfb56aa633" width="260"/> |
| 208 | 96.97 | <img src="https://github.com/user-attachments/assets/095cab59-0c1d-47da-8a2e-154e5320fcb1" width="260"/> | <img src="https://github.com/user-attachments/assets/1a700fd5-5e12-493e-a064-5542c09a5532" width="260"/> |

---

## 🧬 Key Features

- **Dynamic neural evolution** — networks are not predefined; they emerge from genetic connections.  
- **Genome encoding** — each `Gene` encodes which neurons connect and with what weight.  
- **Selection-based survival** — only entities meeting a certain condition live to reproduce.  
- **Mutation & crossover** — parents’ genomes are combined and randomly mutated to create new offspring.  
- **Grid world** — all movement and interactions happen within a discrete spatial environment.  
- **Visualization tools (for debuging purposes)** —  
  - `brain_visualizer.py`: renders neural networks as `.svg` graphs  
  - `visualize_condition_on_grid.py`: shows selection zones
  - `preview_simulation_data.py`: plots diversity and survival across generations  

---

## 🧩 Tech Stack

- **Python 3.11+**
- **NumPy**, **Matplotlib**, **OpenCV**, **PIL**, **igraph**
- Multi-threaded simulation support (debug feature)
- JSON-based config storage and output logs

---

## 💭 Vision

This project isn’t about creating the smartest agent — it’s about observing **life-like complexity emerge from simplicity**.  
Every run is different.  
Sometimes they learn to cluster, sometimes to avoid edges, and sometimes — to do absolutely nothing.  
But that’s exactly the point.

---

## 🪴 Future Plans

- Add phenotypic visualization (colors, shape diversity)  
- Support more neurons (storage, vision, kindness)  
- Evolve cooperative behaviors  
- Interactive mode for watching evolution live  

---

## 🧑‍🔬 Author

**TinyPablo**

> “Evolution doesn’t need instructions — only iteration”
