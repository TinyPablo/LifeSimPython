from __future__ import annotations

from typing import TYPE_CHECKING

from lifesim.brain.neuron import Neuron
from lifesim.brain.neuron_type import NeuronType
from lifesim.utils.direction import Direction
from lifesim.utils.rng import rng

if TYPE_CHECKING:
    from lifesim.common.typing import (Entity, Grid, Simulation,
                                       SimulationSettings)

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
    return entity.simulation.cached_inputs['age']


def random_float(entity: Entity) -> float:
    return rng.random.random()


def get_blockage_forward(entity: Entity) -> float:
    grid: Grid | None = entity.grid
    assert grid is not None  # for mypy
    blockage_forward: bool = grid.blockage_in_direction(entity, entity.transform.direction)
    return 1.0 if blockage_forward else 0.0


def get_blockage_north(entity: Entity) -> float:
    grid: Grid | None = entity.grid
    assert grid is not None  # for mypy
    return 1.0 if grid.blockage_in_direction(entity, Direction.UP) else 0.0


def get_blockage_east(entity: Entity) -> float:
    grid: Grid | None = entity.grid
    assert grid is not None  # for mypy
    return 1.0 if grid.blockage_in_direction(entity, Direction.RIGHT) else 0.0


def get_blockage_south(entity: Entity) -> float:
    grid: Grid | None = entity.grid
    assert grid is not None  # for mypy
    return 1.0 if grid.blockage_in_direction(entity, Direction.DOWN) else 0.0


def get_blockage_west(entity: Entity) -> float:
    grid: Grid | None = entity.grid
    assert grid is not None  # for mypy
    return 1.0 if grid.blockage_in_direction(entity, Direction.LEFT) else 0.0


def oscilator_input(entity: Entity) -> float:
    return entity.simulation.cached_inputs['oscillator']


def meets_condition_input(entity: Entity) -> float:
    simulation: Simulation = entity.simulation
    if simulation.selection_condition(entity.transform.position_x, entity.transform.position_y):
        return 1.0
    return 0.0


def get_entities_alive(entity: Entity) -> float:
    simulation: Simulation = entity.simulation
    return len(simulation.entities) / simulation.settings.max_entity_count


# ======= OUTPUT NEURON FUNCTIONS =======

def move_north(entity: Entity) -> None:
    grid: Grid | None = entity.grid
    assert grid is not None  # for mypy
    grid.move(entity, Direction.UP)


def move_east(entity: Entity) -> None:
    grid: Grid | None = entity.grid
    assert grid is not None  # for mypy
    grid.move(entity, Direction.RIGHT)


def move_south(entity: Entity) -> None:
    grid: Grid | None = entity.grid
    assert grid is not None  # for mypy
    grid.move(entity, Direction.DOWN)


def move_west(entity: Entity) -> None:
    grid: Grid | None = entity.grid
    assert grid is not None  # for mypy
    grid.move(entity, Direction.LEFT)


def move_forward(entity: Entity) -> None:
    grid: Grid | None = entity.grid
    assert grid is not None  # for mypy
    grid.move_relative(entity, Direction.UP)


def reverse(entity: Entity) -> None:
    grid: Grid | None = entity.grid
    assert grid is not None  # for mypy
    grid.move_relative(entity, Direction.DOWN)


def move_right(entity: Entity) -> None:
    grid: Grid | None = entity.grid
    assert grid is not None  # for mypy
    grid.move_relative(entity, Direction.RIGHT)


def move_left(entity: Entity) -> None:
    grid: Grid | None = entity.grid
    assert grid is not None  # for mypy
    grid.move_relative(entity, Direction.LEFT)


def move_random(entity: Entity) -> None:
    grid: Grid | None = entity.grid
    assert grid is not None  # for mypy
    grid.move(entity, Direction.random())


def stay_still(entity: Entity) -> None:
    pass


def kys(entity: Entity) -> None:
    entity.die()


def kill(entity: Entity) -> None:
    x, y = entity.transform.next_x, entity.transform.next_y
    grid: Grid | None = entity.grid
    assert grid is not None  # for mypy
    if not grid.in_boundaries(x, y):
        return

    target_cell = grid.grid[x][y]
    target_entity = target_cell.object

    if isinstance(target_entity, Entity):
        target_entity.die()
        

input_neuron_definitions: list[Neuron] = [
    Neuron('I_location_vertically', NeuronType.INPUT, input_func=get_location_vertically),
    Neuron('I_location_horizontally', NeuronType.INPUT, input_func=get_location_horizontally),
    Neuron('I_distance_to_north_border', NeuronType.INPUT, input_func=get_distance_north),
    Neuron('I_distance_to_east_border', NeuronType.INPUT, input_func=get_distance_east),
    Neuron('I_distance_to_south_border', NeuronType.INPUT, input_func=get_distance_south),
    Neuron('I_distance_to_west_border', NeuronType.INPUT, input_func=get_distance_west),
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


output_neuron_definitions: list[Neuron] = [
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

def get_fresh_neurons(settings: SimulationSettings) -> list[Neuron]:
    internal_count = settings.max_internal_neurons
    internal_neurons = [Neuron(f'internal_{i+1}', NeuronType.INTERNAL) for i in range(internal_count)]

    neurons = (
        [Neuron(n.name, n.type, input_func=n.input_func, output_func=n.output_func)
         for n in input_neuron_definitions + output_neuron_definitions] +
        internal_neurons
    )
    return neurons