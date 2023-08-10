from geometry import *
from utils import multiply_matrix_vector, draw_triangle
import pygame
import numpy as np
import math

cube = Cube()

class Engine3D:
    """
    Engine manages the main loop, window creation, and event handling.
    """
    global projection_matrix
    
    def __init__(self, window: pygame.Surface = None):
        self.window = window
        
        # Projection matrix
        projection_matrix = np.zeros((4, 4))
        
        near = 0.1
        far = 1000
        fov = 90
        fov_rad = 1 / math.tan(fov * 0.5 / 180 * math.pi)
        aspect_ratio = window.get_height() / window.get_width()
        
        projection_matrix[0][0] = aspect_ratio * fov_rad
        projection_matrix[1][1] = fov_rad
        projection_matrix[2][2] = far / (far - near)
        projection_matrix[3][2] = (-far * near) / (far - near)
        projection_matrix[2][3] = 1
        projection_matrix[3][3] = 0
        
    def update(self, deltatime: float):
        for triangle in cube.triangles:
            triangle_projected = Triangle()
            multiply_matrix_vector(triangle.points[0], triangle_projected.points[0], projection_matrix)
            multiply_matrix_vector(triangle.points[1], triangle_projected.points[1], projection_matrix)
            multiply_matrix_vector(triangle.points[2], triangle_projected.points[2], projection_matrix)

            draw_triangle(triangle_projected.points, (255, 255, 255), self.window)