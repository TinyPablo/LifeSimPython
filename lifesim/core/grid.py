from __future__ import annotations

import os
import threading
from typing import TYPE_CHECKING

import cv2
import numpy as np

from lifesim.core.cell import Cell
from lifesim.core.entity import Entity
from lifesim.utils.direction import Direction
from lifesim.utils.direction_map import ABSOLUTE_DIRECTION_MAPPING
from lifesim.utils.rng import rng

if TYPE_CHECKING:
    from lifesim.core.simulation import Simulation  

class Grid:
    def __init__(self, width: int, height: int, simulation: Simulation) -> None:
        self.width: int = width
        self.height: int = height
        self.simulation: Simulation = simulation
        self.grid: list[list[Cell]] = [[Cell() for _ in range(self.height)] for _ in range(self.width)]

    def __str__(self) -> str:
        grid_str = '\n'.join(
            ' '.join(str(self.grid[x][y]) for x in range(self.width))
            for y in range(self.height)
        )
        return grid_str

    def __repr__(self) -> str:
        return self.__str__()

    def deploy_entity_randomly(self, entity: Entity) -> None:
        attempted_positions = set()
        attempts = 0
        max_attempts = self.width * self.height

        while attempts < max_attempts:
            x = rng.random.randint(0, self.width - 1)
            y = rng.random.randint(0, self.height - 1)

            if (x, y) in attempted_positions:
                continue
            
            attempted_positions.add((x, y))
            placed = self.try_set_position(entity, x, y)

            if placed:
                entity.grid = self
                return
            
            attempts += 1

        raise Exception('All cells are taken')
    
    def try_set_position(self, object: Entity, x: int, y: int) -> bool:
        if not self.in_boundaries(x, y):
            return False
        
        if self.grid[x][y].is_occupied:
            return False
        
        self.place_object(object, x, y)
        return True

    def place_object(self, object: Entity, x: int, y: int) -> None:
        self.grid[x][y].set_object(object)
        object.set_position(x, y)

    def remove_entity(self, x: int, y: int) -> None:
        cell = self.grid[x][y]
        if cell.is_entity:
            self.grid[x][y].reset()
    
    def get_picture(self) -> np.ndarray:
        sim = self.simulation
        w, h = sim.settings.grid_width, sim.settings.grid_height

        picture = np.full((h, w, 3), 255, dtype=np.uint8)

        mask = sim._selection_mask
        if mask is not None:
            picture[mask] = (144, 238, 144)

        for entity in sim.entities:
            x, y = entity.transform.position_x, entity.transform.position_y
            picture[y, x] = entity.color

        return picture

    def save_video(self, pictures: list[np.ndarray], generation: int, survival_rate: float) -> None:
        pictures_copy = list(pictures)
        def save() -> None:
            if not pictures_copy:
                return
            path: str = f"{self.simulation.settings.simulation_directory}/videos"
            os.makedirs(path, exist_ok=True)
            video_path = f'{path}/{self.simulation.settings.name} gen-{generation} surv-{survival_rate:.2f}.avi'

            original_height, original_width = len(pictures_copy[0]), len(pictures_copy[0][0])
            height, width = (
                original_height * self.simulation.settings.video_upscale_factor,
                original_width * self.simulation.settings.video_upscale_factor,
            )

            fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # type: ignore[attr-defined]
            video = cv2.VideoWriter(video_path, fourcc, self.simulation.settings.video_framerate, (width, height), isColor=True)

            for picture in pictures_copy:
                frame = np.array(picture, dtype=np.uint8)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                upscaled_frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_NEAREST)
                video.write(upscaled_frame)

            video.release()

        threading.Thread(target=save, daemon=True).start()

    def move(self, entity: Entity, direction: Direction) -> None:
        x: int = entity.transform.position_x
        y: int = entity.transform.position_y
        
        new_x: int = x + direction.value[0]
        new_y: int = y + direction.value[1]

        if self.try_set_position(entity, new_x, new_y):
            self.remove_entity(x, y)
            entity.set_position(new_x, new_y)
            entity.transform.direction = direction
            
    def move_relative(self, entity: Entity, relative_direction: Direction) -> None:
        facing_direction = entity.transform.direction
        absolute_direction = self.get_absolute_direction(facing_direction, relative_direction)
        self.move(entity, absolute_direction)

    def in_boundaries(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def blockage_in_direction(self, entity: Entity, direction: Direction) -> bool:
        x: int = entity.transform.position_x + direction.value[0]
        y: int = entity.transform.position_y + direction.value[1]
        return not self.in_boundaries(x, y) or self.grid[x][y].is_occupied

    @staticmethod
    def get_absolute_direction(facing_direction: Direction, relative_direction: Direction) -> Direction:
        return ABSOLUTE_DIRECTION_MAPPING[(facing_direction, relative_direction)]