class Vec3:
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z
        
    def __getitem__(self, index: int):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        raise IndexError("Index out of range.")
        
    def __setitem__(self, index: int, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        elif index == 2:
            self.z = value
            
    def __add__(self, other: 'Vec3') -> 'Vec3':
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
class Mat4x4:
    def __init__(self) -> None:
        self.m = [[0.0 for _ in range(4)] for _ in range(4)]
        
    def __repr__(self) -> str:
        return str(self.m)
    
    def __getitem__(self, index: int) -> list:
        return self.m[index]
    
class Triangle:
    def __init__(self, v1: Vec3=Vec3(0,0,0), v2: Vec3=Vec3(0,0,0), v3: Vec3=Vec3(0,0,0)):
        self.points = [v1, v2, v3]

class Mesh:
    def __init__(self):
        self.triangles = []

class Cube(Mesh):
    def __init__(self):
        super().__init__()
        self.triangles = [
            Triangle(Vec3(0, 0, 0), Vec3(0, 1, 0), Vec3(1, 1, 0)),  # South (Front) face, Triangle 1
            Triangle(Vec3(0, 0, 0), Vec3(1, 1, 0), Vec3(1, 0, 0)),  # South (Front) face, Triangle 2

            Triangle(Vec3(1, 0, 0), Vec3(1, 1, 0), Vec3(1, 1, 1)),  # East face, Triangle 3
            Triangle(Vec3(1, 0, 0), Vec3(1, 1, 1), Vec3(1, 0, 1)),  # East face, Triangle 4

            Triangle(Vec3(1, 0, 1), Vec3(1, 1, 1), Vec3(0, 1, 1)),  # North face, Triangle 5
            Triangle(Vec3(1, 0, 1), Vec3(0, 1, 1), Vec3(0, 0, 1)),  # North face, Triangle 6

            Triangle(Vec3(0, 0, 1), Vec3(0, 1, 1), Vec3(0, 1, 0)),  # West face, Triangle 7
            Triangle(Vec3(0, 0, 1), Vec3(0, 1, 0), Vec3(0, 0, 0)),  # West face, Triangle 8

            Triangle(Vec3(0, 1, 0), Vec3(0, 1, 1), Vec3(1, 1, 1)),  # Top face, Triangle 9
            Triangle(Vec3(0, 1, 0), Vec3(1, 1, 1), Vec3(1, 1, 0)),  # Top face, Triangle 10

            Triangle(Vec3(1, 0, 1), Vec3(0, 0, 1), Vec3(0, 0, 0)),  # Bottom face, Triangle 11
            Triangle(Vec3(1, 0, 1), Vec3(0, 0, 0), Vec3(1, 0, 0))   # Bottom face, Triangle 12
        ]
