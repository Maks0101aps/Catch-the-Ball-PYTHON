import pygame
import sys
import subprocess
import os
import platform
from pygame.locals import *

# Функция для определения пути к Python в виртуальной среде
def get_python_executable():
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        # Уже в виртуальной среде
        return sys.executable
    else:
        # Определяем путь к Python в виртуальной среде
        if platform.system() == "Windows":
            return os.path.join("venv", "Scripts", "python.exe")
        else:
            return os.path.join("venv", "bin", "python")

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 350  # Increased height for extra button
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)
LIGHT_BLUE = (100, 200, 255)
GREEN = (0, 180, 0)
LIGHT_GREEN = (100, 255, 100)
PURPLE = (170, 50, 180)
LIGHT_PURPLE = (210, 120, 220)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Catch the Ball - Launcher')
clock = pygame.time.Clock()

# Button class
class Button:
    def __init__(self, x, y, width, height, text, action=None, color=BLUE, hover_color=LIGHT_BLUE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False
        self.font = pygame.font.Font(None, 32)
        self.color = color
        self.hover_color = hover_color
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        
        # Draw button
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        
        # Draw text
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.action:
                self.action()

# Button actions
def launch_simple_game():
    pygame.quit()
    python_exe = get_python_executable()
    subprocess.Popen([python_exe, "game.py"])
    sys.exit()
    
def launch_improved_game():
    pygame.quit()
    python_exe = get_python_executable()
    subprocess.Popen([python_exe, "game_improved.py"])
    sys.exit()
    
def launch_enhanced_game():
    pygame.quit()
    python_exe = get_python_executable()
    subprocess.Popen([python_exe, "enhanced_game.py"])
    sys.exit()
    
def quit_game():
    pygame.quit()
    sys.exit()

# Create buttons
button_width, button_height = 250, 50
center_x = SCREEN_WIDTH // 2 - button_width // 2

simple_button = Button(center_x, 80, button_width, button_height, "Simple Game", launch_simple_game)
improved_button = Button(center_x, 145, button_width, button_height, "Improved Game", launch_improved_game, GREEN, LIGHT_GREEN)
enhanced_button = Button(center_x, 210, button_width, button_height, "Advanced Game", launch_enhanced_game, PURPLE, LIGHT_PURPLE)
quit_button = Button(center_x, 275, button_width, button_height, "Quit", quit_game)

buttons = [simple_button, improved_button, enhanced_button, quit_button]

# Main loop
def main():
    title_font = pygame.font.Font(None, 48)
    title_text = title_font.render("Catch the Ball", True, BLACK)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 40))
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
                
            # Handle button events
            for button in buttons:
                button.handle_event(event)
                
        # Update
        for button in buttons:
            button.update(mouse_pos)
            
        # Draw
        screen.fill(WHITE)
        screen.blit(title_text, title_rect)
        
        for button in buttons:
            button.draw(screen)
            
        pygame.display.update()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 