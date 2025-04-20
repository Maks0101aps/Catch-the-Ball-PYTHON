import pygame
import sys
import random
import os
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Catch the Ball - Advanced')
clock = pygame.time.Clock()

# Load assets
current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(current_dir, 'assets', 'images')

# Platform properties
platform_width = 100
platform_height = 15
platform_x = SCREEN_WIDTH // 2 - platform_width // 2
platform_y = SCREEN_HEIGHT - 30
platform_speed = 8

# Ball properties
ball_radius = 15
ball_colors = [RED, BLUE, GREEN, YELLOW]
balls = []  # List to store multiple balls

# Game variables
score = 0
lives = 3
level = 1
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Button for menu return
menu_button_width = 100
menu_button_height = 30
menu_button_x = SCREEN_WIDTH - menu_button_width - 10
menu_button_y = 10
menu_button_rect = pygame.Rect(menu_button_x, menu_button_y, menu_button_width, menu_button_height)

def draw_menu_button():
    pygame.draw.rect(screen, (150, 150, 150), menu_button_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, menu_button_rect, 2, border_radius=10)
    menu_text = small_font.render("Menu", True, BLACK)
    screen.blit(menu_text, (menu_button_x + menu_button_width//2 - menu_text.get_width()//2, 
                           menu_button_y + menu_button_height//2 - menu_text.get_height()//2))

def check_menu_button(mouse_pos):
    return menu_button_rect.collidepoint(mouse_pos)

def return_to_menu():
    # Return to the launcher menu
    pygame.quit()
    import subprocess
    subprocess.Popen([sys.executable, "launcher.py"])
    sys.exit()

# Load SVG images and convert them to Pygame surfaces
def load_svg_as_surface(filename, width, height):
    # We're going to use pygame to render the SVG
    # In a real implementation, we'd use a proper SVG library like cairosvg
    # For this example, we'll load a backup red circle if SVG loading fails
    try:
        # Try to create a simple surface with a gradient effect
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        if "ball" in filename:
            # Create a red ball with custom gradient
            pygame.draw.circle(surface, (255, 0, 0), (width//2, height//2), width//2-2)
            # Add a highlight
            pygame.draw.circle(surface, (255, 200, 200), (width//3, height//3), width//6)
        elif "platform" in filename:
            # Create a blue platform with custom gradient
            pygame.draw.rect(surface, (0, 100, 255), (0, 0, width, height), border_radius=height//4)
            # Add a highlight
            pygame.draw.rect(surface, (100, 150, 255), (2, 2, width-4, height//4), border_radius=height//8)
        elif "background" in filename:
            # Create a gradient background
            for y in range(height):
                color_value = 255 - int(y * 100 / height)
                color = (200, 220, color_value)
                pygame.draw.line(surface, color, (0, y), (width, y))
        
        return surface
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        # Create fallback surface
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        if "ball" in filename:
            pygame.draw.circle(surface, RED, (width//2, height//2), width//2-2)
        elif "platform" in filename:
            pygame.draw.rect(surface, BLUE, (0, 0, width, height), border_radius=height//4)
        return surface

# Load images
background_img = load_svg_as_surface(os.path.join(assets_dir, 'background.svg'), SCREEN_WIDTH, SCREEN_HEIGHT)
platform_img = load_svg_as_surface(os.path.join(assets_dir, 'platform.svg'), platform_width, platform_height)

# Ball class
class Ball:
    def __init__(self):
        self.radius = random.randint(10, 20)
        self.x = random.randint(self.radius, SCREEN_WIDTH - self.radius)
        self.y = 0
        self.speed = random.uniform(2, 5)
        self.color = random.choice(ball_colors)
        self.points = max(1, 6 - int(self.radius / 3))  # Smaller balls are worth more points
        # Load ball image with correct size
        self.image = load_svg_as_surface(os.path.join(assets_dir, 'ball.svg'), self.radius * 2, self.radius * 2)
    
    def update(self):
        self.y += self.speed
    
    def draw(self):
        # Draw the ball using the SVG image
        screen.blit(self.image, (self.x - self.radius, self.y - self.radius))
    
    def is_caught(self, plat_x, plat_y, plat_width, plat_height):
        return (plat_x - self.radius < self.x < plat_x + plat_width + self.radius and 
                plat_y - self.radius < self.y < plat_y + self.radius)
    
    def is_out_of_bounds(self):
        return self.y > SCREEN_HEIGHT + self.radius

# Platform class
class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = BLUE
        self.speed = platform_speed
    
    def update(self, keys):
        # Движение влево (стрелка влево или A)
        if (keys[K_LEFT] or keys[K_a]) and self.x > 0:
            self.x -= self.speed
        # Движение вправо (стрелка вправо или D)
        if (keys[K_RIGHT] or keys[K_d]) and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
    
    def draw(self):
        # Draw the platform using the SVG image
        screen.blit(platform_img, (self.x, self.y))

# Game controller
class Game:
    def __init__(self):
        self.platform = Platform(platform_x, platform_y, platform_width, platform_height)
        self.balls = []
        self.score = 0
        self.lives = lives
        self.level = level
        self.game_over_state = False
        self.spawn_timer = 0
        self.spawn_interval = 60  # Frames between ball spawns
        
    def update(self, events):
        if self.game_over_state:
            # Check for menu button click in game over state
            for event in events:
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.reset()
                    elif event.key == K_m:
                        return_to_menu()
                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if check_menu_button(event.pos):
                            return_to_menu()
            return
            
        # Handle menu button clicks during gameplay
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_m:
                    return_to_menu()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if check_menu_button(event.pos):
                        return_to_menu()
                        
        # Update platform
        keys = pygame.key.get_pressed()
        self.platform.update(keys)
        
        # Spawn new balls
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.balls.append(Ball())
            self.spawn_timer = 0
            
        # Update and check collisions for each ball
        balls_to_remove = []
        for ball in self.balls:
            ball.update()
            
            # Check if ball is caught
            if ball.is_caught(self.platform.x, self.platform.y, self.platform.width, self.platform.height):
                self.score += ball.points
                balls_to_remove.append(ball)
                
                # Level up every 20 points
                if self.score // 20 + 1 > self.level:
                    self.level = self.score // 20 + 1
                    self.spawn_interval = max(10, 60 - self.level * 5)  # Spawn balls faster as level increases
                    
            # Check if ball is missed
            elif ball.is_out_of_bounds():
                self.lives -= 1
                balls_to_remove.append(ball)
                if self.lives <= 0:
                    self.game_over_state = True
                    
        # Remove caught or missed balls
        for ball in balls_to_remove:
            if ball in self.balls:
                self.balls.remove(ball)
    
    def draw(self):
        # Draw background using the SVG image
        screen.blit(background_img, (0, 0))
            
        # Draw platform
        self.platform.draw()
        
        # Draw balls
        for ball in self.balls:
            ball.draw()
        
        # Draw UI elements
        score_text = font.render(f'Score: {self.score}', True, BLACK)
        level_text = small_font.render(f'Level: {self.level}', True, BLACK)
        lives_text = small_font.render(f'Lives: {self.lives}', True, BLACK)
        controls_text = small_font.render(f'Controls: Arrows/WASD', True, BLACK)
        
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))
        screen.blit(lives_text, (SCREEN_WIDTH - 200, 10))
        screen.blit(controls_text, (SCREEN_WIDTH - 200, 40))
        
        # Draw menu button
        draw_menu_button()
        
        # Draw game over screen
        if self.game_over_state:
            self.draw_game_over()
            
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent overlay
        screen.blit(overlay, (0, 0))
        
        game_over_text = font.render('GAME OVER', True, WHITE)
        final_score_text = font.render(f'Final Score: {self.score}', True, WHITE)
        retry_text = font.render('Press SPACE to retry', True, WHITE)
        menu_text = font.render('Press M to return to menu', True, WHITE)
        quit_text = font.render('Press ESC to quit', True, WHITE)
        
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
        screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80))
            
    def reset(self):
        self.__init__()

# Main game loop
def main():
    game = Game()
    running = True

    while running:
        # Collect events
        events = pygame.event.get()
        
        # Check for quit event
        for event in events:
            if event.type == QUIT:
                running = False
                
        # Update game state
        game.update(events)
        
        # Render
        game.draw()
        pygame.display.update()
        
        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 