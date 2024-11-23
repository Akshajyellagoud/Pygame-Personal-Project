import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 64)

# Title and Icon
pygame.display.set_caption("Space Invaders")

# Player
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - 80
player_speed = 6

# Enemy
enemy_size = 40
enemy_count = 6
enemies = [{"x": random.randint(0, WIDTH - enemy_size),
            "y": random.randint(50, 150),
            "dx": random.choice([-3, 3]),
            "dy": 20} for _ in range(enemy_count)]

# Bullet
bullet_width, bullet_height = 5, 20
bullet_x, bullet_y = None, None
bullet_speed = 8
bullet_state = "ready"  # "ready" -> bullet is hidden, "fire" -> bullet is moving

# Score
score = 0

def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, player_size, player_size))

def draw_enemy(x, y):
    pygame.draw.ellipse(screen, RED, (x, y, enemy_size, enemy_size))

def fire_bullet(x, y):
    pygame.draw.rect(screen, YELLOW, (x, y, bullet_width, bullet_height))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x + enemy_size // 2 - bullet_x) ** 2 +
                         (enemy_y + enemy_size // 2 - bullet_y) ** 2)
    return distance < 25

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed
    if keys[pygame.K_SPACE] and bullet_state == "ready":
        bullet_x, bullet_y = player_x + player_size // 2, player_y
        bullet_state = "fire"

    # Enemy Movement
    for enemy in enemies:
        enemy["x"] += enemy["dx"]
        if enemy["x"] <= 0 or enemy["x"] >= WIDTH - enemy_size:
            enemy["dx"] *= -1
            enemy["y"] += enemy["dy"]

        # Collision Detection
        if bullet_state == "fire" and is_collision(enemy["x"], enemy["y"], bullet_x, bullet_y):
            bullet_state = "ready"
            bullet_y = None
            enemy["x"], enemy["y"] = random.randint(0, WIDTH - enemy_size), random.randint(50, 150)
            score += 1

        # Game Over Condition
        if enemy["y"] > HEIGHT - 120:
            screen.fill(RED)
            game_over_text = big_font.render("GAME OVER", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
            pygame.display.update()
            pygame.time.delay(3000)
            running = False

        draw_enemy(enemy["x"], enemy["y"])

    # Bullet Movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_speed
        if bullet_y < 0:
            bullet_state = "ready"

    # Draw Player
    draw_player(player_x, player_y)

    # Score Display
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update Display
    pygame.display.update()
    clock.tick(60)

pygame.quit()
