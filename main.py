import numpy as np
import tomllib
import os
import pygame
from geometry import *

selected_shape = None
selected_vertex_index = None
mouse_release_pos = None
mouse_dragging = False
mouse_3d_homogenous = None

pygame.init()
window = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

shapes = [
    Cube(scale=1, position=(-200, -200), color=(0, 255, 0), start_rotation=Rotation(0, 0, 0, "xyz", 0.0025)),
    Pyramid(scale=1, position=(175, 175), color=(255, 0, 0), start_rotation=Rotation(0, 15, -90, "x", 0)),
]

    
def clear_terminal():
    """
    Clears the terminal.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def project_vertex(vertex):
    """
    Returns the 2D coordinates of a 3D vertex projected in 2D space.
    """
    matmul_res = np.matmul(Projection.projection_matrix, vertex)
    return [matmul_res[0], matmul_res[1]]


def connect_edges(shape, color=None):
    """
    Connects the edges of a shape using its edge definition and its points.
    """
    for edge in shape.edges:
        if color is not None:
            pygame.draw.line(window, color, (shape.points[edge[0]]), (shape.points[edge[1]]))
        else:
            pygame.draw.line(window, shape.color, (shape.points[edge[0]]), (shape.points[edge[1]]))


def update(shapes):
    """
    Handles the update logic.
    """
    clear_terminal()
    mouse_3d_homogenous = None
    mouse_ndc = None
    x = 0
    y = 0

    for shape in shapes:
        for index, vertex in enumerate(shape.vertices):
            # Rotate each vertex according to the shape's rotation matrices
            rot_x = np.matmul(shape.start_rotation.x_mat, vertex)
            rot_y = np.matmul(shape.start_rotation.y_mat, rot_x)
            rot_z = np.matmul(shape.start_rotation.z_mat, rot_y)
            
            # Project each vertex in 2D space
            vertex_2d = project_vertex(rot_z)

            # Per-shape rotation
            shape.start_rotation.rotate()
            
            # Vertex "grabbing"
            if mouse_dragging and selected_shape is not None and selected_vertex_index is not None and selected_shape == shape:
                mouse_pos = pygame.mouse.get_pos()
                
                # Normalized device coordinates 
                ndc_x = (mouse_pos[0] / window.get_width() - 0.5) * 2
                ndc_y = (mouse_pos[1] / window.get_height() - 0.5) * 2
                mouse_ndc = [ndc_x, ndc_y, 0, 1]
                
                # Reverse projection to convert from 2D to 3D
                mouse_3d_homogenous = np.matmul(Projection.inverse_projection_matrix, mouse_ndc)
                mouse_3d = mouse_3d_homogenous[:3] / mouse_3d_homogenous[3]
                
                shape.vertices[selected_vertex_index] = mouse_3d
                shape.points[selected_vertex_index] = mouse_pos
            
            # Scale and translate each point
            x = vertex_2d[0] * config['global_scale'] + (window.get_width() // 2) + (shape.position[0] * (config['global_scale'] // 100))
            y = vertex_2d[1] * config['global_scale'] + (window.get_height() // 2) + (shape.position[1] * (config['global_scale'] // 100))
            shape.points[index] = (x, y)
                
            pygame.draw.circle(window, shape.color, (x, y), shape.scale * config['vertex_scale'])
            
        connect_edges(shape)
        
        clear_terminal()
        print(f"selected_shape: {selected_shape}\nselected_vertex_index: {selected_vertex_index}\nmouse_release_pos: {mouse_release_pos}\nmouse_dragging: {mouse_dragging}\nmouse_3d_homogenous: {mouse_3d_homogenous}\nmouse_ndc: {mouse_ndc}")


def main():
    global selected_shape, selected_vertex_index, mouse_release_pos, mouse_dragging, mouse_3d_homogenous
    
    while True:
        clock.tick(60)
        window.fill(config['background_color'])
        update(shapes)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for shape in shapes:
                        for index, vertex in enumerate(shape.points):
                            distance = np.linalg.norm(np.array(vertex) - np.array(event.pos))
                            if distance <= (shape.scale * config['vertex_scale'] + config['vertex_selection_forgiveness']):
                                selected_shape = shape
                                selected_vertex_index = index
                                mouse_dragging = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_release_pos = event.pos
                    mouse_dragging = False
                    selected_shape = None
                    selected_vertex_index = None
            
        pygame.display.update()


if __name__ == '__main__':
    main()