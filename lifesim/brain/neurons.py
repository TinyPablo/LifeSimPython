from copy import deepcopy
import math
import random
from typing import TYPE_CHECKING, List

from lifesim.utils.direction import Direction
from lifesim.core.entity import Entity
from lifesim.core.grid import Grid
from lifesim.brain.neuron import Neuron
from lifesim.brain.neuron_type import NeuronType
from lifesim.core.simulation import Simulation
from lifesim.core.simulation_settings import SimulationSettings


if TYPE_CHECKING:
    from lifesim.core.entity import Entity


# ======= INPUT NEURON FUNCTIONS =======

def get_location_vertically(entity: Entity) -> float:
    return 1 - (entity.transform.position_y / entity.simulation.settings.grid_height)


def get_location_horizontally(entity: Entity) -> float:
    return 1 - (entity.transform.position_x / entity.simulation.settings.grid_width)


def get_distance_north(entity: Entity) -> float:
    return 1 - (entity.transform.position_y / entity.simulation.settings.grid_height)


def get_distance_east(entity: Entity) -> float:
    return entity.transform.position_x / entity.simulation.settings.grid_width


def get_distance_south(entity: Entity) -> float:
    return entity.transform.position_y / entity.simulation.settings.grid_height


def get_distance_west(entity: Entity) -> float:
    return 1 - (entity.transform.position_x / entity.simulation.settings.grid_width)


def get_age(entity: Entity) -> float:
    simulation: Simulation = entity.simulation
    return simulation.current_step / simulation.settings.steps_per_generation


def random_float(entity: Entity) -> float:
    return random.random()


def get_blockage_forward(entity: Entity) -> float:
    grid: Grid = entity.grid
    blockage_forward: bool = grid.blockage_in_direction(entity, entity.transform.direction)
    return 1.0 if blockage_forward else 0.0


def get_blockage_north(entity: Entity) -> float:
    grid: Grid = entity.grid
    return 1.0 if grid.blockage_in_direction(entity, Direction.UP) else 0.0


def get_blockage_east(entity: Entity) -> float:
    grid: Grid = entity.grid
    return 1.0 if grid.blockage_in_direction(entity, Direction.RIGHT) else 0.0


def get_blockage_south(entity: Entity) -> float:
    grid: Grid = entity.grid
    return 1.0 if grid.blockage_in_direction(entity, Direction.DOWN) else 0.0


def get_blockage_west(entity: Entity) -> float:
    grid: Grid = entity.grid
    return 1.0 if grid.blockage_in_direction(entity, Direction.LEFT) else 0.0


def oscilator_input(entity: Entity) -> float:
    simulation: Simulation = entity.simulation
    return 0.5 * (math.sin((2 * math.pi * simulation.current_step) / simulation.settings.steps_per_generation) + 1)


def meets_condition_input(entity: Entity) -> float:
    simulation: Simulation = entity.simulation
    if simulation.selection_condition(entity.transform.position_x, entity.transform.position_y):
        return 1.0
    return 0.0


def get_entities_alive(entity: Entity) -> float:
    simulation: Simulation = entity.simulation
    return len(simulation.entities) / simulation.settings.max_entity_count


# ======= OUTPUT NEURON FUNCTIONS =======

def move_north(entity: Entity) -> float:
    grid: Grid = entity.grid
    grid.move(entity, Direction.UP)


def move_east(entity: Entity) -> float:
    grid: Grid = entity.grid
    grid.move(entity, Direction.RIGHT)


def move_south(entity: Entity) -> float:
    grid: Grid = entity.grid
    grid.move(entity, Direction.DOWN)


def move_west(entity: Entity) -> float:
    grid: Grid = entity.grid
    grid.move(entity, Direction.LEFT)


def move_forward(entity: Entity) -> float:
    grid: Grid = entity.grid
    grid.move_relative(entity, Direction.UP)


