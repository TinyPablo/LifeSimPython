from direction import Direction
import math
import matplotlib.pyplot as plt
import numpy as np

def get_relative_direction_old(current_direction: Direction, relative_direction: Direction) -> Direction:
    direction_mapping = {
        (Direction.UP, Direction.UP): Direction.UP,
        }
    
    return direction_mapping[(current_direction, relative_direction)]


def get_relative_direction(facing_direction: Direction, relative_direction: Direction) -> Direction:
        facing_x, facing_y = facing_direction.value
        relative_x, relative_y = relative_direction.value

        def to_degrees(vec):
            x, y = vec
            return math.degrees(math.atan2(y, x))

        degrees = 360 - to_degrees((facing_x, facing_y))
        print(degrees)
        return degrees



def display_angle(angle: float) -> None:
    angle_rad = np.deg2rad(angle)

    # Line length (arbitrary, say 1 unit)
    length = 1.0

    # Compute end point using cosine (x) and sine (y)
    x_end = length * np.cos(angle_rad)
    y_end = length * np.sin(angle_rad)

    # Draw line from origin (0,0) to endpoint
    plt.plot([0, x_end], [0, y_end], 'r-', linewidth=2)

    # Draw origin and setup axes
    plt.scatter(0, 0, color='black')
    plt.axis('equal')
    plt.xlim(-1.5, 1.5)
    plt.ylim(-1.5, 1.5)
    plt.grid(True)
    plt.title(f"{angle}°")
    plt.show()



display_angle(get_relative_direction(Direction.UP, Direction.DOWN))
display_angle(get_relative_direction(Direction.UP_LEFT, Direction.DOWN))

display_angle(get_relative_direction(Direction.LEFT, Direction.DOWN))
display_angle(get_relative_direction(Direction.DOWN_LEFT, Direction.DOWN))

display_angle(get_relative_direction(Direction.DOWN, Direction.DOWN))
display_angle(get_relative_direction(Direction.DOWN_RIGHT, Direction.DOWN))

display_angle(get_relative_direction(Direction.RIGHT, Direction.DOWN))
display_angle(get_relative_direction(Direction.UP_RIGHT, Direction.DOWN))