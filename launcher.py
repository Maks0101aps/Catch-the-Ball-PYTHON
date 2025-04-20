import pygame
import sys
import subprocess
import os
import platform
import random
from pygame.locals import *

def get_python_executable():
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        return sys.executable
    else:
        if platform.system() == "Windows":
            return os.path.join("venv", "Scripts", "python.exe")
        else:
            return os.path.join("venv", "bin", "python")

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)
LIGHT_BLUE = (100, 200, 255)
GREEN = (0, 180, 0)
LIGHT_GREEN = (100, 255, 100)
PURPLE = (170, 50, 180)
LIGHT_PURPLE = (210, 120, 220)
GOLD = (255, 215, 0)
LIGHT_GOLD = (255, 240, 110)
RED = (255, 50, 50)
LIGHT_RED = (255, 150, 150)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Catch the Ball - Launcher')
clock = pygame.time.Clock()

RESOLUTION_OPTIONS = [
    {"name": "HD (1280x720)", "width": 1280, "height": 720},
    {"name": "Full HD (1920x1080)", "width": 1920, "height": 1080},
    {"name": "HD+ (1600x900)", "width": 1600, "height": 900},
    {"name": "XGA (1024x768)", "width": 1024, "height": 768}
]

selected_resolution = 0

class Button:
    def __init__(self, x, y, width, height, text, action=None, color=BLUE, hover_color=LIGHT_BLUE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False
        self.font = pygame.font.Font(None, 48)
        self.color = color
        self.hover_color = hover_color
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        
        pygame.draw.rect(surface, color, self.rect, border_radius=20)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=20)
        
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.action:
                self.action()

def launch_new_game():
    pygame.quit()
    python_exe = get_python_executable()
    resolution = RESOLUTION_OPTIONS[selected_resolution]
    width = resolution["width"]
    height = resolution["height"]
    subprocess.Popen([python_exe, "catch_the_ball.py", str(width), str(height)])
    sys.exit()
    
def cycle_resolution():
    global selected_resolution
    selected_resolution = (selected_resolution + 1) % len(RESOLUTION_OPTIONS)

def quit_game():
    pygame.quit()
    sys.exit()

button_width, button_height = 400, 80
center_x = SCREEN_WIDTH // 2 - button_width // 2

play_button = Button(center_x, SCREEN_HEIGHT // 2 - 120, button_width, button_height, "Play (10 levels)", launch_new_game, GOLD, LIGHT_GOLD)
resolution_button = Button(center_x, SCREEN_HEIGHT // 2, button_width, button_height, RESOLUTION_OPTIONS[selected_resolution]["name"], cycle_resolution, GREEN, LIGHT_GREEN)
quit_button = Button(center_x, SCREEN_HEIGHT // 2 + 120, button_width, button_height, "Exit", quit_game, RED, LIGHT_RED)

buttons = [play_button, resolution_button, quit_button]

def main():
    title_font = pygame.font.Font(None, 96)
    title_text = title_font.render("Catch the Ball", True, BLACK)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    
    version_font = pygame.font.Font(None, 36)
    version_text = version_font.render("Choose your resolution", True, BLACK)
    version_rect = version_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 80))
    
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    for y in range(SCREEN_HEIGHT):
        color_value = 255 - int(y * 100 / SCREEN_HEIGHT)
        color = (200, 220, color_value)
        pygame.draw.line(background, color, (0, y), (SCREEN_WIDTH, y))
    
    for _ in range(50):
        size = random.randint(5, 20)
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        alpha = random.randint(10, 60)
        bubble = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(bubble, (255, 255, 255, alpha), (size//2, size//2), size//2)
        background.blit(bubble, (x, y))
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
                
            for button in buttons:
                button.handle_event(event)
                
        for button in buttons:
            button.update(mouse_pos)
        
        resolution_button.text = RESOLUTION_OPTIONS[selected_resolution]["name"]
            
        screen.blit(background, (0, 0))
        screen.blit(title_text, title_rect)
        screen.blit(version_text, version_rect)
        
        for button in buttons:
            button.draw(screen)
            
        pygame.display.update()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 