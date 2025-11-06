import threading
import cProfile
import pstats

from lifesim.evolution.selection_conditions.enum import SelectionCondition
from lifesim.core.simulation import Simulation
from lifesim.utils.utils import timeit
from lifesim.visualization.render_toggle_ui import launch_render_ui


@timeit
def simulation_thread(simulation: Simulation, delay: int) -> None:
    print(f'\n--- starting simulation "{simulation.settings.name}" ---')
    simulation.start()


def main() -> None:
    simulation_configs = [
        {
            "grid_width": 80,
            "grid_height": 80,

            "steps_per_generation": 120,
            "max_generations": 1_000_000,
            "selection_condition": SelectionCondition.BOTTOM_RIGHT_SQUARE,

            "max_entity_count": 250,
            "brain_size": 10,
            "max_internal_neurons": 8,
            "fresh_minds": 10,

            "gene_mutation_probability": 1 / 10_000,

            "video_framerate": 40,
            "video_upscale_factor": 8,
        }
        for _ in range(1)
    ]

    simulations: list[Simulation] = []
    threads: list[threading.Thread] = []

    for i, config in enumerate(simulation_configs):
        sim = Simulation(config)
        simulations.append(sim)

        thread = threading.Thread(target=simulation_thread, args=(sim, i))
        threads.append(thread)

    for thread in threads:
        thread.start()

    launch_render_ui(simulations)


if __name__ == "__main__":
    measure = False
    if measure:
        profiler = cProfile.Profile()
        profiler.enable()

    main()

    if measure:
        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.sort_stats("cumtime").print_stats(60)