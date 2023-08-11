from geometry import *
from utils import multiply_matrix_vector, draw_triangle, load_config
import pygame
import math

monkey = Monkey()

class Engine3D:
    """
    Engine manages the main loop, window creation, and event handling.
    """
    config = load_config()
    
    camera_position = Vec3(0, 0, 0)
    projection_matrix = Mat4x4()
    theta = 0
    wireframe = True
    
    def __init__(self, window: pygame.Surface):
        self.window = window
        
        near = self.config['Camera Settings']['near']
        far = self.config['Camera Settings']['far']
        fov = self.config['Camera Settings']['fov']
        perspective_warp = self.config['Camera Settings']['perspective_warp']
        
        fov_rad = 1 / math.tan(fov * 0.5 / 180 * math.pi)
        aspect_ratio = window.get_height() / window.get_width()
        
        self.projection_matrix[0][0] = aspect_ratio * fov_rad
        self.projection_matrix[1][1] = fov_rad
        self.projection_matrix[2][2] = far / (far - near)
        self.projection_matrix[3][2] = (-far * near) / (far - near)
        self.projection_matrix[2][3] = perspective_warp
        self.projection_matrix[3][3] = 0
        
    def update(self, deltatime: float):
        # Rotation matrices
        mat_rot_z = Mat4x4()
        mat_rot_x = Mat4x4()
        self.theta += deltatime
        
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
        for triangle in monkey.triangles:
            triangle_projected = Triangle()
            triangle_translated = Triangle()
            triangle_rotated_z = Triangle()
            triangle_rotated_z_x = Triangle()
            
            # Z rotation
            multiply_matrix_vector(triangle.points[0], triangle_rotated_z.points[0], mat_rot_z)
            multiply_matrix_vector(triangle.points[1], triangle_rotated_z.points[1], mat_rot_z)
            multiply_matrix_vector(triangle.points[2], triangle_rotated_z.points[2], mat_rot_z)

            # X rotation
            multiply_matrix_vector(triangle_projected.points[0], triangle_rotated_z_x.points[0], mat_rot_x)
            multiply_matrix_vector(triangle_projected.points[1], triangle_rotated_z_x.points[1], mat_rot_x)
            multiply_matrix_vector(triangle_projected.points[2], triangle_rotated_z_x.points[2], mat_rot_x)
            
            # Translation
            triangle_translated = triangle_rotated_z_x
            triangle_translated.points[0].z = triangle_rotated_z_x.points[0].z + 50.0
            triangle_translated.points[1].z = triangle_rotated_z_x.points[1].z + 50.0
            triangle_translated.points[2].z = triangle_rotated_z_x.points[2].z + 50.0
            
            normal = Vec3(0, 0, 0)
            line1 = Vec3(0, 0, 0)
            line2 = Vec3(0, 0, 0)
            
            line1.x = triangle_translated.points[1].x - triangle_translated.points[0].x
            line1.y = triangle_translated.points[1].y - triangle_translated.points[0].y
            line1.z = triangle_translated.points[1].z - triangle_translated.points[0].z
            
            line2.x = triangle_translated.points[2].x - triangle_translated.points[0].x
            line2.y = triangle_translated.points[2].y - triangle_translated.points[0].y
            line2.z = triangle_translated.points[2].z - triangle_translated.points[0].z
            
            normal.x = line1.y * line2.z - line1.z * line2.y
            normal.y = line1.z * line2.x - line1.x * line2.z
            normal.z = line1.x * line2.y - line1.y * line2.x
            
            normalized_normal = math.sqrt(normal.x * normal.x + normal.y * normal.y + normal.z * normal.z)
            normal.x /= normalized_normal
            normal.y /= normalized_normal
            normal.z /= normalized_normal
            
            # Projection
            if (normal.x * (triangle_translated.points[0].x - self.camera_position.x) +
                normal.y * (triangle_translated.points[0].y - self.camera_position.y) +
                normal.z * (triangle_translated.points[0].z - self.camera_position.z) < 0.0
                ):
                
                # Lighting
                light_direction = Vec3(0, 0, -1)
                light_direction_normalized = math.sqrt(light_direction.x * light_direction.x + light_direction.y * light_direction.y + light_direction.z * light_direction.z)
                light_direction.x /= light_direction_normalized
                light_direction.y /= light_direction_normalized
                light_direction.z /= light_direction_normalized
                
                luminance = normal.x * light_direction.x + normal.y * light_direction.y + normal.z * light_direction.z
                triangle_translated.color = (abs(luminance * 255), abs(luminance * 255), abs(luminance * 255))
                
                multiply_matrix_vector(triangle_translated.points[0], triangle_projected.points[0], self.projection_matrix)
                multiply_matrix_vector(triangle_translated.points[1], triangle_projected.points[1], self.projection_matrix)
                multiply_matrix_vector(triangle_translated.points[2], triangle_projected.points[2], self.projection_matrix)
                triangle_projected.color = triangle_translated.color
            
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
                    draw_triangle(_points, triangle_projected.color, self.window)
                if self.wireframe == False:
                    draw_triangle(_points, triangle_projected.color, self.window, fill=True)