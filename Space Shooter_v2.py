# =====================
# Imports
# =====================
import math
import pygame
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
# =====================
# Enemy
# =====================
ENEMY_COLOR = (255, 70, 70)
ENEMY_SPEED = 2
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
# =====================
# Game Objects
# =====================
player_x = 100
player_y = 100
bullets = []
enemies = [
    {"x": 600, "y": 200, "angle": 0},
    {"x": 300, "y": 450, "angle": 0},
]
last_shot = 0
# =====================
# Functions
# =====================
def draw_ship(screen, x, y, angle, color):
    tip = (
        x + math.cos(angle) * PLAYER_HEIGHT,
        y + math.sin(angle) * PLAYER_HEIGHT,
    )
    left = (
        x + math.cos(angle + math.radians(140)) * PLAYER_HALF_BASE,
        y + math.sin(angle + math.radians(140)) * PLAYER_HALF_BASE,
    )
    right = (
        x + math.cos(angle - math.radians(140)) * PLAYER_HALF_BASE,
        y + math.sin(angle - math.radians(140)) * PLAYER_HALF_BASE,
    )
    pygame.draw.polygon(screen, color, [tip, left, right])
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
    # Fire
    buttons = pygame.mouse.get_pressed()
    current_time = pygame.time.get_ticks()
    tip_x = player_x + math.cos(player_angle) * PLAYER_HEIGHT
    tip_y = player_y + math.sin(player_angle) * PLAYER_HEIGHT
    if buttons[0]:
        if current_time - last_shot >= FIRE_DELAY:
            bullets.append([tip_x, tip_y, player_angle])
            last_shot = current_time
    # Update bullets
    for bullet in bullets[:]:
        bullet[0] += math.cos(bullet[2]) * BULLET_SPEED
        bullet[1] += math.sin(bullet[2]) * BULLET_SPEED
        if (
            bullet[0] < 0
            or bullet[0] > SCREEN_WIDTH
            or bullet[1] < 0
            or bullet[1] > SCREEN_HEIGHT
        ):
            bullets.remove(bullet)
    # Rotate enemies toward player
    for enemy in enemies:
        enemy["angle"] = math.atan2(
            player_y - enemy["y"],
            player_x - enemy["x"],
        )
    # Draw
    screen.fill(BACKGROUND_COLOR)
    draw_ship(
        screen,
        player_x,
        player_y,
        player_angle,
        PLAYER_COLOR,
    )
    for enemy in enemies:
        draw_ship(
            screen,
            enemy["x"],
            enemy["y"],
            enemy["angle"],
            ENEMY_COLOR,
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
    pygame.display.update()
    clock.tick(60)
pygame.quit()