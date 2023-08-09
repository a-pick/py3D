import numpy as np
import tomllib
import os
import pygame
from geometry import *

pygame.init()
window = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

shapes = [
    Cube(scale=1, position=(-200, -200), color=(0, 255, 0), start_rotation=Rotation(0, 0, 0, "xyz", 0.0025)),
    Pyramid(scale=0.25, position=(175, 175), color=(255, 0, 0), start_rotation=Rotation(0, 15, -90, "x", 0.005)),
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


def connect_edges(shape):
    """
    Connects the edges of a shape using its edge definition and its points.
    """
    for edge in shape.edges:
        pygame.draw.line(window, shape.color, (shape.points[edge[0]]), (shape.points[edge[1]]))


def render(shapes):
    """
    Renders the shapes in the window.
    """
    clear_terminal()

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
            
            # Scale and translate each vertex
            x = vertex_2d[0] * config['global_scale'] + (window.get_width() / 2) + (shape.position[0] * (config['global_scale'] / 100))
            y = vertex_2d[1] * config['global_scale'] + (window.get_height() / 2) + (shape.position[1] * (config['global_scale'] / 100))

            shape.points[index] = (x, y)
            pygame.draw.circle(window, shape.color, (x, y), shape.scale * config['vertex_scale'])
        connect_edges(shape)


def main():
    while True:
        clock.tick(60)
        window.fill(config['background_color'])
        render(shapes)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        pygame.display.update()


if __name__ == '__main__':
    main()