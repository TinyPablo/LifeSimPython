from simulation import Simulation
from utils import timeit
import threading


@timeit
def simulation_thread(simulation: Simulation) -> None:
    print(f'\n--- starting simulation "{simulation.settings.name}" ---')
    simulation.start()


def main() -> None:
    simulation_configs = [
    {
        "name": f"sim{seed+1}",
        "seed": seed,
        "grid_width": 128,
        "grid_height": 128,
        "steps_per_generation": 200,
        "max_entity_count": 1024,
        "brain_size": 4,
        "max_internal_neurons": 1,
        "fresh_minds": 10,
        "gene_mutation_probability": 1/10000
    }
    for seed in range(1)
]

    threads = []
    for config in simulation_configs:
        sim = Simulation(config)
        thread: threading.Thread = threading.Thread(target=simulation_thread, args=(sim,))
        threads.append(thread)
        
    for t in threads:
        t.start()


if __name__ == '__main__':
    main()