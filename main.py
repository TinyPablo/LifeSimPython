import threading
import time

from selection_conditions.enum import SelectionCondition
from simulation import Simulation
from utils import timeit


@timeit
def simulation_thread(simulation: Simulation, delay: str) -> None:
    time.sleep(delay)
    print(f'\n--- starting simulation "{simulation.settings.name}" ---')
    simulation.start()


def main() -> None:
    simulation_configs = [
        {
            "name": f"sim{seed+1}",

            "random_seed": False,
            "seed": seed + 1,

            "grid_width": 80,
            "grid_height": 80,

            "steps_per_generation": 256,
            "max_generations": 10_000_000,
            "selection_condition": SelectionCondition.CORNERS.value,

            "max_entity_count": 1000,
            "brain_size": 1,
            "max_internal_neurons": 0,
            "fresh_minds": 1,

            "gene_mutation_probability": 1 / 10_000,

            "video_framerate": 60,
            "video_upscale_factor": 8
            }
        for seed in range(1)
        ]


    threads = []
    for i, config in enumerate(simulation_configs):
        sim = Simulation(config)
        thread: threading.Thread = threading.Thread(target=simulation_thread, args=(sim, i))
        threads.append(thread)

    for t in threads:
        t.start()


if __name__ == '__main__':
    main()