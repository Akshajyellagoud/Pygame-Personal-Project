import pygame
import random
import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Driving Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Car settings
car_width = 40
car_height = 80
player_x = WIDTH // 2 - car_width // 2
player_y = HEIGHT - 150
player_speed = 10
lane_width = 200

# Obstacles and fuel
obstacles = []
fuel_pickups = []
obstacle_width = 50
obstacle_height = 80
fuel_width = 30
fuel_height = 30
obstacle_speed = 5

# Game variables
lane_positions = [WIDTH // 4 - lane_width // 2, WIDTH // 2 - lane_width // 2, 3 * WIDTH // 4 - lane_width // 2]
player_lane = 1
fuel = 100
distance = 0
score = 0
game_running = True
paused = False

# Helper functions
def draw_road():
    """Draws the road and lane markings."""
    screen.fill(GRAY)
    pygame.draw.rect(screen, BLACK, (WIDTH // 4, 0, lane_width * 2, HEIGHT))  # Road
    for i in range(0, HEIGHT, 40):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, i, 10, 20))  # Lane markings

def draw_car(x, y, color=BLUE):
    """Draws the player's car."""
    pygame.draw.rect(screen, color, (x, y, car_width, car_height))

def draw_obstacle(x, y):
    """Draws an obstacle."""
    pygame.draw.rect(screen, RED, (x, y, obstacle_width, obstacle_height))

def draw_fuel(x, y):
    """Draws a fuel pickup."""
    pygame.draw.rect(screen, GREEN, (x, y, fuel_width, fuel_height))

def draw_hud(fuel, distance, score):
    """Displays the fuel, distance, and score."""
    fuel_text = font.render(f"Fuel: {fuel}%", True, WHITE)
    distance_text = font.render(f"Distance: {distance} m", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(fuel_text, (10, 10))
    screen.blit(distance_text, (10, 40))
    screen.blit(score_text, (10, 70))

def spawn_obstacle():
    """Spawns a new obstacle."""
    lane = random.choice(lane_positions)
    obstacles.append([lane + lane_width // 2 - obstacle_width // 2, -obstacle_height])

def spawn_fuel():
    """Spawns a new fuel pickup."""
    lane = random.choice(lane_positions)
    fuel_pickups.append([lane + lane_width // 2 - fuel_width // 2, -fuel_height])

def handle_collision(player_rect):
    """Handles collisions with obstacles and fuel pickups."""
    global fuel, score, game_running

    # Check for collisions with obstacles
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height)
        if player_rect.colliderect(obstacle_rect):
            game_running = False
            return

    # Check for collisions with fuel pickups
    for fuel_pickup in fuel_pickups[:]:
        fuel_rect = pygame.Rect(fuel_pickup[0], fuel_pickup[1], fuel_width, fuel_height)
        if player_rect.colliderect(fuel_rect):
            fuel = min(100, fuel + 20)
            score += 10
            fuel_pickups.remove(fuel_pickup)

def show_game_over():
    """Displays the Game Over screen."""
    screen.fill(BLACK)
    game_over_text = large_font.render("GAME OVER", True, RED)
    final_score = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 1.5))
    pygame.display.update()

# Main game loop
while True:
    if not game_running:
        show_game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart
                    # Reset game variables
                    player_x = WIDTH // 2 - car_width // 2
                    player_y = HEIGHT - 150
                    fuel = 100
                    distance = 0
                    score = 0
                    obstacles = []
                    fuel_pickups = []
                    obstacle_speed = 5
                    game_running = True
                elif event.key == pygame.K_q:  # Quit
                    pygame.quit()
                    exit()

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and player_lane > 0:
                    player_lane -= 1
                if event.key == pygame.K_RIGHT and player_lane < 2:
                    player_lane += 1
                if event.key == pygame.K_p:
                    paused = not paused

        if paused:
            continue

        # Update player position
        player_x = lane_positions[player_lane] + lane_width // 2 - car_width // 2

        # Move obstacles
        obstacles = [[x, y + obstacle_speed] for x, y in obstacles if y < HEIGHT]
        fuel_pickups = [[x, y + obstacle_speed] for x, y in fuel_pickups if y < HEIGHT]

        # Spawn new obstacles and fuel pickups
        if random.randint(0, 100) < 2:
            spawn_obstacle()
        if random.randint(0, 100) < 1:
            spawn_fuel()

        # Update distance and fuel
        distance += 1
        fuel -= 0.1
        if fuel <= 0:
            game_running = False

        # Check for collisions
        player_rect = pygame.Rect(player_x, player_y, car_width, car_height)
        handle_collision(player_rect)

        # Speed up obstacles over time
        if distance % 100 == 0:
            obstacle_speed += 0.1

        # Draw everything
        draw_road()
        draw_car(player_x, player_y)
        for obstacle in obstacles:
            draw_obstacle(*obstacle)
        for fuel_pickup in fuel_pickups:
            draw_fuel(*fuel_pickup)
        draw_hud(int(fuel), distance, score)

        # Update display and tick
        pygame.display.update()
        clock.tick(FPS)

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Driving Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_GRAY = (30, 30, 30)

# Clock and font
clock = pygame.time.Clock()
FPS = 60
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Car settings
car_width = 40
car_height = 80
player_x = WIDTH // 2 - car_width // 2
player_y = HEIGHT - 150
player_speed = 10
lane_width = 200

# Lanes and road
lane_positions = [WIDTH // 4 - lane_width // 2, WIDTH // 2 - lane_width // 2, 3 * WIDTH // 4 - lane_width // 2]
player_lane = 1
target_lane = 1
lane_change_speed = 5

# Obstacles and fuel
obstacles = []
fuel_pickups = []
boost_pickups = []
obstacle_width = 50
obstacle_height = 80
fuel_width = 30
fuel_height = 30
boost_width = 40
boost_height = 40
obstacle_speed = 5

# Game variables
fuel = 100
distance = 0
score = 0
boost_active = False
boost_timer = 0
game_running = True
paused = False
rain_effect = False

# Weather effects
rain_drops = []


def draw_road():
    """Draws the road and lane markings."""
    screen.fill(DARK_GRAY if rain_effect else GRAY)
    pygame.draw.rect(screen, BLACK, (WIDTH // 4, 0, lane_width * 2, HEIGHT))
    for i in range(0, HEIGHT, 40):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, i, 10, 20))  # Lane markings


def draw_car(x, y, color=BLUE):
    """Draws the player's car."""
    pygame.draw.rect(screen, color, (x, y, car_width, car_height))


def draw_obstacle(x, y):
    """Draws an obstacle."""
    pygame.draw.rect(screen, RED, (x, y, obstacle_width, obstacle_height))


def draw_fuel(x, y):
    """Draws a fuel pickup."""
    pygame.draw.rect(screen, GREEN, (x, y, fuel_width, fuel_height))


def draw_boost(x, y):
    """Draws a boost pickup."""
    pygame.draw.rect(screen, YELLOW, (x, y, boost_width, boost_height))


def draw_hud(fuel, distance, score, boost_timer):
    """Displays the HUD elements."""
    fuel_text = font.render(f"Fuel: {fuel}%", True, WHITE)
    distance_text = font.render(f"Distance: {distance} m", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    boost_text = font.render(f"Boost: {'Active' if boost_active else 'Inactive'}", True, YELLOW if boost_active else WHITE)
    screen.blit(fuel_text, (10, 10))
    screen.blit(distance_text, (10, 40))
    screen.blit(score_text, (10, 70))
    if boost_timer > 0:
        boost_remaining = font.render(f"Boost Time: {boost_timer // FPS}s", True, YELLOW)
        screen.blit(boost_remaining, (WIDTH - 200, 10))
    screen.blit(boost_text, (WIDTH - 200, 40))


def handle_collision(player_rect):
    """Handles collisions with obstacles, fuel, and boosts."""
    global fuel, score, boost_active, boost_timer, game_running

    # Check collisions with obstacles
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height)
        if player_rect.colliderect(obstacle_rect):
            game_running = False
            return

    # Check collisions with fuel
    for fuel_pickup in fuel_pickups[:]:
        fuel_rect = pygame.Rect(fuel_pickup[0], fuel_pickup[1], fuel_width, fuel_height)
        if player_rect.colliderect(fuel_rect):
            fuel = min(100, fuel + 20)
            score += 10
            fuel_pickups.remove(fuel_pickup)

    # Check collisions with boosts
    for boost_pickup in boost_pickups[:]:
        boost_rect = pygame.Rect(boost_pickup[0], boost_pickup[1], boost_width, boost_height)
        if player_rect.colliderect(boost_rect):
            boost_active = True
            boost_timer = FPS * 5  # 5 seconds of boost
            score += 20
            boost_pickups.remove(boost_pickup)


def spawn_obstacle():
    """Spawns a new obstacle."""
    lane = random.choice(lane_positions)
    obstacles.append([lane + lane_width // 2 - obstacle_width // 2, -obstacle_height])


def spawn_fuel():
    """Spawns a new fuel pickup."""
    lane = random.choice(lane_positions)
    fuel_pickups.append([lane + lane_width // 2 - fuel_width // 2, -fuel_height])


def spawn_boost():
    """Spawns a boost pickup."""
    lane = random.choice(lane_positions)
    boost_pickups.append([lane + lane_width // 2 - boost_width // 2, -boost_height])


def draw_rain():
    """Draws falling rain."""
    for drop in rain_drops:
        pygame.draw.line(screen, WHITE, (drop[0], drop[1]), (drop[0], drop[1] + 10), 1)
    for i in range(len(rain_drops)):
        rain_drops[i][1] += 10
        if rain_drops[i][1] > HEIGHT:
            rain_drops[i][1] = -10
            rain_drops[i][0] = random.randint(0, WIDTH)


# ... Additional code for updates continues ...
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultimate Driving Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_GRAY = (30, 30, 30)
DAY_SKY = (135, 206, 250)
NIGHT_SKY = (25, 25, 112)

# Clock and font
clock = pygame.time.Clock()
FPS = 60
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Game variables
car_width = 40
car_height = 80
player_x = WIDTH // 2 - car_width // 2
player_y = HEIGHT - 150
lane_width = 200
lane_positions = [WIDTH // 4 - lane_width // 2, WIDTH // 2 - lane_width // 2, 3 * WIDTH // 4 - lane_width // 2]
target_lane = 1
lane_change_speed = 5

# Obstacles and collectibles
obstacles = []
fuel_pickups = []
boost_pickups = []
hazards = []
obstacle_width = 50
obstacle_height = 80
fuel_width = 30
fuel_height = 30
boost_width = 40
boost_height = 40
hazard_width = 60
hazard_height = 60

# Difficulty and progress
obstacle_speed = 5
fuel = 100
distance = 0
score = 0
boost_active = False
boost_timer = 0
day_cycle_time = 0
difficulty_timer = 0

# Misc
leaderboard = []
game_running = False
player_color = BLUE
rain_effect = False
rain_drops = []

# Sounds
collision_sound = pygame.mixer.Sound("collision.wav")
pickup_sound = pygame.mixer.Sound("pickup.wav")
boost_sound = pygame.mixer.Sound("boost.wav")


def draw_road():
    """Draws the road and lane markings."""
    time_of_day = (day_cycle_time % (FPS * 60)) / (FPS * 60)  # Cycle every 60 seconds
    sky_color = [DAY_SKY[i] + (NIGHT_SKY[i] - DAY_SKY[i]) * time_of_day for i in range(3)]
    screen.fill(sky_color)
    pygame.draw.rect(screen, BLACK, (WIDTH // 4, 0, lane_width * 2, HEIGHT))
    for i in range(0, HEIGHT, 40):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, i, 10, 20))  # Lane markings


def draw_car(x, y, color):
    """Draws the player's car."""
    pygame.draw.rect(screen, color, (x, y, car_width, car_height))


def draw_obstacle(x, y):
    """Draws an obstacle."""
    pygame.draw.rect(screen, RED, (x, y, obstacle_width, obstacle_height))


def draw_fuel(x, y):
    """Draws a fuel pickup."""
    pygame.draw.rect(screen, GREEN, (x, y, fuel_width, fuel_height))


def draw_boost(x, y):
    """Draws a boost pickup."""
    pygame.draw.rect(screen, YELLOW, (x, y, boost_width, boost_height))


def draw_hazard(x, y):
    """Draws a hazard (e.g., oil spill)."""
    pygame.draw.rect(screen, DARK_GRAY, (x, y, hazard_width, hazard_height))


def draw_hud(fuel, distance, score, boost_timer):
    """Displays the HUD elements."""
    fuel_text = font.render(f"Fuel: {fuel}%", True, WHITE)
    distance_text = font.render(f"Distance: {distance} m", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    leaderboard_text = font.render(f"High Score: {max(leaderboard) if leaderboard else 0}", True, WHITE)
    screen.blit(fuel_text, (10, 10))
    screen.blit(distance_text, (10, 40))
    screen.blit(score_text, (10, 70))
    screen.blit(leaderboard_text, (10, 100))
    if boost_timer > 0:
        boost_remaining = font.render(f"Boost Time: {boost_timer // FPS}s", True, YELLOW)
        screen.blit(boost_remaining, (WIDTH - 200, 10))


def handle_collision(player_rect):
    """Handles collisions with obstacles, fuel, boosts, and hazards."""
    global fuel, score, boost_active, boost_timer, game_running

    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height)
        if player_rect.colliderect(obstacle_rect):
            collision_sound.play()
            game_running = False

    for fuel_pickup in fuel_pickups[:]:
        fuel_rect = pygame.Rect(fuel_pickup[0], fuel_pickup[1], fuel_width, fuel_height)
        if player_rect.colliderect(fuel_rect):
            pickup_sound.play()
            fuel = min(100, fuel + 20)
            score += 10
            fuel_pickups.remove(fuel_pickup)

    for boost_pickup in boost_pickups[:]:
        boost_rect = pygame.Rect(boost_pickup[0], boost_pickup[1], boost_width, boost_height)
        if player_rect.colliderect(boost_rect):
            boost_sound.play()
            boost_active = True
            boost_timer = FPS * 5  # 5 seconds of boost
            score += 20
            boost_pickups.remove(boost_pickup)

    for hazard in hazards[:]:
        hazard_rect = pygame.Rect(hazard[0], hazard[1], hazard_width, hazard_height)
        if player_rect.colliderect(hazard_rect):
            score -= 10  # Penalty for hitting hazard
            hazards.remove(hazard)


def spawn_obstacle():
    """Spawns a new obstacle."""
    lane = random.choice(lane_positions)
    obstacles.append([lane + lane_width // 2 - obstacle_width // 2, -obstacle_height])


def spawn_fuel():
    """Spawns a new fuel pickup."""
    lane = random.choice(lane_positions)
    fuel_pickups.append([lane + lane_width // 2 - fuel_width // 2, -fuel_height])


def spawn_boost():
    """Spawns a boost pickup."""
    lane = random.choice(lane_positions)
    boost_pickups.append([lane + lane_width // 2 - boost_width // 2, -boost_height])


def spawn_hazard():
    """Spawns a new hazard."""
    lane = random.choice(lane_positions)
    hazards.append([lane + lane_width // 2 - hazard_width // 2, -hazard_height])


def reset_game():
    """Resets the game to the initial state."""
    global obstacles, fuel_pickups, boost_pickups, hazards, obstacle_speed, fuel, distance, score, boost_active, boost_timer, game_running
    obstacles = []
    fuel_pickups = []
    boost_pickups = []
    hazards = []
    obstacle_speed = 5
    fuel = 100
    distance = 0
    score = 0
    boost_active = False
    boost_timer = 0
    game_running = True