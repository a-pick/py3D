from scene import Scene
from geometry import Cube

class TestScene(Scene):
    def __init__(self) -> None:
        super().__init__()
        self.shapes = [
            Cube()
        ]