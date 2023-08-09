import numpy as np
import tomllib
import os
import pygame
from geometry import *

# == INIT ==
projection_matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 0]]

pygame.init()
window = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

shapes = [
    Cube(scale=1, position=(-200, -200), color=(0, 255, 0), rotation=Rotation(-45, 90, 45)),
    Cube(scale=2, position=(200, 200), color=(255, 0, 0), rotation=Rotation(0, 45, 90)),
]

    
def clear_terminal():
    """
    Clears the terminal.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def project_vertex(vertex):
    """
    Returns the 2D coordinates of a 3D vertex projected in 2D space
    """
    matmul_res = np.matmul(projection_matrix, vertex)
    return [matmul_res[0], matmul_res[1]]


def connect_edges(shape):
    for edge in shape.edges:
        pygame.draw.line(window, shape.color, (shape.points[edge[0]]), (shape.points[edge[1]]))


def render(shapes):
    clear_terminal()

    for shape in shapes:
        for index, vertex in enumerate(shape.vertices):
            rot_x = np.matmul(shape.rotation.x_mat, vertex)
            rot_y = np.matmul(shape.rotation.y_mat, rot_x)
            rot_z = np.matmul(shape.rotation.z_mat, rot_y)
            vertex_2d = project_vertex(rot_z)

            shape.rotation.rotate_all_axis(0.002)
            
            x = vertex_2d[0] * config['global_scale'] + (window.get_width() / 2) + (shape.position[0] * (config['global_scale'] / 100))
            y = vertex_2d[1] * config['global_scale'] + (window.get_height() / 2) + (shape.position[1] * (config['global_scale'] / 100))

            shape.points[index] = (x, y)

            pygame.draw.circle(window, shape.color, (x, y), config['vertex_scale'])
        connect_edges(shape)


def main():
    while True:
        clock.tick(60)
        window.fill(config['background_color'])
        render(shapes)

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