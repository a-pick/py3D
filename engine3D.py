from geometry import *
from utils import multiply_matrix_vector, draw_triangle
import pygame
import math

cube = Cube()

class Engine3D:
    """
    Engine manages the main loop, window creation, and event handling.
    """
    projection_matrix = Mat4x4()
    theta = 0
    wireframe = True
    
    def __init__(self, window: pygame.Surface):
        self.window = window
        
        near = 0.1
        far = 1000.0
        fov = 50
        fov_rad = 1 / math.tan(fov * 0.5 / 180 * math.pi)
        aspect_ratio = window.get_height() / window.get_width()
        
        self.projection_matrix[0][0] = aspect_ratio * fov_rad
        self.projection_matrix[1][1] = fov_rad
        self.projection_matrix[2][2] = far / (far - near)
        self.projection_matrix[3][2] = (-far * near) / (far - near)
        self.projection_matrix[2][3] = 1
        self.projection_matrix[3][3] = 0
        
    def update(self, deltatime: float):
        # Rotation matrices
        mat_rot_z = Mat4x4()
        mat_rot_x = Mat4x4()
        self.theta += float(deltatime)
        
        # Z rotation matrix
        mat_rot_z[0][0] = math.cos(self.theta)
        mat_rot_z[0][1] = math.sin(self.theta)
        mat_rot_z[1][0] = -math.sin(self.theta)
        mat_rot_z[1][1] = math.cos(self.theta)
        mat_rot_z[2][2] = 1
        mat_rot_z[3][3] = 1
        
        # X rotation matrix
        mat_rot_x[0][0] = 1
        mat_rot_x[1][1] = math.cos(self.theta)
        mat_rot_x[1][2] = math.sin(self.theta)
        mat_rot_x[2][1] = -math.sin(self.theta)
        mat_rot_x[2][2] = math.cos(self.theta)
        mat_rot_x[3][3] = 1
        
        # Draw triangles
        for triangle in cube.triangles:
            triangle_projected = Triangle()
            triangle_translated = Triangle()
            triangle_rotated_z = Triangle()
            triangle_rotated_z_x = Triangle()
            
            # Z rotation
            multiply_matrix_vector(triangle.points[0], triangle_projected.points[0], mat_rot_z)
            multiply_matrix_vector(triangle.points[1], triangle_projected.points[1], mat_rot_z)
            multiply_matrix_vector(triangle.points[2], triangle_projected.points[2], mat_rot_z)

            # X rotation
            multiply_matrix_vector(triangle_projected.points[0], triangle_rotated_z_x.points[0], mat_rot_x)
            multiply_matrix_vector(triangle_projected.points[1], triangle_rotated_z_x.points[1], mat_rot_x)
            multiply_matrix_vector(triangle_projected.points[2], triangle_rotated_z_x.points[2], mat_rot_x)
            
            # Translation
            triangle_translated = triangle_rotated_z_x
            triangle_translated.points[0].z = triangle_rotated_z_x.points[0].z + 3.0
            triangle_translated.points[1].z = triangle_rotated_z_x.points[1].z + 3.0
            triangle_translated.points[2].z = triangle_rotated_z_x.points[2].z + 3.0
            
            # Projection
            multiply_matrix_vector(triangle_translated.points[0], triangle_projected.points[0], self.projection_matrix)
            multiply_matrix_vector(triangle_translated.points[1], triangle_projected.points[1], self.projection_matrix)
            multiply_matrix_vector(triangle_translated.points[2], triangle_projected.points[2], self.projection_matrix)
            
            # Scale into view
            triangle_projected.points[0].x += 1; triangle_projected.points[0].y += 1
            triangle_projected.points[1].x += 1; triangle_projected.points[1].y += 1
            triangle_projected.points[2].x += 1; triangle_projected.points[2].y += 1
            triangle_projected.points[0].x *= 0.5 * self.window.get_width()
            triangle_projected.points[0].y *= 0.5 * self.window.get_height()
            triangle_projected.points[1].x *= 0.5 * self.window.get_width()
            triangle_projected.points[1].y *= 0.5 * self.window.get_height()
            triangle_projected.points[2].x *= 0.5 * self.window.get_width()
            triangle_projected.points[2].y *= 0.5 * self.window.get_height()
            
            # Draw triangle
            _points = [(vec.x, vec.y) for vec in triangle_projected.points]
            if self.wireframe == True:
                draw_triangle(_points, (255, 255, 255), self.window)
            if self.wireframe == False:
                draw_triangle(_points, (255, 255, 255), self.window, fill=True)