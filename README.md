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
