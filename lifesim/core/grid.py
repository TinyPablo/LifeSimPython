import os
import threading
from typing import List, TYPE_CHECKING
import cv2
import numpy as np

from lifesim.core.cell import Cell
from lifesim.utils.direction import Direction
from lifesim.utils.rng import rng


if TYPE_CHECKING:
    from lifesim.core.entity import Entity
    from lifesim.core.simulation import Simulation


class Grid:
    def __init__(self, width: int, height: int, simulation: 'Simulation') -> None:
        self.width: int = width
        self.height: int = height
        self.simulation: 'Simulation' = simulation
        self.grid: List[List[Cell]] = [[Cell() for _ in range(self.height)] for _ in range(self.width)]

    def __str__(self) -> str:
        grid_str = '\n'.join(
            ' '.join(str(self.grid[x][y]) for x in range(self.width))
            for y in range(self.height)
        )
        return grid_str

    def __repr__(self) -> str:
        return self.__str__()

    def deploy_entity_randomly(self, entity: 'Entity') -> None:
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
    
    def try_set_position(self, object: 'Entity', x: int, y: int) -> bool:
        if not self.in_boundaries(x, y):
            return False
        
        if self.grid[x][y].is_occupied:
            return False
        
        self.place_object(object, x, y)
        return True

    def place_object(self, object: 'Entity', x: int, y: int) -> None:
        self.grid[x][y].set_object(object)
        object.set_position(x, y)

    def remove_entity(self, x: int, y: int) -> None:
        cell = self.grid[x][y]
        if cell.is_entity:
            self.grid[x][y].reset()

    def get_picture(self) -> List[List[tuple[int, int, int]]]:
        picture = []
        width = len(self.grid[0])
        height = len(self.grid)

        for y in range(height):
            picture_row = []
            for x in range(width):
                cell = self.grid[x][y]
                if cell.is_entity:
                    color = cell.object.color
                elif (x, y) in self.simulation.tracked_positions:
                    color = (0, 0, 0)  # black 
                    
                elif self.simulation.selection_condition(x, y):
                    color = (144, 238, 144)  # green
                else:
                    color = (255, 255, 255)  # white
                picture_row.append(color)
            picture.append(picture_row)

        return picture


    def save_video(self, pictures: List[List[tuple[int, int, int]]], generation: int, survival_rate: float) -> None:
        def save() -> None:
            path: str = f"{self.simulation.settings.simulation_directory}/videos"
            os.makedirs(path, exist_ok=True)
            video_path = f'{path}/{self.simulation.settings.name} gen-{generation} surv-{survival_rate:.2f}.avi'
            
            original_height, original_width = len(pictures[0]), len(pictures[0][0])
            height, width = original_height * self.simulation.settings.video_upscale_factor, original_width * self.simulation.settings.video_upscale_factor
            
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            video = cv2.VideoWriter(video_path, fourcc, self.simulation.settings.video_framerate, (width, height), isColor=True)
            
            for picture in pictures:
                frame = np.array(picture, dtype=np.uint8)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                upscaled_frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_NEAREST)
                video.write(upscaled_frame)
            
            video.release()
        
        threading.Thread(target=save).start()

    def move(self, entity: 'Entity', direction: Direction) -> None:
        x: int = entity.transform.position_x
        y: int = entity.transform.position_y
        
        new_x: int = x + direction.value[0]
        new_y: int = y + direction.value[1]

        if self.try_set_position(entity, new_x, new_y):
            self.remove_entity(x, y)
            entity.set_position(new_x, new_y)
            entity.transform.direction = direction
            
    def move_relative(self, entity: 'Entity', relative_direction: Direction) -> None:
        facing_direction = entity.transform.direction
        absolute_direction = self.get_absolute_direction(facing_direction, relative_direction)
        self.move(entity, absolute_direction)

    def in_boundaries(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def blockage_in_direction(self, entity: 'Entity', direction: Direction) -> bool:
        x: int = entity.transform.position_x + direction.value[0]
        y: int = entity.transform.position_y + direction.value[1]
        return not self.in_boundaries(x, y) or self.grid[x][y].is_occupied
    
    @staticmethod 
    def get_absolute_direction(facing: Direction, relative: Direction) -> Direction:
        directions = [
            Direction.UP,
            Direction.UP_RIGHT,
            Direction.RIGHT,
            Direction.DOWN_RIGHT,
            Direction.DOWN,
            Direction.DOWN_LEFT,
            Direction.LEFT,
            Direction.UP_LEFT,
        ]
        i_facing = directions.index(facing)
        i_relative = directions.index(relative)
        i_absolute = (i_facing + i_relative) % len(directions)
        return directions[i_absolute]