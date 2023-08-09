import math

class Rotation:
    def __init__(self, angle_x: float = 0, angle_y: float = 0, angle_z: float = 0):
        self.angle_x = angle_x
        self.angle_y = angle_y
        self.angle_z = angle_z
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

    def rotate_x(self, speed: float):
        self.angle_x += speed
        self.update_matrices()

    def rotate_y(self, speed: float):
        self.angle_y += speed
        self.update_matrices()

    def rotate_z(self, speed: float):
        self.angle_z += speed
        self.update_matrices()
        
    def rotate_all_axis(self, speed: float):
        self.angle_x += speed
        self.angle_y += speed
        self.angle_z += speed
        self.update_matrices()


class Shape:
    def __init__(self, scale, position, color, rotation):
        self.scale = scale
        self.position = position
        self.color = color
        self.rotation = rotation
        self.vertices = []
        self.points = []
        self.edges = []


class Cube(Shape):
    def __init__(self, scale: int = 1, position: tuple = (0, 0), color: tuple = (255, 255, 255), rotation: Rotation = Rotation(0, 0, 0)):
        super().__init__(scale=scale, position=position, color=color, rotation=rotation)
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