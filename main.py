from simulation import Simulation
from utils import timeit
import threading

@timeit
def simulation_thread(simulation: Simulation) -> None:
    print(f'\n--- starting simulation "{simulation.settings.name}" ---')
    simulation.start()

@timeit
def main() -> None:
    simulation_configs = [
        {
            "name": "sim_1",
            "seed": 0,
            "brain_size": 1,
            "max_entity_count": 500,
            "max_generations": 5
        },
        {
            "name": "sim_2",
            "seed": 1,
            "max_entity_count": 400,
            "brain_size": 2,
            "max_generations": 7
        },
        {
            "name": "sim_3",
            "seed": 2,
            "max_entity_count": 300,
            "brain_size": 3,
            "max_generations": 8
        }
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