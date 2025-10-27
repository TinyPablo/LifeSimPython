import json
import os
import random
from typing import Dict

from selection_conditions.enum import SelectionCondition
from utils import get_time_now


class SimulationSettings:
    def __init__(self, settings_dict: Dict = None):
        self.name: str = None

        self.random_seed: bool = False
        self.seed: int = 0

        self.grid_width: int = 128
        self.grid_height: int = 128

        self.steps_per_generation: int = 256
        self.max_generations: int = 10_000_000
        self.selection_condition: SelectionCondition | None = None

        self.max_entity_count: int = 1024
        self.brain_size: int = 1
        self.max_internal_neurons: int = 0
        self.fresh_minds: int = 1

        self.gene_mutation_probability: float = 1 / 10_000

        self.video_framerate: int = 30
        self.video_upscale_factor: int = 8

        if settings_dict:
            for key, value in settings_dict.items():
                if key == "selection_condition" and isinstance(value, str):
                    self.selection_condition = SelectionCondition(value)
                elif hasattr(self, key):
                    setattr(self, key, value)

        self.initialize_seed()

        if not self.name:
            self.name = f"SIMULATION_{self.seed}"
        self.simulation_directory = f"./simulations/{self.name} {get_time_now()}"

        self.save_settings()

    def initialize_seed(self):
        if self.random_seed:
            self.seed = random.getrandbits(32)
        random.seed(self.seed)

    def save_settings(self) -> None:
        os.makedirs(self.simulation_directory, exist_ok=True)
        data: Dict = {
            "general": {
                "name": self.name
            },
            "randomness": {
                "random_seed": self.random_seed,
                "seed": self.seed
            },
            "grid": {
                "width": self.grid_width,
                "height": self.grid_height
            },
            "simulation_control": {
                "steps_per_generation": self.steps_per_generation,
                "max_generations": self.max_generations,
                "selection_condition": self.selection_condition.value if self.selection_condition else None
            },
            "entities_and_brain": {
                "max_entity_count": self.max_entity_count,
                "brain_size": self.brain_size,
                "max_internal_neurons": self.max_internal_neurons,
                "fresh_minds": self.fresh_minds
            },
            "mutation_and_evolution": {
                "gene_mutation_probability": self.gene_mutation_probability
            },
            "video": {
                "video_framerate": self.video_framerate,
                "video_upscale_factor": self.video_upscale_factor
            },
            "directories": {
                "simulation_directory": self.simulation_directory
            }
        }
        with open(f"{self.simulation_directory}/settings.json", "w+") as f:
            json.dump(data, f, indent=4)