def reverse(entity: Entity) -> float:
    grid: Grid = entity.grid
    grid.move_relative(entity, Direction.DOWN)


def move_right(entity: Entity) -> float:
    grid: Grid = entity.grid
    grid.move_relative(entity, Direction.RIGHT)


def move_left(entity: Entity) -> float:
    grid: Grid = entity.grid
    grid.move_relative(entity, Direction.LEFT)


def move_random(entity: Entity) -> float:
    grid: Grid = entity.grid
    grid.move(entity, Direction.random())


def stay_still(entity: Entity) -> float:
    pass


def kys(entity: Entity) -> float:
    entity.die()


def kill(entity: Entity) -> float:
    grid: Grid = entity.grid
    x: int = entity.transform.next_x
    y: int = entity.transform.next_y

    if grid.in_boundaries(x, y):
        target = grid.grid[x][y]
        if isinstance(target, Entity):
            target.object.die()


input_neuron_definitions: List[Neuron] = [
    Neuron('I_location_vertically', NeuronType.INPUT, input_func=get_location_vertically),
    Neuron('I_location_horizontally', NeuronType.INPUT, input_func=get_location_horizontally),
    Neuron('I_distance_to_north_border', NeuronType.INPUT, input_func=get_distance_north),
    Neuron('I_distance_to_east_border', NeuronType.INPUT, input_func=get_distance_east),
    Neuron('I_distance_to_south_border', NeuronType.INPUT, input_func=get_distance_south),
    Neuron('I_distance_to_west_border', NeuronType.INPUT, input_func=get_blockage_west),
    Neuron('I_age', NeuronType.INPUT, input_func=get_age),
    Neuron('I_random_float', NeuronType.INPUT, input_func=random_float),
    Neuron('I_blockage_forward', NeuronType.INPUT, input_func=get_blockage_forward),
    Neuron('I_oscilator_input', NeuronType.INPUT, input_func=oscilator_input),
    Neuron('I_blockage_north', NeuronType.INPUT, input_func=get_blockage_north),
    Neuron('I_blockage_east', NeuronType.INPUT, input_func=get_blockage_east),
    Neuron('I_blockage_south', NeuronType.INPUT, input_func=get_blockage_south),
    Neuron('I_blockage_west', NeuronType.INPUT, input_func=get_blockage_west),
    Neuron('entities_alive', NeuronType.INPUT, input_func=get_entities_alive),
    # Neuron('meets_condition_input', NeuronType.INPUT, input_func=meets_condition_input)
]


output_neuron_definitions: List[Neuron] = [
    Neuron('O_move_forward', NeuronType.OUTPUT, output_func=move_forward),
    Neuron('O_reverse', NeuronType.OUTPUT, output_func=reverse),
    Neuron('O_move_random', NeuronType.OUTPUT, output_func=move_random),
    Neuron('O_stay_still', NeuronType.OUTPUT, output_func=stay_still),
    Neuron('O_move_north', NeuronType.OUTPUT, output_func=move_north),
    Neuron('O_move_east', NeuronType.OUTPUT, output_func=move_east),
    Neuron('O_move_south', NeuronType.OUTPUT, output_func=move_south),
    Neuron('O_move_west', NeuronType.OUTPUT, output_func=move_west),
    # Neuron('kys', NeuronType.OUTPUT, output_func=kys),
    # Neuron('kill', NeuronType.OUTPUT, output_func=kill),
]


def get_fresh_neurons(settings: SimulationSettings) -> List[Neuron]:
    internal_neuron_definitions: List[Neuron] = [
        Neuron(f'internal_{i+1}', NeuronType.INTERNAL)
        for i in range(settings.max_internal_neurons)
        ]
    neuron_definitions: List[Neuron] = [
        *input_neuron_definitions,
        *output_neuron_definitions,
        *internal_neuron_definitions
        ]
    return deepcopy(neuron_definitions)