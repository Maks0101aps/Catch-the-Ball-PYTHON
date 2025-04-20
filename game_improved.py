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

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Catch the Ball - Improved')
clock = pygame.time.Clock()

# Load assets
current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(current_dir, 'assets', 'images')

# Ball properties
ball_radius = 25
ball_x = random.randint(ball_radius, SCREEN_WIDTH - ball_radius)
ball_y = ball_radius + 10
ball_speed_x = random.choice([-4, -3, -2, 2, 3, 4])
ball_speed_y = 3
bounce_count = 0  # Track number of bounces for scoring
speed_increase = 0.2  # Скорость будет увеличиваться на это значение с каждым отскоком
max_speed_x = 12  # Максимальная скорость по x
max_speed_y = 12  # Максимальная скорость по y

# Platform properties
platform_width = 100
platform_height = 20
platform_x = SCREEN_WIDTH // 2 - platform_width // 2
platform_y = SCREEN_HEIGHT - 30
platform_speed = 8
platform_speed_increase = 0.5  # Скорость платформы будет расти
max_platform_speed = 15  # Максимальная скорость платформы

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
ball_img = load_svg_as_surface(os.path.join(assets_dir, 'ball.svg'), ball_radius * 2, ball_radius * 2)
platform_img = load_svg_as_surface(os.path.join(assets_dir, 'platform.svg'), platform_width, platform_height)

# Game functions
def draw_ball(x, y):
    screen.blit(ball_img, (x - ball_radius, y - ball_radius))

def draw_platform(x, y):
    screen.blit(platform_img, (x, y))

def show_score():
    score_text = font.render(f'Score: {score}', True, BLACK)
    lives_text = small_font.render(f'Lives: {lives}', True, BLACK)
    level_text = small_font.render(f'Level: {level}', True, BLACK)
    bounces_text = small_font.render(f'Bounces: {bounce_count}', True, BLACK)
    speed_text = small_font.render(f'Ball Speed: {abs(ball_speed_y):.1f}', True, BLACK)
    controls_text = small_font.render(f'Controls: Arrows/WASD', True, BLACK)
    
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (SCREEN_WIDTH - 200, 10))
    screen.blit(level_text, (10, 50))
    screen.blit(bounces_text, (10, 80))
    screen.blit(speed_text, (10, 110))
    screen.blit(controls_text, (SCREEN_WIDTH - 200, 40))

def check_collision(ball_x, ball_y, platform_x, platform_y):
    # Check if ball hits the platform
    if (platform_x - ball_radius < ball_x < platform_x + platform_width + ball_radius and 
        platform_y - ball_radius < ball_y < platform_y + platform_height//2):
        # Calculate bounce angle based on where the ball hit the platform
        # Middle of platform bounces straight up, edges angle the ball
        hit_pos = (ball_x - platform_x) / platform_width
        angle_factor = hit_pos * 2 - 1  # -1 to 1
        return True, angle_factor * 5  # Multiply by max angle (speed)
    return False, 0

def reset_ball():
    global bounce_count, platform_speed  # Make sure to reset bounce counter when ball is reset
    bounce_count = 0
    platform_speed = 8  # Сбрасываем скорость платформы
    return (random.randint(ball_radius * 2, SCREEN_WIDTH - ball_radius * 2), 
            ball_radius + 10,
            random.choice([-4, -3, -2, 2, 3, 4]),  # Random x speed
            3)  # Initial y speed

def game_over():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Semi-transparent overlay
    screen.blit(overlay, (0, 0))
    
    game_over_text = font.render('GAME OVER', True, WHITE)
    final_score_text = font.render(f'Final Score: {score}', True, WHITE)
    retry_text = font.render('Press SPACE to retry', True, WHITE)
    menu_text = font.render('Press M to return to menu', True, WHITE)
    quit_text = font.render('Press ESC to quit', True, WHITE)
    
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
    screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
    screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80))
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_SPACE:
                    waiting = False
                if event.key == K_m:
                    return_to_menu()
    
    global bounce_count
    bounce_count = 0
    return 0, 3, 1  # Reset score, lives, and level

# Main game loop
running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_m:
                return_to_menu()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if check_menu_button(event.pos):
                    return_to_menu()
    
    # Platform movement
    keys = pygame.key.get_pressed()
    
    # Движение влево (стрелка влево или A)
    if (keys[K_LEFT] or keys[K_a]) and platform_x > 0:
        platform_x -= platform_speed
    
    # Движение вправо (стрелка вправо или D)
    if (keys[K_RIGHT] or keys[K_d]) and platform_x < SCREEN_WIDTH - platform_width:
        platform_x += platform_speed
    
    # Ball movement
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    
    # Wall collisions
    if ball_x <= ball_radius or ball_x >= SCREEN_WIDTH - ball_radius:
        ball_speed_x = -ball_speed_x
    
    if ball_y <= ball_radius:
        ball_speed_y = -ball_speed_y
    
    # Platform collision
    hit, angle = check_collision(ball_x, ball_y, platform_x, platform_y)
    if hit:
        # Увеличиваем скорость мяча с каждым отскоком
        ball_speed_x = angle  # Angle based on hit position
        ball_speed_y = -abs(ball_speed_y) - speed_increase  # Bounce up with increased speed
        
        # Ограничиваем максимальную скорость
        if abs(ball_speed_x) > max_speed_x:
            ball_speed_x = max_speed_x * (1 if ball_speed_x > 0 else -1)
        if abs(ball_speed_y) > max_speed_y:
            ball_speed_y = -max_speed_y
            
        # Увеличиваем скорость платформы с ростом уровня
        platform_speed = min(max_platform_speed, platform_speed + platform_speed_increase / 5)
            
        bounce_count += 1
        
        # Add points for each bounce
        score += 1  # Fixed: Now adds just 1 point per bounce
        
        # Level up every 10 bounces
        if bounce_count % 10 == 0:
            level += 1
            platform_speed = min(max_platform_speed, platform_speed + platform_speed_increase)  # Increase platform speed with level
    
    # Ball out of bounds
    if ball_y > SCREEN_HEIGHT + ball_radius:
        lives -= 1
        
        if lives <= 0:
            score, lives, level = game_over()
            ball_x, ball_y, ball_speed_x, ball_speed_y = reset_ball()
        else:
            ball_x, ball_y, ball_speed_x, ball_speed_y = reset_ball()
    
    # Drawing
    screen.blit(background_img, (0, 0))
    draw_platform(platform_x, platform_y)
    draw_ball(ball_x, ball_y)
    show_score()
    draw_menu_button()
    pygame.display.update()
    
    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit() 