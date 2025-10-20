from typing import Dict, List
import matplotlib.pyplot as plt
import math
from matplotlib.ticker import MaxNLocator
import json
from matplotlib.animation import FuncAnimation

path = '/Users/pawel/Documents/Python/simulations/brain_generator_att4/simulations/0 17-10-2025 18:50:30'

def load_data():
    with open(f'{path}/settings.json', 'r') as f:
        simulation_settings: List[Dict] = json.load(f)

    with open(f'{path}/simulation_data.json', 'r') as f:
        simulation_data: List[Dict] = json.load(f)

    return simulation_settings, simulation_data

def calculate_shannon_index(gene_occurrences):
    total_occurrences = sum(gene_occurrences.values())
    if total_occurrences == 0:
        return 0
    shannon_index = -sum(
        (count / total_occurrences) * math.log(count / total_occurrences)
        for count in gene_occurrences.values() if count > 0
    )
    return shannon_index

def update(frame):
    simulation_settings, simulation_data = load_data()
    
    max_entity_count: int = simulation_settings['max_entity_count']
    generations = [data['generation'] for data in simulation_data]
    survival_rates = [data['survival_rate'] for data in simulation_data]
    gene_occurrences_per_generation = [data['genome_diversity'] for data in simulation_data]
    
    shannon_indices = [calculate_shannon_index(genes) for genes in gene_occurrences_per_generation]
    
    max_shannon = max(shannon_indices)
    min_shannon = min(shannon_indices)
    normalized_diversity = [(H - min_shannon) / (max_shannon - min_shannon) * 100 if max_shannon != min_shannon else 0 for H in shannon_indices]
    
    ax1.clear()
    ax2.clear()
    
    ax1.set_xlabel('Generations')
    ax1.set_ylabel('Survival Rate', color='tab:blue')
    ax1.plot(generations, survival_rates, color='tab:blue', label='Survival Rate')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.set_ylim(0, 100)
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
    
    ax2.set_ylabel('Gene Diversity', color='tab:green')
    ax2.plot(generations, normalized_diversity, color='tab:green', label='Gene Diversity')
    ax2.tick_params(axis='y', labelcolor='tab:green')
    ax2.set_ylim(0, 100)
    
    fig.tight_layout()
    plt.title('Survival Rate and Gene Diversity Across Generations')

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ani = FuncAnimation(fig, update, interval=1000)
plt.show()
