import pygame
from pygame_widgets.slider import Slider
import pygame_widgets
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
    pygame.display.set_caption("3D Engine")
    
    # GUI (wip)
    # slider = Slider(window, 10, 10, 265, 10, min=0, max=255, step=1, handleRadius=5, initial=50, handleColour=(255, 0, 0), colour=(100, 0, 0), handleOnColour=(0, 0, 255), handleOnRadius=20, handleOnOutline=2, handleImageHeight=40, handleImageWidth=40, onRelease=lambda: print(slider.getValue()))
    
    engine = engine3D.Engine3D(window)
    
    # Main loop
    clock = pygame.time.Clock()
    running = True
    while running:
        # Event handling
        events = pygame.event.get()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Clear the display buffer
        window.fill((0, 0, 0))
                
        # Engine update
        engine.update(clock.tick() / 1000.0)
        pygame_widgets.update(events)
         
        # Update display
        pygame.display.update()
    
    pygame.quit()
    
if __name__ == "__main__":
    main()
