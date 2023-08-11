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
    def __init__(self, v1: Vec3=Vec3(0,0,0), v2: Vec3=Vec3(0,0,0), v3: Vec3=Vec3(0,0,0), color: tuple=(255,255,255)):
        self.points = [v1, v2, v3]
        self.color = color

class Mesh:
    def __init__(self):
        self.triangles = []
        
    def load_object_from_obj(self, filename: str):
        with open(filename, "r") as f:
            data = f.readlines()
        vertices = []
        
        # while not at the end of the file
        for line in data:
            if line.startswith("v "):
                # split the line into a list of strings
                vertex = line.split()
                # append the vertex to the list of vertices
                vertices.append(Vec3(float(vertex[1]), float(vertex[2]), float(vertex[3])))
            elif line.startswith("f "):
                # split the line into a list of strings
                face = line.split()
                # append the face to the list of faces
                self.triangles.append(Triangle(vertices[int(face[1]) - 1], vertices[int(face[2]) - 1], vertices[int(face[3]) - 1]))
            
        return True

class Monkey(Mesh):
    def __init__(self):
        super().__init__()
        self.load_object_from_obj("models/suzanne.obj")

class Cube(Mesh):
    def __init__(self):
        super().__init__()
        self.load_object_from_obj("models/cube.obj")
