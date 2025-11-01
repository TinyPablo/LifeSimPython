import copy
import json
import random
import time
from typing import Dict, List

from lifesim.brain.genome import Genome
from lifesim.core.grid import Grid
from lifesim.core.entity import Entity
from lifesim.core.simulation_settings import SimulationSettings
from lifesim.utils.utils import load_selection_condition_module


class Simulation:
    def __init__(self, settings: dict = None) -> None:
        self.settings = SimulationSettings(settings)
        self.grid: 'Grid' = Grid(self.settings.grid_width, self.settings.grid_height, self)
        self.current_generation: int = 0
        self.current_step: int = 0
        self.entities: List[Entity] = []
        self.simulation_ended: bool = False
        self.survival_rate: float = 0.0
        self.generation_data: Dict[str, int | str] = {}
        self.generation_start_time: float = 0.0
        self.timer_start = None
        
        if getattr(self.settings, "selection_condition", None):
            try:
                mod = load_selection_condition_module(self.settings.selection_condition.value)
            except Exception as e:
                raise RuntimeError(f"Failed to load selection condition '{self.settings.selection_condition.value}': {e}")

            if not hasattr(mod, "condition") or not callable(mod.condition):
                raise RuntimeError(
                    f"Selection condition module '{self.settings.selection_condition.value}' "
                    "does not define callable 'condition(x, y, w, h)'"
                )
        
        self._selection_condition_callable = mod.condition
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
        self.timer_start = time.perf_counter()
        self.populate()
        self.simulation_loop()
        
    def populate(self) -> None:
        self.entities: List[Entity] = []
        for _ in range(self.settings.max_entity_count):
            genome: Genome = Genome(self.settings.brain_size)
            entity: Entity = Entity(genome, self)
            self.entities.append(entity)
        
        for entity in self.entities:
            self.grid.deploy_entity_randomly(entity)
            
    def simulation_loop(self) -> None:
        self.current_generation = 1
    
        while not self.simulation_ended and self.current_generation < (self.settings.max_generations + 1):
            self.generation_loop()
            self.current_generation += 1

        print(f'simulation ended | SEED: {self.settings.seed}')

    def generation_loop(self) -> None:
        self.generation_start_time = time.perf_counter()
        self.current_step = 1

        for entity in self.entities:
            entity.brain.init()

        pictures: List[List[List[tuple[int, int, int]]]] = []
        while self.settings.steps_per_generation >= self.current_step and not self.simulation_ended:
            for entity in self.entities:
                entity.brain.process()   

            
            pictures.append(self.grid.get_picture())
            self.current_step += 1

        self.on_generation_end(pictures)
        if self.current_generation == 10:
            print(time.perf_counter() - self.timer_start)
                
    def on_generation_end(self, pictures: List[List[tuple[int, int, int]]]) -> None:
        self.update_simulation_data()
        self.do_natural_selection()  

        elapsed = time.perf_counter() - self.generation_start_time
        self.log_generation_summary(elapsed) 

        self.reproduce()
        self.grid.save_video(pictures, self.current_generation, self.survival_rate)
        self.place_new_generation_entities()

    def update_simulation_data(self):
        self.generation_data["generation"] = self.current_generation
        self.generation_data['random_brains_3'] = [str(random.choice([e.brain for e in self.entities])) for _ in range(3)]
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

    def log_generation_summary(self, elapsed_time: float, safe_entities_count: int = None) -> None:
        generation_num = self.current_generation
        if safe_entities_count is None:
            safe_entities_count = sum(
                1 for e in self.entities
                if self.selection_condition(e.transform.position_x, e.transform.position_y)
            )
        safe_entities_percent = safe_entities_count / self.settings.max_entity_count * 100

        log_message = (
            f"[LOG] Simulation: {self.settings.name}\n"
            f"[LOG] Generation: {generation_num}\n"
            f"[LOG] Safe Entities: {safe_entities_count}/{self.settings.max_entity_count} "
            f"SR {safe_entities_percent:.2f}% / PRS {self.primary_survival_rate:.2f}%\n"
            f"[LOG] Generation Duration: {elapsed_time:.3f} seconds\n"
            f"{'-'*50}\n"
        )

        print(log_message, flush=True)

    def reproduce(self) -> None:
        parents: List[Entity] = copy.copy(self.entities)
        used_parents: List[Entity] = []

        new_entities: List[Entity] = []

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

            parent_a, parent_b = random.sample(parents, 2)
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

    def write_simulation_data(self, generation_data: Dict) -> None:
        simulation_data_path = f"{self.settings.simulation_directory}/simulation_data.json"
        all_data: List[Dict] = self.load_simulation_data()

        with open(simulation_data_path, 'w') as f:
            all_data.append(generation_data)
            json.dump(all_data, f)

    def selection_condition(self, x: int, y: int) -> bool:
        w: int = self.settings.grid_width
        h: int = self.settings.grid_height

        if not self._selection_condition_callable:
            raise RuntimeError(f"selection condition not loaded for simulation '{self.settings.name}'")

        try:
            return bool(self._selection_condition_callable(x, y, w, h))
        except Exception as e:
            raise RuntimeError(f"selection_condition error: {e}")

    def update_survival_rate(self, alive_entities_count: int) -> None:
        self.survival_rate = alive_entities_count / self.settings.max_entity_count * 100

    def load_simulation_data(self) -> List:
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