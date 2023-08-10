class Triangle:
    def __init__(self):
        self.points = [0 for _ in range(3)]
        
class Mesh:
    def __init__(self):
        triangles = [Triangle() for _ in range(3)]
        
class Cube(Mesh):
    def __init__(self):
        super().__init__()
        
        self.triangles = [
            # South
            [0, 0, 0,    0, 1, 0,    1, 1, 0],
            [0, 0, 0,    1, 1, 0,    1, 0, 0],
            
            # East
            [1, 0, 0,    1, 1, 0,    1, 1, 1],
            [1, 0, 0,    1, 1, 1,    1, 0, 1],
            
            # North
            [1, 0, 1,    1, 1, 1,    0, 1, 1],
            [1, 0, 1,    0, 1, 1,    0, 0, 1],
            
            # West
            [0, 0, 1,    0, 1, 1,    0, 1, 0],
            [0, 0, 1,    0, 1, 0,    0, 0, 0],
            
            # Top
            [0, 1, 0,    0, 1, 1,    1, 1, 1],
            [0, 1, 0,    1, 1, 1,    1, 1, 0],
            
            # Bottom
            [1, 0, 1,    0, 0, 1,    0, 0, 0],
        ]