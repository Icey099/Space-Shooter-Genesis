# =====================
# Imports
# =====================
import math
import pygame
import random

pygame.init()
pygame.mouse.set_visible(False)
# =====================
# Screen
# =====================
SCREEN_WIDTH = 832
SCREEN_HEIGHT = 624
BACKGROUND_COLOR = (10, 10, 30)
# =====================
# Player
# =====================
PLAYER_SPEED = 3
PLAYER_HALF_BASE = 40
PLAYER_HEIGHT = 60
PLAYER_COLOR = (108, 180, 219)
PLAYER_HIT_RADIUS = 50
# =====================
# Enemy
# =====================
ENEMY_HALF_BASE = 25
ENEMY_HEIGHT = 40
ENEMY_COLOR = (255, 70, 70)
ENEMY_SPEED = 1
ENEMY_HIT_RADIUS = 25
ENEMY_COUNT = 5
# =====================
# Bullets
# =====================
BULLET_SPEED = 8
BULLET_RADIUS = 4
BULLET_COLOR = (255, 255, 255)
FIRE_DELAY = 150
# =====================
# Window
# =====================
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My First Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
# =====================
# Functions
# =====================
def draw_ship(screen, x, y, angle, color, half_base, height):
    tip = (
        x + math.cos(angle) * height,
        y + math.sin(angle) * height,
    )
    left = (
        x + math.cos(angle + math.radians(140)) * half_base,
        y + math.sin(angle + math.radians(140)) * half_base,
    )
    right = (
        x + math.cos(angle - math.radians(140)) * half_base,
        y + math.sin(angle - math.radians(140)) * half_base,
    )
    pygame.draw.polygon(screen, color, [tip, left, right])

def spawn_enemy():
    side = random.randint(0, 3)

    if side == 0:
        x = random.randint(0, SCREEN_WIDTH)
        y = -50

    elif side == 1:
        x = random.randint(0, SCREEN_WIDTH)
        y = SCREEN_HEIGHT + 50

    elif side == 2:
        x = -50
        y = random.randint(0, SCREEN_HEIGHT)

    else:
        x = SCREEN_WIDTH + 50
        y = random.randint(0, SCREEN_HEIGHT)

    return {
        "x": x,
        "y": y,
        "angle": 0,
    }

def handle_input():
    global player_x, player_y
    # Keyboard
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_x += PLAYER_SPEED
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_y -= PLAYER_SPEED
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_y += PLAYER_SPEED
    # Boundaries
    player_x = max(0, min(player_x, SCREEN_WIDTH))
    player_y = max(0, min(player_y, SCREEN_HEIGHT))

def update_bullets():
    global score

        # Update bullets
    for bullet in bullets[:]:
        bullet[0] += math.cos(bullet[2]) * BULLET_SPEED
        bullet[1] += math.sin(bullet[2]) * BULLET_SPEED

        hit = False

        for enemy in enemies[:]:
            dx = bullet[0] - enemy["x"]
            dy = bullet[1] - enemy["y"]

            distance = math.sqrt(dx * dx + dy * dy)

            if distance < ENEMY_HIT_RADIUS:
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                hit = True
                break

        if hit:
            continue

        if (
            bullet[0] < 0
            or bullet[0] > SCREEN_WIDTH
            or bullet[1] < 0
            or bullet[1] > SCREEN_HEIGHT
        ):
            bullets.remove(bullet)

def update_enemies():
    for enemy in enemies[:]:
        enemy["angle"] = math.atan2(
            player_y - enemy["y"],
            player_x - enemy["x"],
        )
        enemy["x"] += math.cos(enemy["angle"]) * ENEMY_SPEED
        enemy["y"] += math.sin(enemy["angle"]) * ENEMY_SPEED

        dx = player_x - enemy["x"]
        dy = player_y - enemy["y"]
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < (PLAYER_HIT_RADIUS + ENEMY_HIT_RADIUS):
            enemies.remove(enemy)
            break

    while len(enemies) < ENEMY_COUNT:
        enemies.append(spawn_enemy())

def draw():
       # Draw
    screen.fill(BACKGROUND_COLOR)

    draw_ship(
        screen,
        player_x,
        player_y,
        player_angle,
        PLAYER_COLOR,
        PLAYER_HALF_BASE,
        PLAYER_HEIGHT
    )

    for enemy in enemies:
        draw_ship(
            screen,
            enemy["x"],
            enemy["y"],
            enemy["angle"],
            ENEMY_COLOR,
            ENEMY_HALF_BASE,
            ENEMY_HEIGHT
        )

    for bullet in bullets:
        pygame.draw.circle(
            screen,
            BULLET_COLOR,
            (int(bullet[0]), int(bullet[1])),
            BULLET_RADIUS,
        )

    pygame.draw.circle(
        screen,
        (255, 255, 0),
        (mouse_x, mouse_y),
        5,
    )

    #Score
    score_text = font.render(
        f"Score: {score}",
        True,
        (255, 255, 255)
    )
    screen.blit(score_text, (15, 15))

# =====================
# Game Objects
# =====================
player_x = 100
player_y = 100
bullets = []
score = 0

enemies = []
for _ in range(ENEMY_COUNT):
    enemies.append(spawn_enemy())
last_shot = 0
# =====================
# Game Loop
# =====================

running = True
while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - player_x
    dy = mouse_y - player_y
    player_angle = math.atan2(dy, dx)

    handle_input()
    
    # Fire
    buttons = pygame.mouse.get_pressed()
    current_time = pygame.time.get_ticks()
    tip_x = player_x + math.cos(player_angle) * PLAYER_HEIGHT
    tip_y = player_y + math.sin(player_angle) * PLAYER_HEIGHT
    if buttons[0]:
        if current_time - last_shot >= FIRE_DELAY:
            bullets.append([tip_x, tip_y, player_angle])
            last_shot = current_time

    update_bullets()

    update_enemies()

    draw()
    
    pygame.display.update()
    clock.tick(60)
    
pygame.quit()