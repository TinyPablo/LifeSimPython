import copy
import json
import random
from typing import Dict, List
from gene import Gene
from genome import Genome
from grid import Grid
from entity import Entity
from simulation_settings import SimulationSettings


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
    

    def update_survival_rate(self, alive_entities_count: int) -> None:
        self.survival_rate = alive_entities_count / self.settings.max_entity_count * 100

    def log_generation_info(self) -> None:
        generation: int = self.current_generation
        safe_entities: float = len([e for e in self.entities if self.selection_condition(e.transform.position_x, e.transform.position_y)]) / self.settings.max_entity_count * 100
        survival_rate: float = self.survival_rate

        info: str = (
            f'SIMULATION: {self.settings.name}\n'
            f'GENERATION: {generation}\n'
            f'SAFE ENTITIES: {safe_entities:.2f}%\n'
            f'PREVIOUS SURVIVAL RATE: {survival_rate:.2f}%\n\n'
        )

        print(info, end='', flush=True)

    def update_genome_diversity(self) -> None:
        self.generation_data['genome_diversity'] = {}
        for entity in self.entities:
            for neuron in entity.brain.neurons:
                if neuron.disabled:
                    continue

                if neuron.name not in self.generation_data['genome_diversity']:
                    self.generation_data['genome_diversity'][neuron.name] = 1
                    continue
                
                self.generation_data['genome_diversity'][neuron.name] += 1


    def generation_loop(self) -> None:
        
        self.current_step = 1

        for entity in self.entities:
            entity.brain.init()

        
        self.update_genome_diversity()
        pictures: List[List[List[tuple[int, int, int]]]] = []
        while self.settings.steps_per_generation >= self.current_step and not self.simulation_ended:

            if self.current_step == self.settings.steps_per_generation:
                self.log_generation_info()

            # if (self.current_step % (1 // self.settings.loging_rate) == 0) or \
            # (self.current_step == 1) or (self.current_step == self.settings.steps_per_generation):
            #     self.log_info()
            


            # self.entities[0].brain.genome = Genome(genes=[Gene(), Gene()])
            # print(self.entities[0].brain)

            # self.entities[0].brain.init()
            # print(self.entities[0].brain)
            # [print(g) for g in self.entities[0].brain.genome.genes]
            # exit()


            for entity in self.entities:
                entity.brain.process()            
            
            pictures.append(self.grid.get_picture())
            self.current_step += 1

        self.on_generation_end(pictures)




    def on_generation_end(self, pictures: List[List[tuple[int, int, int]]]) -> None:
        self.update_simulation_data()
        self.do_natural_selection()     
        self.reproduce()
        
        self.grid.save_video(pictures, self.current_generation, self.survival_rate)
        
        self.place_new_generation_entities()


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

    def write_simulation_data(self, generation_data: Dict) -> None:
        simulation_data_path = f"{self.settings.simulation_directory}/simulation_data.json"
        all_data: List[Dict] = self.load_simulation_data()

        with open(simulation_data_path, 'w') as f:
            all_data.append(generation_data)
            json.dump(all_data, f)


    def update_simulation_data(self):
        #temp
        print('='*20)
        print(random.choice([e.brain for e in self.entities]))
        print("\033[F\033[K"+'='*20)  # remove line - temporary use
        #temp
        self.generation_data["generation"] = self.current_generation
        self.generation_data['random_brains_3'] = [str(random.choice([e.brain for e in self.entities])) for _ in range(3)]
        self.generation_data["survival_rate"] = self.survival_rate

        self.write_simulation_data(self.generation_data)


    def simulation_loop(self) -> None:
        self.current_generation = 1
    
        while not self.simulation_ended and self.current_generation < (self.settings.max_generations + 1):
            self.generation_loop()
            self.current_generation += 1

        print(f'simulation ended | SEED: {self.settings.seed}')

    def populate(self) -> None:
        self.entities = [Entity(Genome(self.settings.brain_size), self, self.grid) for _ in range(self.settings.max_entity_count)]
        
        for entity in self.entities:
            self.grid.deploy_entity_randomly(entity)
        

    def start(self) -> None:
        self.populate()
        self.simulation_loop()

    def selection_condition(self, x: int, y: int) -> bool:
        w: int = self.settings.grid_width
        h: int = self.settings.grid_height
                    
        return (x > w - w // 12)

    # def selection_condition(self, x: int, y: int) -> bool:
    #     w: int = self.settings.grid_width
    #     h: int = self.settings.grid_height

    #     return (x > w - w // 4) and (y > h - h // 4)

    # def selection_condition(self, x: int, y: int) -> bool:
    #     w: int = self.settings.grid_width
    #     h: int = self.settings.grid_height

    #     return (x > w - w // 3) and (y > h - h // 3)
    
    # def selection_condition(self, x: int, y: int) -> bool:
    #     w: int = self.settings.grid_width
    #     h: int = self.settings.grid_height

    #     return ((x < w // 5 and y < h // 5) or          # top-left
    #     (x > w - w // 5 and y < h // 5) or      # top-right
    #     (x < w // 5 and y > h - h // 5) or      # bottom-left
    #     (x > w - w // 5 and y > h - h // 5))    # bottom-right

    # def selection_condition(self, x: int, y: int) -> bool:
    #     w: int = self.settings.grid_width
    #     h: int = self.settings.grid_height

    #     # Define the size of the hollow square
    #     size = min(w, h) // 2  # width/height of the square
    #     thickness = 4          # how thick the border should be

    #     # Compute square bounds centered in the grid
    #     left = (w - size) // 2
    #     right = left + size
    #     top = (h - size) // 2
    #     bottom = top + size

    #     # Return True if point is on the border of the square
    #     on_vertical_border = left <= x <= right and (abs(y - top) < thickness or abs(y - bottom) < thickness)
    #     on_horizontal_border = top <= y <= bottom and (abs(x - left) < thickness or abs(x - right) < thickness)

    #     return on_vertical_border or on_horizontal_border

    
        
    def do_natural_selection(self) -> None:
        alive_entities = []
        for entity in self.entities:
            if self.selection_condition(entity.transform.position_x, entity.transform.position_y):
                alive_entities.append(entity)
            else:
                entity.die()
        self.entities = alive_entities


    def reproduce(self) -> None:
        parents: List[Entity] = copy.copy(self.entities)
        used_parents: List[Entity] = []

        new_entities: List[Entity] = []
            
        self.update_survival_rate(len(parents))

        if len(parents) < 2:
            print("population went extinct")
            self.simulation_ended = True
            return      
        
        for mind in range(self.settings.fresh_minds):
            fresh_mind: Entity = Entity(Genome(self.settings.brain_size), self, self.grid)
            new_entities.append(fresh_mind)
        
        while len(new_entities) < self.settings.max_entity_count:      

            if len(parents) < 2:
                parents += used_parents
                used_parents.clear()

            parent_a, parent_b = random.sample(parents, 2)
            child_genome: Genome = Genome.crossover(parent_a.brain.genome, parent_b.brain.genome, self.settings.gene_mutation_probability)

            entity: Entity = Entity(child_genome, self, self.grid)
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