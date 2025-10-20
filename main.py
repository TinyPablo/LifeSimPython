from simulation import Simulation 
from utils import timeit


@timeit
def main() -> None:
    simulation = Simulation()
    simulation.start() 


if __name__ == '__main__':  
    input('press enter to start the simulation')
    main()