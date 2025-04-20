import pygame
import sys
import random
import os
from pygame.locals import *

pygame.init()

if len(sys.argv) >= 3:
    SCREEN_WIDTH = int(sys.argv[1])
    SCREEN_HEIGHT = int(sys.argv[2])
else:
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 180, 0)
YELLOW = (255, 255, 0)
PURPLE = (180, 50, 180)
ORANGE = (255, 140, 0)

KEY_A = 97
KEY_D = 100
KEY_S = 115
KEY_W = 119
KEY_M = 109
KEY_LEFT = pygame.K_LEFT
KEY_RIGHT = pygame.K_RIGHT
KEY_ESCAPE = pygame.K_ESCAPE
KEY_SPACE = pygame.K_SPACE

LEVELS = [
    {"name": "First Steps", "ball_speed": 5, "platform_width": 140, "platform_speed": 10, "ball_count": 1, "background_color": (200, 240, 255)},
    {"name": "Warm Up", "ball_speed": 6, "platform_width": 130, "platform_speed": 11, "ball_count": 1, "background_color": (220, 240, 220)},
    {"name": "First Challenge", "ball_speed": 7, "platform_width": 120, "platform_speed": 12, "ball_count": 1, "background_color": (240, 240, 200)},
    {"name": "Double Trouble", "ball_speed": 7, "platform_width": 120, "platform_speed": 12, "ball_count": 2, "background_color": (240, 220, 200)},
    {"name": "Speed Test", "ball_speed": 8, "platform_width": 110, "platform_speed": 13, "ball_count": 1, "background_color": (240, 200, 200)},
    {"name": "Platform Master", "ball_speed": 8, "platform_width": 100, "platform_speed": 14, "ball_count": 2, "background_color": (240, 200, 240)},
    {"name": "Ball Storm", "ball_speed": 9, "platform_width": 100, "platform_speed": 14, "ball_count": 3, "background_color": (220, 200, 240)},
    {"name": "Speed Chaos", "ball_speed": 10, "platform_width": 90, "platform_speed": 15, "ball_count": 2, "background_color": (200, 200, 240)},
    {"name": "Maximum Focus", "ball_speed": 11, "platform_width": 80, "platform_speed": 16, "ball_count": 3, "background_color": (200, 180, 240)},
    {"name": "Ball Master", "ball_speed": 12, "platform_width": 70, "platform_speed": 17, "ball_count": 4, "background_color": (180, 180, 220)}
]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(f'Catch the Ball - 10 Levels of Challenge [{SCREEN_WIDTH}x{SCREEN_HEIGHT}]')
clock = pygame.time.Clock()

current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(current_dir, 'assets', 'images')

current_level = 0
level_data = LEVELS[current_level]
level_progress = 0
level_target = 10

ball_radius = 25
balls = []
speed_increase = 0.1
max_speed_x = 15
max_speed_y = 15

platform_width = level_data["platform_width"]
platform_height = 20
platform_x = SCREEN_WIDTH // 2 - platform_width // 2
platform_y = SCREEN_HEIGHT - 50
platform_speed = level_data["platform_speed"]

score = 0
lives = 3
bounce_count = 0
total_bounces = 0
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)
big_font = pygame.font.Font(None, 72)

menu_button_width = 100
menu_button_height = 30
menu_button_x = SCREEN_WIDTH - menu_button_width - 20
menu_button_y = 20
menu_button_rect = pygame.Rect(menu_button_x, menu_button_y, menu_button_width, menu_button_height)

