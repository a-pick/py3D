import math
import numpy as np


class Projection:
    projection_matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 0]]
    inverse_projection_matrix = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]


class Rotation:
    def __init__(self, angle_x: float = 0, angle_y: float = 0, angle_z: float = 0, rotation_mode: str = "xyz", speed: float = 0.0025):
        self.angle_x = math.radians(angle_x)
        self.angle_y = math.radians(angle_y)
        self.angle_z = math.radians(angle_z)
        self.rotation_mode = rotation_mode
        self.speed = speed
        self.update_matrices()

    def update_matrices(self):
        self.x_mat = [
            [1, 0, 0],
            [0, math.cos(self.angle_x), -math.sin(self.angle_x)],
            [0, math.sin(self.angle_x), math.cos(self.angle_x)]
        ]
        self.y_mat = [
            [math.cos(self.angle_y), 0, math.sin(self.angle_y)],
            [0, 1, 0],
            [-math.sin(self.angle_y), 0, math.cos(self.angle_y)]
        ]
        self.z_mat = [
            [math.cos(self.angle_z), -math.sin(self.angle_z), 0],
            [math.sin(self.angle_z), math.cos(self.angle_z), 0],
            [0, 0, 1]
        ]

    def rotate(self):
        match self.rotation_mode:
            case "x":
                self.rotate_x()
            case "y":
                self.rotate_y()
            case "z":
                self.rotate_z()
            case "xyz":
                self.rotate_xyz()
            case "xy":
                self.rotate_xy()
            case "xz":
                self.rotate_xz()
    
    def rotate_x(self):
        self.angle_x += self.speed
        self.update_matrices()

    def rotate_y(self):
        self.angle_y += self.speed
        self.update_matrices()

    def rotate_z(self):
        self.angle_z += self.speed
        self.update_matrices()
        
    def rotate_xyz(self):
        self.angle_x += self.speed
        self.angle_y += self.speed
        self.angle_z += self.speed
        self.update_matrices()
        
    def rotate_xy(self):
        self.angle_x += self.speed
        self.angle_y += self.speed
        self.update_matrices()
        
    def rotate_xz(self):
        self.angle_x += self.speed
        self.angle_z += self.speed
        self.update_matrices()


class Shape:
    def __init__(self, scale, position, color, start_rotation):
        self.scale = scale
        self.position = position
        self.color = color
        self.start_rotation = start_rotation
        self.vertices = []
        self.points = []
        self.edges = []


class Cube(Shape):
    def __init__(self, scale: int = 1, position: tuple = (0, 0), color: tuple = (255, 255, 255), start_rotation: Rotation = Rotation(0, 0, 0, "")):
        super().__init__(scale=scale, position=position, color=color, start_rotation=start_rotation)
        self.vertices =  [
            (-scale, -scale, -scale),
            (-scale, -scale, scale),
            (-scale, scale, -scale),
            (-scale, scale, scale),
            (scale, -scale, -scale),
            (scale, -scale, scale),
            (scale, scale, -scale),
            (scale, scale, scale)
        ]
        self.points = [0 for _ in range(len(self.vertices))]
        self.edges = [
            (0, 1),
            (0, 2),
            (0, 4),
            (1, 3),
            (1, 5),
            (2, 3),
            (2, 6),
            (3, 7),
            (4, 5),
            (4, 6),
            (5, 7),
            (7, 6)
        ]
      
        
class Pyramid(Shape):
    def __init__(self, scale: int = 1, position: tuple = (0, 0), color: tuple = (255, 255, 255), start_rotation: Rotation = Rotation(0, 0, 0, "")):
        super().__init__(scale=scale, position=position, color=color, start_rotation=start_rotation)
        self.vertices =  [
            (-scale, -scale, -scale),
            (-scale, -scale, scale),
            (-scale, scale, -scale),
            (-scale, scale, scale),
            (scale, 0, 0)
        ]
        self.points = [0 for _ in range(len(self.vertices))]
        self.edges = [
            (0, 1),
            (0, 2),
            (0, 4),
            (1, 3),
            (1, 4),
            (2, 3),
            (2, 4),
            (3, 4)
        ]