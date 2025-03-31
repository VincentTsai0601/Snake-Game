import pygame
import random
import math
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (30, 30, 30)
SNAKE_COLOR = (0, 255, 0)
FOOD_COLORS = {
    "apple": (255, 0, 0),  # Normal growth
    "burger": (200, 100, 50),  # Makes snake fatter
    "chili": (255, 50, 0)  # Speed boost
}
OBSTACLE_COLOR = (150, 150, 150)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics-Based Snake Game")
clock = pygame.time.Clock()

script_dir = os.path.dirname(os.path.abspath(__file__))
# Load sounds
eat_sound = pygame.mixer.Sound(os.path.join(script_dir, "Sounds/eat.wav"))
crash_sound = pygame.mixer.Sound(os.path.join(script_dir, "Sounds/crash.wav"))

# Snake properties
snake = [(WIDTH // 2, HEIGHT // 2)]  # Start position

snake_radius = 10
velocity = 2  # Default velocity
max_speed = 6
angle = 0  # Initial angle of movement (0 means moving right)
score = 0

# Food properties
food_list = []
def spawn_food():
    food_type = random.choice(list(FOOD_COLORS.keys()))
    food_x = random.randint(50, WIDTH - 50)
    food_y = random.randint(50, HEIGHT - 50)
    food_list.append((food_x, food_y, food_type))

for _ in range(3):
    spawn_food()

# Obstacles
obstacles = [(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100), 30) for _ in range(5)]

# Special Effects
font = pygame.font.Font(None, 36)
def draw_effect(text, pos, color=(255, 255, 255)):
    effect_surface = font.render(text, True, color)
    screen.blit(effect_surface, pos)

# Game loop
running = True
game_over = False
while running:
    screen.fill(BG_COLOR)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            # Restart the game
            snake = [(WIDTH // 2, HEIGHT // 2)]
            velocity = 2  # Reset velocity to default
            snake_radius = 10
            angle = 0
            score = 0
            food_list.clear()
            for _ in range(3):
                spawn_food()
            game_over = False
    
    if not game_over:
        # Control movement (only left and right)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            angle -= 5  # Turn left
        if keys[pygame.K_RIGHT]:
            angle += 5  # Turn right

        # Move the snake forward continuously
        dx = math.cos(math.radians(angle)) * velocity
        dy = math.sin(math.radians(angle)) * velocity
        new_head = (snake[0][0] + dx, snake[0][1] + dy)
        
        # Screen wrapping
        new_head = (new_head[0] % WIDTH, new_head[1] % HEIGHT)
        
        snake.insert(0, new_head)
        if len(snake) > 50:
            snake.pop()
        
        # Check collision with food
        for food in food_list[:]:
            fx, fy, ftype = food
            if math.hypot(new_head[0] - fx, new_head[1] - fy) < snake_radius * 2:
                food_list.remove(food)
                spawn_food()
                eat_sound.play()
                score += 10
                if ftype == "burger":
                    snake_radius += 2  # Make snake fatter
                    draw_effect("Bigger!", (fx, fy))
                elif ftype == "chili":
                    velocity = min(max_speed, velocity + 2)  # Speed boost
                    draw_effect("Speed Up!", (fx, fy), (255, 50, 50))
        
        # Check collision with obstacles
        for ox, oy, orad in obstacles:
            if math.hypot(new_head[0] - ox, new_head[1] - oy) < snake_radius + orad:
                draw_effect("Ouch!", (ox, oy), (255, 255, 0))
                crash_sound.play()
                game_over = True
        
        # Draw snake
        for segment in snake:
            pygame.draw.circle(screen, SNAKE_COLOR, (int(segment[0]), int(segment[1])), snake_radius)
        
        # Draw food
        for food in food_list:
            pygame.draw.circle(screen, FOOD_COLORS[food[2]], (food[0], food[1]), 8)
        
        # Draw obstacles
        for ox, oy, orad in obstacles:
            pygame.draw.circle(screen, OBSTACLE_COLOR, (ox, oy), orad)
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
    else:
        screen.fill((0, 0, 0))
        text = font.render("Game Over! Press ESC to exit", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
