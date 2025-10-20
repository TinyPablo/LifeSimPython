import os
import random
import threading
from typing import Optional, List, TYPE_CHECKING
import cv2
import numpy as np
from cell import Cell
from direction import Direction
from simulation_settings import settings
from PIL import Image

if TYPE_CHECKING:
    from entity import Entity
    from simulation import Simulation

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
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

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
        for y, row in enumerate(self.grid):
            picture_row = []
            for x, cell in enumerate(row):
                if cell.is_entity:
                    color = cell.object.color
                else:
                    if self.simulation.selection_condition(y, x):
                        color = (144, 238, 144)
                    else:
                        color = (255, 255, 255)
                    
                picture_row.append(color)
            picture.append(picture_row)
        return picture


    @staticmethod
    def save_video(pictures: List[List[tuple[int, int, int]]], generation: int, survival_rate: float) -> None:
        def save() -> None:
            path: str = f"{settings.simulation_directory}/videos"
            os.makedirs(path, exist_ok=True)
            video_path = f'{path}/gen-{generation} surv-{survival_rate:.2f}.avi'
            
            upscale_factor = 4
            original_height, original_width = len(pictures[0]), len(pictures[0][0])
            height, width = original_height * upscale_factor, original_width * upscale_factor
            
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            video = cv2.VideoWriter(video_path, fourcc, settings.video_framerate, (width, height), isColor=True)
            
            for picture in pictures:
                frame = np.array(picture, dtype=np.uint8)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                upscaled_frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_NEAREST)
                video.write(upscaled_frame)
            
            video.release()
        
        threading.Thread(target=save).start()

     

    # def render(self, GEN: int, STEP: int) -> None:
    #     path = f'{settings.simulation_directory}/{settings.seed}/{GEN}'
    #     os.makedirs(path, exist_ok=True)

    #     full_path = f'{path}/{STEP}.png'
        
    #     img = Image.new('RGB', (self.width, self.height), "white")
    #     pixels = img.load()
        
    #     for y in range(self.height):
    #         for x in range(self.width):
    #             cell = self.grid[x][y]
    #             if cell.is_entity:
    #                 pixels[x, y] = cell.object.color
    #             elif not cell.is_occupied:
    #                 pixels[x, y] = (255, 255, 255)
        
    #     img.save(full_path)

    def move(self, entity: 'Entity', direction: Direction, absolute_direction: Optional[Direction] = None) -> None:
        x: int = entity.transform.position_x
        y: int = entity.transform.position_y
        
        new_x: int = x + direction.value[0]
        new_y: int = y + direction.value[1]

        if self.try_set_position(entity, new_x, new_y):
            self.remove_entity(x, y)
            entity.set_position(new_x, new_y)
            entity.transform.direction = absolute_direction if absolute_direction is not None else direction

    def move_relative(self, entity: 'Entity', direction: Direction) -> None:
        current_direction = entity.transform.direction
        relative_direction = self.get_relative_direction(current_direction, direction)
        self.move(entity, relative_direction, relative_direction)

    def in_boundaries(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height


    def blockage_in_direction(self, entity: 'Entity', direction: Direction) -> bool:
        x: int = entity.transform.position_x + direction.value[0]
        y: int = entity.transform.position_y + direction.value[1]
        return not self.in_boundaries(x, y) or self.grid[x][y].is_occupied

    # @staticmethod 
    # def get_relative_direction(current_direction: Direction, relative_direction: Direction) -> Direction:
    #     # Obrót kierunku relatywnego względem bieżącego kierunku
    #     cx, cy = current_direction.value
    #     rx, ry = relative_direction.value

    #     # Wszystkie kierunki traktujemy jako wektory 2D
    #     # Wyznaczamy kąt aktualnego kierunku w radianach
    #     import math

    #     def to_angle(vec):
    #         x, y = vec
    #         return math.atan2(y, x)

    #     def from_angle(angle):
    #         # Zamieniamy z powrotem na najbliższy kierunek 8-kierunkowy
    #         dirs = list(Direction)
    #         best = min(dirs, key=lambda d: abs(angle - to_angle(d.value)))
    #         return best

    #     angle_current = to_angle((cx, cy))
    #     angle_relative = to_angle((rx, ry))

    #     # Sumujemy kąty, by uzyskać nowy globalny kierunek
    #     angle_result = angle_current + angle_relative

    #     # Normalizujemy wynik do najbliższego kierunku z Direction
    #     return from_angle(angle_result)


#     @staticmethod 
#     def get_relative_direction(current_direction: Direction, relative_direction: Direction) -> Direction:
#         direction_mapping = {
#     (Direction.UP, Direction.UP): Direction.UP,
#     (Direction.UP, Direction.DOWN): Direction.UP,
#     (Direction.UP, Direction.LEFT): Direction.UP_LEFT,
#     (Direction.UP, Direction.RIGHT): Direction.UP_RIGHT,
#     (Direction.UP, Direction.UP_LEFT): Direction.UP_LEFT,
#     (Direction.UP, Direction.UP_RIGHT): Direction.UP_RIGHT,
#     (Direction.UP, Direction.DOWN_LEFT): Direction.LEFT,
#     (Direction.UP, Direction.DOWN_RIGHT): Direction.RIGHT,

#     (Direction.DOWN, Direction.UP): Direction.DOWN,
#     (Direction.DOWN, Direction.DOWN): Direction.DOWN,
#     (Direction.DOWN, Direction.LEFT): Direction.DOWN_LEFT,
#     (Direction.DOWN, Direction.RIGHT): Direction.DOWN_RIGHT,
#     (Direction.DOWN, Direction.UP_LEFT): Direction.LEFT,
#     (Direction.DOWN, Direction.UP_RIGHT): Direction.RIGHT,
#     (Direction.DOWN, Direction.DOWN_LEFT): Direction.DOWN_LEFT,
#     (Direction.DOWN, Direction.DOWN_RIGHT): Direction.DOWN_RIGHT,

#     (Direction.LEFT, Direction.UP): Direction.UP_LEFT,
#     (Direction.LEFT, Direction.DOWN): Direction.DOWN_LEFT,
#     (Direction.LEFT, Direction.LEFT): Direction.LEFT,
#     (Direction.LEFT, Direction.RIGHT): Direction.LEFT,
#     (Direction.LEFT, Direction.UP_LEFT): Direction.UP_LEFT,
#     (Direction.LEFT, Direction.UP_RIGHT): Direction.UP,
#     (Direction.LEFT, Direction.DOWN_LEFT): Direction.DOWN_LEFT,
#     (Direction.LEFT, Direction.DOWN_RIGHT): Direction.DOWN,

#     (Direction.RIGHT, Direction.UP): Direction.UP_RIGHT,
#     (Direction.RIGHT, Direction.DOWN): Direction.DOWN_RIGHT,
#     (Direction.RIGHT, Direction.LEFT): Direction.RIGHT,
#     (Direction.RIGHT, Direction.RIGHT): Direction.RIGHT,
#     (Direction.RIGHT, Direction.UP_LEFT): Direction.UP,
#     (Direction.RIGHT, Direction.UP_RIGHT): Direction.UP_RIGHT,
#     (Direction.RIGHT, Direction.DOWN_LEFT): Direction.DOWN,
#     (Direction.RIGHT, Direction.DOWN_RIGHT): Direction.DOWN_RIGHT,

#     (Direction.UP_LEFT, Direction.UP): Direction.UP_LEFT,
#     (Direction.UP_LEFT, Direction.DOWN): Direction.LEFT,
#     (Direction.UP_LEFT, Direction.LEFT): Direction.UP_LEFT,
#     (Direction.UP_LEFT, Direction.RIGHT): Direction.UP,
#     (Direction.UP_LEFT, Direction.UP_LEFT): Direction.UP_LEFT,
#     (Direction.UP_LEFT, Direction.UP_RIGHT): Direction.UP,
#     (Direction.UP_LEFT, Direction.DOWN_LEFT): Direction.LEFT,
#     (Direction.UP_LEFT, Direction.DOWN_RIGHT): Direction.LEFT,

#     (Direction.UP_RIGHT, Direction.UP): Direction.UP_RIGHT,
#     (Direction.UP_RIGHT, Direction.DOWN): Direction.RIGHT,
#     (Direction.UP_RIGHT, Direction.LEFT): Direction.UP,
#     (Direction.UP_RIGHT, Direction.RIGHT): Direction.UP_RIGHT,
#     (Direction.UP_RIGHT, Direction.UP_LEFT): Direction.UP,
#     (Direction.UP_RIGHT, Direction.UP_RIGHT): Direction.UP_RIGHT,
#     (Direction.UP_RIGHT, Direction.DOWN_LEFT): Direction.RIGHT,
#     (Direction.UP_RIGHT, Direction.DOWN_RIGHT): Direction.RIGHT,

#     (Direction.DOWN_LEFT, Direction.UP): Direction.LEFT,
#     (Direction.DOWN_LEFT, Direction.DOWN): Direction.DOWN_LEFT,
#     (Direction.DOWN_LEFT, Direction.LEFT): Direction.DOWN_LEFT,
#     (Direction.DOWN_LEFT, Direction.RIGHT): Direction.DOWN,
#     (Direction.DOWN_LEFT, Direction.UP_LEFT): Direction.LEFT,
#     (Direction.DOWN_LEFT, Direction.UP_RIGHT): Direction.DOWN,
#     (Direction.DOWN_LEFT, Direction.DOWN_LEFT): Direction.DOWN_LEFT,
#     (Direction.DOWN_LEFT, Direction.DOWN_RIGHT): Direction.DOWN,

#     (Direction.DOWN_RIGHT, Direction.UP): Direction.RIGHT,
#     (Direction.DOWN_RIGHT, Direction.DOWN): Direction.DOWN_RIGHT,
#     (Direction.DOWN_RIGHT, Direction.LEFT): Direction.DOWN,
#     (Direction.DOWN_RIGHT, Direction.RIGHT): Direction.DOWN_RIGHT,
#     (Direction.DOWN_RIGHT, Direction.UP_LEFT): Direction.DOWN,
#     (Direction.DOWN_RIGHT, Direction.UP_RIGHT): Direction.RIGHT,
#     (Direction.DOWN_RIGHT, Direction.DOWN_LEFT): Direction.DOWN,
#     (Direction.DOWN_RIGHT, Direction.DOWN_RIGHT): Direction.DOWN_RIGHT
# }
#         return direction_mapping[(current_direction, relative_direction)]