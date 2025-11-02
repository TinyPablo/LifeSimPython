import matplotlib.pyplot as plt
import json
import os
from matplotlib.animation import FuncAnimation
import numpy as np

paths = [
    '/Users/pawel/Documents/Python/LifeSimPython/simulations/sim1 27-10-2025 18:51:14'
]


def load_data(path: str):
    with open(os.path.join(path, 'settings.json'), 'r') as f:
        simulation_settings: dict = json.load(f)

    with open(os.path.join(path, 'simulation_data.json'), 'r') as f:
        simulation_data: list[dict] = json.load(f)

    return simulation_settings, simulation_data


def smooth(data: list[float], window_size: int = 20) -> list[float]:
    if len(data) < window_size:
        return data
    kernel = np.ones(window_size) / window_size
    smoothed = np.convolve(data, kernel, mode='same')
    return smoothed.tolist()


def process_data(path: str):
    simulation_settings, simulation_data = load_data(path)

    generations = [d['generation'] for d in simulation_data]
    survival_rates = [d['survival_rate'] for d in simulation_data]

    return generations, survival_rates


def update(frame):
    global paths, axes, fig
    for ax in axes:
        ax.clear()

    all_data = []

    for i, path in enumerate(paths):
        generations, survival = process_data(path)
        smoothed = smooth(survival, window_size=8) 

        all_data.append((generations, survival, smoothed))
        ax = axes[i]
        ax.set_title(os.path.basename(path))

        ax.plot(
            generations, survival,
            color='tab:blue',
            alpha=0.3,
            linewidth=1.5,
            label='Raw'
        )

        ax.plot(
            generations, smoothed,
            color='tab:blue',
            alpha=0.9,
            linewidth=3,
            label='Smoothed'
        )

        ax.set_xlabel('Generation')
        ax.set_ylabel('Survival Rate (%)')
        ax.legend()
        ax.set_ylim(0, 100)

    ax_all = axes[-1]
    ax_all.set_title("All simulations combined")
    for i, (generations, survival, smoothed) in enumerate(all_data):
        ax_all.plot(generations, survival, color='tab:blue', alpha=0.3, linewidth=1.5)
        ax_all.plot(generations, smoothed, color='tab:blue', alpha=0.9, linewidth=3)

    ax_all.set_xlabel('Generation')
    ax_all.set_ylabel('Survival Rate (%)')
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