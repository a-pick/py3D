import tomllib
import pygame

def load_config():
    """
    Returns a dictionary containing the configuration file data.
    """
    with open("config.toml", "rb") as f:
        return tomllib.load(f)
    
def multiply_matrix_vector(a, b, m):
    b[0] = a[0] * m[0][0] + a[1] * m[1][0] + a[2] * m[2][0] + m[3][0]
    b[1] = a[0] * m[0][1] + a[1] * m[1][1] + a[2] * m[2][1] + m[3][1]
    b[2] = a[0] * m[0][2] + a[1] * m[1][2] + a[2] * m[2][2] + m[3][2]
    w = a[0] * m[0][3] + a[1] * m[1][3] + a[2] * m[2][3] + m[3][3]
    
    if (w != 0.0):
        b[0] /= w
        b[1] /= w
        b[2] /= w
        
def draw_triangle(points: list, color: tuple, surface: pygame.Surface):
    pygame.draw.polygon(surface, color, points)