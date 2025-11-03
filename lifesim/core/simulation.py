import copy
import json
import math
import threading
import time

import numpy as np

from lifesim.brain.genome import Genome
from lifesim.core.entity import Entity
from lifesim.core.grid import Grid
from lifesim.core.simulation_settings import SimulationSettings
from lifesim.utils.rng import rng
from lifesim.utils.utils import load_selection_condition_module


class Simulation:
    _id_counter_lock = threading.Lock()
    _id_counter = 1
    
    def __init__(self, settings: dict | None = None) -> None:
        with Simulation._id_counter_lock:
            self.id = Simulation._id_counter
            Simulation._id_counter += 1
            
        self.settings = SimulationSettings(self.id, settings)
        self.grid: Grid = Grid(self.settings.grid_width, self.settings.grid_height, self)
        self.current_generation: int = 0
        self.current_step: int = 0
        self.entities: list[Entity] = []
        self.simulation_ended: bool = False
        self.survival_rate: float = 0.0
        self.generation_data: dict[str, int | str] = {}
        self.generation_start_time: float = 0.0
        self.cached_inputs: dict[str, float] = {}
        self._selection_mask: np.ndarray | None = None
        
        selection_condition = getattr(self.settings, "selection_condition", None)
        if selection_condition is not None:
            try:
                mod = load_selection_condition_module(selection_condition.value)
            except Exception as e:
                raise RuntimeError(
                    f"Failed to load selection condition '{selection_condition.value}': {e}"
                )

            if not hasattr(mod, "condition") or not callable(mod.condition):
                raise RuntimeError(
                    f"Selection condition module '{selection_condition.value}' "
                    "does not define callable 'condition(x, y, w, h)'"
                )

            self._selection_condition_callable = mod.condition
        else:
            self._selection_condition_callable = None
            
        self.primary_survival_rate: float = self.get_primary_survival_rate()
    
    def get_primary_survival_rate(self):
        total_squares = self.settings.grid_width * self.settings.grid_height
        safe_squares = sum(
            1
            for x in range(self.settings.grid_width)
            for y in range(self.settings.grid_height)
            if self.selection_condition(x, y)
        )
        
        return safe_squares / total_squares * 100
    
    def start(self) -> None:
        self.populate()
        self.simulation_loop()
        
    def populate(self) -> None:
        self.entities = []
        for _ in range(self.settings.max_entity_count):
            genome: Genome = Genome(self.settings.brain_size)
            entity: Entity = Entity(genome, self)
            self.entities.append(entity)
        
        for entity in self.entities:
            self.grid.deploy_entity_randomly(entity)
            
    def simulation_loop(self) -> None:
        self.current_generation = 1
    
        while not self.simulation_ended and self.current_generation < (self.settings.max_generations + 1):
            if self.current_generation == 26:
                break
            self.generation_loop()
            self.current_generation += 1

        print('[LOG] simulation ended')

    def generation_loop(self) -> None:
        self.generation_start_time = time.perf_counter()
        self.current_step = 1

        for entity in self.entities:
            entity.brain.init()

        pictures: list = []
        while self.settings.steps_per_generation >= self.current_step and not self.simulation_ended:
            self.update_cached_inputs()
            
            for entity in self.entities:
                entity.brain.process()   

            
            pictures.append(self.grid.get_picture())
            self.current_step += 1

        self.on_generation_end(pictures)
                
    def on_generation_end(self, pictures: list[np.ndarray]) -> None:
        self.update_simulation_data()
        self.do_natural_selection()  

        elapsed = time.perf_counter() - self.generation_start_time
        self.log_generation_summary(elapsed) 

        self.reproduce()
        self.grid.save_video(pictures, self.current_generation, self.survival_rate)
        self.place_new_generation_entities()

    def update_simulation_data(self):
        self.generation_data["generation"] = self.current_generation
        self.generation_data['random_brains_3'] = [str(rng.random.choice([e.brain for e in self.entities])) for _ in range(3)]
        self.generation_data["survival_rate"] = self.survival_rate

        self.write_simulation_data(self.generation_data)
       
    def do_natural_selection(self) -> None:
        alive_entities = []
        for entity in self.entities:
            if self.selection_condition(entity.transform.position_x, entity.transform.position_y):
                alive_entities.append(entity)
            else:
                entity.die()
        self.entities = alive_entities
        self.update_survival_rate(len(self.entities))

    def log_generation_summary(self, elapsed_time: float, safe_entities_count: int | None = None) -> None:
        generation_num = self.current_generation
        if safe_entities_count is None:
            safe_entities_count = sum(
                1 for e in self.entities
                if self.selection_condition(e.transform.position_x, e.transform.position_y)
            )
        safe_entities_percent = safe_entities_count / self.settings.max_entity_count * 100
        generations_per_minute: float = 60 / elapsed_time

        log_message = (
            f"[LOG] Simulation: {self.settings.name}\n"
            f"[LOG] Generation: {generation_num}\n"
            f"[LOG] Safe Entities: {safe_entities_count}/{self.settings.max_entity_count} "
            f"SR {safe_entities_percent:.2f}% / PRS {self.primary_survival_rate:.2f}%\n"
            f"[LOG] Generations per minute: {generations_per_minute:.1f}\n"
            f"{'-'*50}\n"
        )

        print(log_message, flush=True)

    def reproduce(self) -> None:
        parents: list[Entity] = copy.copy(self.entities)
        used_parents: list[Entity] = []

        new_entities: list[Entity] = []

        if len(parents) < 2:
            print(f"[LOG] Population went extinct after {self.current_generation} generations")
            self.simulation_ended = True
            return      
        
        for _ in range(self.settings.fresh_minds):
            fresh_mind: Entity = Entity(Genome(self.settings.brain_size), self)
            new_entities.append(fresh_mind)
        
        while len(new_entities) < self.settings.max_entity_count:      

            if len(parents) < 2:
                parents += used_parents
                used_parents.clear()

            parent_a, parent_b = rng.random.sample(parents, 2)
            child_genome: Genome = Genome.crossover(parent_a.brain.genome, parent_b.brain.genome, self.settings.gene_mutation_probability)

            entity: Entity = Entity(child_genome, self)
            new_entities.append(entity)

            used_parents.append(parent_a)
            used_parents.append(parent_b)

            parents.remove(parent_a)
            parents.remove(parent_b)

        for e in self.entities:
            e.die()

        self.entities = new_entities

    def place_new_generation_entities(self) -> None:
        for entity in self.entities:
            self.grid.deploy_entity_randomly(entity)

    def write_simulation_data(self, generation_data: dict) -> None:
        simulation_data_path = f"{self.settings.simulation_directory}/simulation_data.json"
        all_data: list[dict] = self.load_simulation_data()

        with open(simulation_data_path, 'w') as f:
            all_data.append(generation_data)
            json.dump(all_data, f)
    
    def selection_condition(self, x: int, y: int) -> bool:
        if self._selection_mask is None:
            self.build_selection_mask()
        mask = self._selection_mask
        assert mask is not None  # for mypy
        return bool(mask[y, x])

    def update_survival_rate(self, alive_entities_count: int) -> None:
        self.survival_rate = alive_entities_count / self.settings.max_entity_count * 100

    def load_simulation_data(self) -> list:
        simulation_data_path = f"{self.settings.simulation_directory}/simulation_data.json"
        try:
            with open(simulation_data_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            with open(simulation_data_path, 'w+') as f:
                return []
        except json.JSONDecodeError:
            with open(simulation_data_path, 'w') as f:
                return []
            
    def update_cached_inputs(self):  # call once per step
        self.cached_inputs['age'] = self.current_step / self.settings.steps_per_generation
        self.cached_inputs['oscillator'] = 0.5 * (
            math.sin(2 * math.pi / self.settings.steps_per_generation * self.current_step) + 1
        )
        
    def build_selection_mask(self) -> None:
        w, h = self.settings.grid_width, self.settings.grid_height
        cond = self._selection_condition_callable
        
        self._selection_mask = np.fromfunction(
            np.vectorize(lambda y, x: bool(cond(int(x), int(y), w, h))),
            (h, w),
            dtype=int
        )