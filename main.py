import threading
import time
import cProfile
import pstats

from lifesim.evolution.selection_conditions.enum import SelectionCondition
from lifesim.core.simulation import Simulation
from lifesim.utils.utils import timeit


@timeit
def simulation_thread(simulation: Simulation, delay: int) -> None:
    time.sleep(delay)
    print(f'\n--- starting simulation "{simulation.settings.name}" ---')
    simulation.start()


def main() -> None:
    simulation_configs = [
        {
            "grid_width": 128,
            "grid_height": 128,

            "steps_per_generation": 196,
            "max_generations": 10,
            "selection_condition": SelectionCondition.ALMOST_P.value,

            "max_entity_count": 1280,
            "brain_size": 6,
            "max_internal_neurons": 2,
            "fresh_minds": 12,

            "gene_mutation_probability": 1 / 10_000,

            "video_framerate": 40,
            "video_upscale_factor": 8
        }
        for i in range(1)
    ]

    threads = []
    for i, config in enumerate(simulation_configs):
        sim = Simulation(config)
        thread = threading.Thread(target=simulation_thread, args=(sim, i))
        threads.append(thread)

    for t in threads:
        t.start()

    for t in threads:
        t.join()


if __name__ == '__main__':
    measure = False
    if measure:
        profiler = cProfile.Profile()
        profiler.enable()

    main()

    if measure:
        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumtime').print_stats(60)