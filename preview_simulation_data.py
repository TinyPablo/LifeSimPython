from typing import Dict, List
import matplotlib.pyplot as plt
import math
import json
from matplotlib.animation import FuncAnimation
import os


paths = [
    '/Users/pawel/Documents/Python/LifeSimPython/simulations/sim0 26-10-2025 03:36:23'
]


def load_data(path: str):
    with open(os.path.join(path, 'settings.json'), 'r') as f:
        simulation_settings: Dict = json.load(f)

    with open(os.path.join(path, 'simulation_data.json'), 'r') as f:
        simulation_data: List[Dict] = json.load(f)

    return simulation_settings, simulation_data

def calculate_shannon_index(gene_occurrences: Dict[str, int]) -> float:
    total_occurrences = sum(gene_occurrences.values())
    if total_occurrences == 0:
        return 0
    return -sum(
        (count / total_occurrences) * math.log(count / total_occurrences)
        for count in gene_occurrences.values() if count > 0
    )

def process_data(path: str):
    simulation_settings, simulation_data = load_data(path)
    
    generations = [d['generation'] for d in simulation_data]
    survival_rates = [d['survival_rate'] for d in simulation_data]
    gene_occurrences_per_generation = [d['genome_diversity'] for d in simulation_data]

    shannon_indices = [calculate_shannon_index(g) for g in gene_occurrences_per_generation]
    
    if len(shannon_indices) == 0:
        return [], [], [], 0, 0

    max_shannon = max(shannon_indices)
    min_shannon = min(shannon_indices)
    normalized_diversity = [
        (H - min_shannon) / (max_shannon - min_shannon) * 100 if max_shannon != min_shannon else 0
        for H in shannon_indices
    ]
    return generations, survival_rates, normalized_diversity, min_shannon, max_shannon

def update(frame):
    global paths, axes
    for ax in axes:
        ax.clear()

    all_data = []

    for i, path in enumerate(paths):
        generations, survival, diversity, _, _ = process_data(path)
        all_data.append((generations, survival, diversity))
        ax = axes[i]
        ax.set_title(os.path.basename(path))
        ax.plot(generations, survival, color='tab:blue', label='Survival Rate')
        ax.plot(generations, diversity, color='tab:green', label='Diversity')
        ax.set_xlabel('Generation')
        ax.set_ylim(0, 100)

    ax_all = axes[-1]
    ax_all.set_title("All simulations combined")
    for i, (generations, survival, diversity) in enumerate(all_data):
        ax_all.plot(generations, survival, label=f'Surv {i}', alpha=0.7)
        ax_all.plot(generations, diversity, label=f'Div {i}', linestyle='--', alpha=0.7)
    ax_all.set_xlabel('Generation')
    ax_all.set_ylim(0, 100)

    fig.tight_layout()

while True:
    try:
        cols = len(paths) + 1
        fig, axes = plt.subplots(1, cols, figsize=(5 * cols, 5))

        ani = FuncAnimation(fig, update, interval=1000)
        plt.show()
    except Exception as e:
        print(f'e: ({e})')