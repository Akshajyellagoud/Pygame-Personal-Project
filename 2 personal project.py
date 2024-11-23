import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

# Clock and initial speed
clock = pygame.time.Clock()
speed = 10

# Snake settings
snake_block = 20
snake = [(WIDTH // 2, HEIGHT // 2)]  # Initial snake body
snake_dir = "RIGHT"  # Initial direction
snake_dx, snake_dy = snake_block, 0

# Food
food_x = random.randrange(0, WIDTH - snake_block, snake_block)
food_y = random.randrange(0, HEIGHT - snake_block, snake_block)

# Special Food
special_food_x, special_food_y = None, None
special_food_timer = 0

# Score
score = 0
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Wall Collision Mode
wall_collision_enabled = True

# Game States
game_running = False
game_over_state = False

def draw_snake(snake):
    for block in snake:
        pygame.draw.rect(screen, GREEN, (block[0], block[1], snake_block, snake_block))

def draw_food(x, y, color=RED):
    pygame.draw.rect(screen, color, (x, y, snake_block, snake_block))

def display_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def display_wall_mode(enabled):
    mode_text = font.render(f"Wall Collision: {'ON' if enabled else 'OFF'}", True, WHITE)
    screen.blit(mode_text, (WIDTH - 200, 10))

def spawn_special_food():
    return random.randrange(0, WIDTH - snake_block, snake_block), random.randrange(0, HEIGHT - snake_block, snake_block)

def draw_button(text, x, y, w, h, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    pygame.draw.rect(screen, hover_color if x < mouse[0] < x + w and y < mouse[1] < y + h else color, (x, y, w, h))
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (x + (w - text_surface.get_width()) // 2, y + (h - text_surface.get_height()) // 2))
    if click[0] == 1 and action is not None and x < mouse[0] < x + w and y < mouse[1] < y + h:
        action()

def reset_game():
    global snake, snake_dir, snake_dx, snake_dy, food_x, food_y, special_food_x, special_food_y, special_food_timer, score, game_running, game_over_state
    snake = [(WIDTH // 2, HEIGHT // 2)]
    snake_dir = "RIGHT"
    snake_dx, snake_dy = snake_block, 0
    food_x = random.randrange(0, WIDTH - snake_block, snake_block)
    food_y = random.randrange(0, HEIGHT - snake_block, snake_block)
    special_food_x, special_food_y = None, None
    special_food_timer = 0
    score = 0
    game_running = True
    game_over_state = False

def show_start_screen():
    global game_running
    while not game_running:
        screen.fill(BLACK)
        title_text = large_font.render("Snake Game", True, GREEN)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        draw_button("Start Game", WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, GRAY, WHITE, reset_game)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def show_game_over_screen():
    global game_over_state
    while game_over_state:
        screen.fill(BLACK)
        game_over_text = large_font.render("Game Over", True, RED)
        final_score = font.render(f"Score: {score}", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
        screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2))
        draw_button("Restart", WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, GRAY, WHITE, reset_game)
        draw_button("Quit", WIDTH // 2 - 100, HEIGHT // 2 + 170, 200, 50, GRAY, WHITE, pygame.quit)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

# Start screen
show_start_screen()

# Main game loop
while True:
    while game_running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Movement controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and snake_dy == 0:
            snake_dx, snake_dy = 0, -snake_block
        if keys[pygame.K_s] and snake_dy == 0:
            snake_dx, snake_dy = 0, snake_block
        if keys[pygame.K_a] and snake_dx == 0:
            snake_dx, snake_dy = -snake_block, 0
        if keys[pygame.K_d] and snake_dx == 0:
            snake_dx, snake_dy = snake_block, 0
        if keys[pygame.K_c]:  # Toggle wall collision mode
            wall_collision_enabled = not wall_collision_enabled

        # Move snake
        head_x = snake[0][0] + snake_dx
        head_y = snake[0][1] + snake_dy

        # Wall collision handling
        if wall_collision_enabled:
            if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
                game_running = False
                game_over_state = True
                break
        else:
            head_x %= WIDTH
            head_y %= HEIGHT

        # Update snake's position
        new_head = (head_x, head_y)
        if new_head in snake:
            game_running = False
            game_over_state = True
            break
        snake = [new_head] + snake[:-1]

        # Collision with food
        if head_x == food_x and head_y == food_y:
            score += 1
            snake.append(snake[-1])
            food_x = random.randrange(0, WIDTH - snake_block, snake_block)
            food_y = random.randrange(0, HEIGHT - snake_block, snake_block)

        # Collision with special food
        if special_food_x is not None and head_x == special_food_x and head_y == special_food_y:
            score += 5
            snake.append(snake[-1])
            special_food_x, special_food_y = None, None

        # Special food spawning logic
        if special_food_timer == 0 and random.randint(0, 100) < 10:
            special_food_x, special_food_y = spawn_special_food()
            special_food_timer = 300

        if special_food_timer > 0:
            special_food_timer -= 1
            if special_food_timer == 0:
                special_food_x, special_food_y = None, None

        # Draw everything
        draw_snake(snake)
        draw_food(food_x, food_y)
        if special_food_x is not None:
            draw_food(special_food_x, special_food_y, BLUE)
        display_score(score)
        display_wall_mode(wall_collision_enabled)

        # Update display and control frame rate
        pygame.display.update()
        clock.tick(speed + score // 5)

    # Show Game Over screen
    show_game_over_screen()