class Ball:
    def __init__(self, level_speed):
        self.radius = random.randint(20, 30)
        self.x = random.randint(self.radius, SCREEN_WIDTH - self.radius)
        self.y = self.radius + 10
        self.speed_x = random.choice([-level_speed/2, -level_speed/3, level_speed/3, level_speed/2])
        self.speed_y = level_speed
        self.color = random.choice([RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE])
        self.point_value = max(1, 30 // self.radius)
        self.image = self.create_ball_image()
    
    def create_ball_image(self):
        surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        
        for r in range(self.radius, 0, -1):
            alpha = 255 if r > self.radius * 0.9 else int(255 * (r / self.radius))
            color = (
                min(255, self.color[0] + (255 - self.color[0]) * (1 - r / self.radius)),
                min(255, self.color[1] + (255 - self.color[1]) * (1 - r / self.radius)),
                min(255, self.color[2] + (255 - self.color[2]) * (1 - r / self.radius)),
                alpha
            )
            pygame.draw.circle(surface, color, (self.radius, self.radius), r)
        
        highlight_radius = int(self.radius * 0.4)
        highlight_pos = (int(self.radius * 0.7), int(self.radius * 0.7))
        for r in range(highlight_radius, 0, -1):
            alpha = 150 * (1 - r / highlight_radius)
            pygame.draw.circle(
                surface, 
                (255, 255, 255, int(alpha)), 
                highlight_pos, 
                r
            )
        
        return surface
    
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
        if self.x <= self.radius or self.x >= SCREEN_WIDTH - self.radius:
            self.speed_x = -self.speed_x
        
        if self.y <= self.radius:
            self.speed_y = -self.speed_y
    
    def draw(self):
        screen.blit(self.image, (self.x - self.radius, self.y - self.radius))
    
    def check_collision(self, platform_x, platform_y, platform_width, platform_height):
        if (platform_x - self.radius < self.x < platform_x + platform_width + self.radius and 
            platform_y - self.radius < self.y < platform_y + platform_height//2):
            hit_pos = (self.x - platform_x) / platform_width
            angle_factor = hit_pos * 2 - 1
            
            self.speed_y = -abs(self.speed_y) - speed_increase
            self.speed_x = angle_factor * (5 + abs(self.speed_y) / 2)
            
            if abs(self.speed_x) > max_speed_x:
                self.speed_x = max_speed_x * (1 if self.speed_x > 0 else -1)
            if abs(self.speed_y) > max_speed_y:
                self.speed_y = -max_speed_y
                
            return True
        return False
    
    def is_out_of_bounds(self):
        return self.y > SCREEN_HEIGHT + self.radius

def draw_menu_button():
    pygame.draw.rect(screen, (150, 150, 150), menu_button_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, menu_button_rect, 2, border_radius=10)
    menu_text = small_font.render("Menu", True, BLACK)
    screen.blit(menu_text, (menu_button_x + menu_button_width//2 - menu_text.get_width()//2, 
                           menu_button_y + menu_button_height//2 - menu_text.get_height()//2))

def check_menu_button(mouse_pos):
    return menu_button_rect.collidepoint(mouse_pos)

def return_to_menu():
    pygame.quit()
    import subprocess
    subprocess.Popen([sys.executable, "launcher.py"])
    sys.exit()

def load_svg_as_surface(filename, width, height):
    try:
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        if "ball" in filename:
            pygame.draw.circle(surface, (255, 0, 0), (width//2, height//2), width//2-2)
            pygame.draw.circle(surface, (255, 200, 200), (width//3, height//3), width//6)
        elif "platform" in filename:
            pygame.draw.rect(surface, (0, 100, 255), (0, 0, width, height), border_radius=height//4)
            pygame.draw.rect(surface, (100, 150, 255), (2, 2, width-4, height//4), border_radius=height//8)
        elif "background" in filename:
            for y in range(height):
                color_value = 255 - int(y * 100 / height)
                color = (200, 220, color_value)
                pygame.draw.line(surface, color, (0, y), (width, y))
        
        return surface
    except Exception as e:
        print(f"Error creating surface for {filename}: {e}")
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        if "ball" in filename:
            pygame.draw.circle(surface, RED, (width//2, height//2), width//2-2)
        elif "platform" in filename:
            pygame.draw.rect(surface, BLUE, (0, 0, width, height), border_radius=height//4)
        return surface

background_images = {}
platform_img = load_svg_as_surface(os.path.join(assets_dir, 'platform.svg'), platform_width, platform_height)

def create_level_background(level_idx):
    level = LEVELS[level_idx]
    bg_color = level["background_color"]
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    for y in range(SCREEN_HEIGHT):
        factor = 1 - (y / SCREEN_HEIGHT * 0.5)
        color = (
            int(bg_color[0] * factor),
            int(bg_color[1] * factor),
            int(bg_color[2] * factor)
        )
        pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))
    
    for _ in range(50):
        size = random.randint(5, 20)
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        alpha = random.randint(10, 60)
        bubble = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(bubble, (*WHITE, alpha), (size//2, size//2), size//2)
        surface.blit(bubble, (x, y))
    
    level_text = big_font.render(f"LEVEL {level_idx + 1}", True, (*WHITE, 120))
    surface.blit(level_text, (SCREEN_WIDTH//2 - level_text.get_width()//2, SCREEN_HEIGHT//2 - level_text.get_height()//2))
    
    return surface

for i in range(len(LEVELS)):
    background_images[i] = create_level_background(i)

def show_game_ui():
    score_text = font.render(f'Score: {score}', True, BLACK)
    lives_text = small_font.render(f'Lives: {lives}', True, BLACK)
    level_text = small_font.render(f'Level {current_level + 1}: {LEVELS[current_level]["name"]}', True, BLACK)
    bounces_text = small_font.render(f'Progress: {bounce_count}/{level_target}', True, BLACK)
    ball_speed = 0 if not balls else abs(balls[0].speed_y)
    speed_text = small_font.render(f'Speed: {ball_speed:.1f}', True, BLACK)
    controls_text = small_font.render(f'Controls: Arrows/WASD', True, BLACK)
    
    progress_width = 200
    progress_height = 15
    progress_x = SCREEN_WIDTH // 2 - progress_width // 2
    progress_y = 20
    progress_fill = int((bounce_count / level_target) * progress_width)
    
    pygame.draw.rect(screen, (50, 50, 50), (progress_x, progress_y, progress_width, progress_height), border_radius=7)
    if progress_fill > 0:
        pygame.draw.rect(screen, (0, 200, 0), (progress_x, progress_y, progress_fill, progress_height), border_radius=7)
    pygame.draw.rect(screen, BLACK, (progress_x, progress_y, progress_width, progress_height), 2, border_radius=7)
    
    screen.blit(score_text, (20, 20))
    screen.blit(level_text, (20, 60))
    screen.blit(lives_text, (SCREEN_WIDTH - 150, 60))
    screen.blit(bounces_text, (20, 100))
    screen.blit(speed_text, (20, 140))
    screen.blit(controls_text, (SCREEN_WIDTH - 250, 100))

def reset_platform():
    global platform_width, platform_x, platform_speed
    platform_width = LEVELS[current_level]["platform_width"]
    platform_x = SCREEN_WIDTH // 2 - platform_width // 2
    platform_speed = LEVELS[current_level]["platform_speed"]
    return load_svg_as_surface(os.path.join(assets_dir, 'platform.svg'), platform_width, platform_height)

def start_level(level_idx):
    global current_level, level_data, balls, bounce_count, level_progress, platform_img
    
    current_level = level_idx
    level_data = LEVELS[current_level]
    bounce_count = 0
    level_progress = 0
    balls = []
    
    for _ in range(level_data["ball_count"]):
        balls.append(Ball(level_data["ball_speed"]))
    
    platform_img = reset_platform()
    
    screen.blit(background_images[current_level], (0, 0))
    
    level_title = big_font.render(f"Level {current_level + 1}", True, BLACK)
    level_name = font.render(LEVELS[current_level]["name"], True, BLACK)
    
    screen.blit(level_title, (SCREEN_WIDTH//2 - level_title.get_width()//2, SCREEN_HEIGHT//2 - 100))
    screen.blit(level_name, (SCREEN_WIDTH//2 - level_name.get_width()//2, SCREEN_HEIGHT//2))
    
    prompt_text = font.render("Press SPACE to start", True, BLACK)
    screen.blit(prompt_text, (SCREEN_WIDTH//2 - prompt_text.get_width()//2, SCREEN_HEIGHT//2 + 100))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == KEY_ESCAPE:
                    return_to_menu()
                if event.key == KEY_SPACE:
                    waiting = False
                if event.key == KEY_M or event.unicode == 'm' or event.unicode == 'м' or event.unicode == 'M' or event.unicode == 'М':
                    return_to_menu()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if check_menu_button(event.pos):
                        return_to_menu()

def show_level_complete():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    complete_text = big_font.render('LEVEL COMPLETE!', True, WHITE)
    level_text = font.render(f'Level {current_level + 1}: {LEVELS[current_level]["name"]}', True, WHITE)
    score_text = font.render(f'Current Score: {score}', True, WHITE)
    next_text = font.render('Press SPACE for next level', True, WHITE)
    
    screen.blit(complete_text, (SCREEN_WIDTH // 2 - complete_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
    screen.blit(next_text, (SCREEN_WIDTH // 2 - next_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == KEY_ESCAPE:
                    return_to_menu()
                if event.key == KEY_SPACE:
                    waiting = False
                if event.key == KEY_M or event.unicode == 'm' or event.unicode == 'м' or event.unicode == 'M' or event.unicode == 'М':
                    return_to_menu()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if check_menu_button(event.pos):
                        return_to_menu()

def show_game_complete():
    global score, lives, current_level, total_bounces
    
    screen.fill(BLACK)
    
    for i in range(100):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        size = random.randint(1, 5)
        pygame.draw.circle(screen, WHITE, (x, y), size)
    
    congrats_text = big_font.render('CONGRATULATIONS!', True, WHITE)
    complete_text = font.render('You have completed all 10 levels!', True, WHITE)
    score_text = big_font.render(f'Final Score: {score}', True, YELLOW)
    retry_text = font.render('Press SPACE to play again', True, WHITE)
    menu_text = font.render('Press M to return to menu', True, WHITE)
    
    screen.blit(congrats_text, (SCREEN_WIDTH // 2 - congrats_text.get_width() // 2, SCREEN_HEIGHT // 2 - 150))
    screen.blit(complete_text, (SCREEN_WIDTH // 2 - complete_text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80))
    screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 2 + 120))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == KEY_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == KEY_SPACE:
                    score = 0
                    lives = 3
                    current_level = 0
                    total_bounces = 0
                    start_level(0)
                    waiting = False
                if event.key == KEY_M or event.unicode == 'm' or event.unicode == 'м' or event.unicode == 'M' or event.unicode == 'М':
                    return_to_menu()

def game_over():
    global score, lives, total_bounces
    
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    game_over_text = big_font.render('GAME OVER', True, RED)
    final_score_text = font.render(f'Final Score: {score}', True, WHITE)
    level_text = font.render(f'Level Reached: {current_level + 1}', True, WHITE)
    retry_text = font.render('Press SPACE to retry', True, WHITE)
    menu_text = font.render('Press M to return to menu', True, WHITE)
    quit_text = font.render('Press ESC to quit', True, WHITE)
    
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 150))
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
    screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
    screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))
    screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 140))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == KEY_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == KEY_SPACE:
                    score = 0
                    lives = 3
                    total_bounces = 0
                    start_level(0)
                    waiting = False
                if event.key == KEY_M or event.unicode == 'm' or event.unicode == 'м' or event.unicode == 'M' or event.unicode == 'М':
                    return_to_menu()

if __name__ == "__main__":
    start_level(0)

    running = True

    move_left = False
    move_right = False

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == KEY_ESCAPE:
                    running = False
                elif event.key == KEY_M or event.unicode == 'm' or event.unicode == 'м' or event.unicode == 'M' or event.unicode == 'М':
                    return_to_menu()
                elif event.key == KEY_LEFT or event.unicode == 'a' or event.unicode == 'A' or event.unicode == 'ф' or event.unicode == 'Ф':
                    move_left = True
                elif event.key == KEY_RIGHT or event.unicode == 'd' or event.unicode == 'D' or event.unicode == 'в' or event.unicode == 'В':
                    move_right = True
            elif event.type == KEYUP:
                if event.key == KEY_LEFT or (event.key > 0 and event.unicode in ('a', 'A', 'ф', 'Ф')):
                    move_left = False
                if event.key == KEY_RIGHT or (event.key > 0 and event.unicode in ('d', 'D', 'в', 'В')):
                    move_right = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if check_menu_button(event.pos):
                        return_to_menu()

        if move_left and platform_x > 0:
            platform_x -= platform_speed
        if move_right and platform_x < SCREEN_WIDTH - platform_width:
            platform_x += platform_speed
        
        balls_to_remove = []
        for ball in balls:
            ball.update()
            
            if ball.check_collision(platform_x, platform_y, platform_width, platform_height):
                bounce_count += 1
                total_bounces += 1
                score += ball.point_value
                
                if bounce_count >= level_target:
                    if current_level < len(LEVELS) - 1:
                        show_level_complete()
                        current_level += 1
                        start_level(current_level)
                    else:
                        show_game_complete()
            
            if ball.is_out_of_bounds():
                balls_to_remove.append(ball)
        
        for ball in balls_to_remove:
            balls.remove(ball)
            lives -= 1
            
            if len(balls) == 0 and lives > 0:
                for _ in range(level_data["ball_count"]):
                    balls.append(Ball(level_data["ball_speed"]))
        
        if lives <= 0:
            game_over()
        
        screen.blit(background_images[current_level], (0, 0))
        
        screen.blit(platform_img, (platform_x, platform_y))
        
        for ball in balls:
            ball.draw()
        
        show_game_ui()
        draw_menu_button()
        
        pygame.display.update()
        
        clock.tick(FPS)

pygame.quit()
sys.exit() 