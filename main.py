# main.py handles window management, the main loop and event handling.

import pygame
from utils import load_config
import engine3D


def main():
    
    # Initialization
    config = load_config()
    pygame.init()
    window = pygame.display.set_mode((
        config['Window Settings']['window_width'], 
        config['Window Settings']['window_height']
        ))
    
    engine = engine3D.Engine3D(window)
    
    # Main loop
    running = True
    while running:
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Engine update
        engine.update(pygame.time.get_ticks() / 1000.0)
         
        # Update display
        pygame.display.update()
    
    pygame.quit()
    
    
if __name__ == "__main__":
    main()

