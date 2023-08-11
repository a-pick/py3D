import pygame
from pygame_widgets.slider import Slider
from pygame_widgets.button import Button
from pygame_widgets.toggle import Toggle
from pygame_widgets.textbox import TextBox
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
    pygame.font.init()
    
    # GUI (wip)
    checkbox = Toggle(window, 10, 10, 25, 10)  
    events = pygame.event.get()        
    checkbox.listen(events)
    
    engine = engine3D.Engine3D(window)
    
    # Main loop
    clock = pygame.time.Clock()
    running = True
    while running:
        # Event handling
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                
        # Clear the display buffer
        window.fill((0, 0, 0))
        
        if checkbox.getValue() == 1:
            engine.wireframe = True
        else:
            engine.wireframe = False
        
        # Engine update
        engine.update(clock.tick() / 1000.0)
        pygame_widgets.update(events)
        
        # Font rendering
        display_font = pygame.font.SysFont("Monospace", 16)
        wireframe_label = display_font.render("Wireframe?", 1, (255,255,255))
        window.blit(wireframe_label, (50, 5))
        
        # Update display
        pygame.display.update()
        pygame.display.set_caption(f"Xander's 'Perfectly Optimized' 3D Engine | FPS: {round(clock.get_fps())}")
    
    pygame.quit()
    
if __name__ == "__main__":
    main()
