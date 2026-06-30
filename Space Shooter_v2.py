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
PLAYER_MAX_HEALTH = 100
PLAYER_DAMAGE = 10

PLAYER_HEALTH_BAR_WIDTH = 55
PLAYER_HEALTH_BAR_HEIGHT = 4
PLAYER_HEALTH_BAR_COLOR = (0, 220, 0)
HEALTH_BAR_OFFSET = 45

# =====================
# Enemy
# =====================
ENEMY_HALF_BASE = 25
ENEMY_HEIGHT = 40
ENEMY_COLOR = (255, 70, 70)
ENEMY_SPEED = 1
ENEMY_HIT_RADIUS = 25
ENEMY_COUNT = 5

ENEMY_MAX_HEALTH = 30
ENEMY_DAMAGE = 10
PLAYER_BULLET_DAMAGE = 10
ENEMY_HEALTH_BAR_WIDTH = 35
ENEMY_HEALTH_BAR_HEIGHT = 3
ENEMY_HEALTH_BAR_COLOR = (220, 40, 40)
# =====================
# Bullets
# =====================
BULLET_SPEED = 12
BULLET_RADIUS = 4
BULLET_COLOR = (255, 255, 255)
FIRE_DELAY = 150
ENEMY_FIRE_DELAY = 1500

ENEMY_BULLET_SPEED = 6
ENEMY_BULLET_RADIUS = 2
ENEMY_BULLET_COLOR = (255, 170, 0)
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

def draw_health_bar(screen, x, y, health, max_health, width, height, color):
    pygame.draw.rect(
        screen,
        (60, 60, 60),
        (
            x - width // 2,
            y + HEALTH_BAR_OFFSET,
            width,
            height,
        ),
        border_radius=3,
    )

    current_width = (
        health / max_health
    ) * width

    pygame.draw.rect(
        screen,
        color,
        (
            x - width // 2,
            y + HEALTH_BAR_OFFSET,
            current_width,
            height,
        ),
        border_radius=3,
    )

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
        "health": ENEMY_MAX_HEALTH,
        "last_shot": pygame.time.get_ticks() - random.randint(0, ENEMY_FIRE_DELAY)
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

                enemy["health"] -= PLAYER_BULLET_DAMAGE

                if enemy["health"] <= 0:
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

def update_enemy_bullets():
    global player_health, game_over, high_score

    for bullet in enemy_bullets[:]:
        bullet[0] += math.cos(bullet[2]) * ENEMY_BULLET_SPEED
        bullet[1] += math.sin(bullet[2]) * ENEMY_BULLET_SPEED

        dx = bullet[0] - player_x
        dy = bullet[1] - player_y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < PLAYER_HIT_RADIUS:
            enemy_bullets.remove(bullet)

            player_health -= ENEMY_DAMAGE

            if player_health <= 0:
                if score > high_score:
                    high_score = score
                game_over = True

        if (
            bullet[0] < 0
            or bullet[0] > SCREEN_WIDTH
            or bullet[1] < 0
            or bullet[1] > SCREEN_HEIGHT
        ):
            enemy_bullets.remove(bullet)    

            continue

def update_enemies():
    global player_health, game_over
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
            player_health -= PLAYER_DAMAGE

            if player_health <= 0:
                global high_score

                if score > high_score:
                    high_score = score
                game_over = True
            enemies.remove(enemy)
            break

    while len(enemies) < ENEMY_COUNT:
        enemies.append(spawn_enemy())

def draw():
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

    draw_health_bar(
        screen,
        player_x,
        player_y,
        player_health,
        PLAYER_MAX_HEALTH,
        PLAYER_HEALTH_BAR_WIDTH,
        PLAYER_HEALTH_BAR_HEIGHT,
        PLAYER_HEALTH_BAR_COLOR,
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

        draw_health_bar(
            screen,
            enemy["x"],
            enemy["y"],
            enemy["health"],
            ENEMY_MAX_HEALTH,
            ENEMY_HEALTH_BAR_WIDTH,
            ENEMY_HEALTH_BAR_HEIGHT,
            ENEMY_HEALTH_BAR_COLOR,
        )

    for bullet in bullets:
        pygame.draw.circle(
            screen,
            BULLET_COLOR,
            (int(bullet[0]), int(bullet[1])),
            BULLET_RADIUS,
        )

    for bullet in enemy_bullets:
        pygame.draw.circle(
            screen,
            ENEMY_BULLET_COLOR,
            (int(bullet[0]), int(bullet[1])),
            ENEMY_BULLET_RADIUS,
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


def handle_shooting():
    global last_shot

    buttons = pygame.mouse.get_pressed()
    current_time = pygame.time.get_ticks()

    tip_x = player_x + math.cos(player_angle) * PLAYER_HEIGHT
    tip_y = player_y + math.sin(player_angle) * PLAYER_HEIGHT
    
    if buttons[0]:
        if current_time - last_shot >= FIRE_DELAY:
            bullets.append([tip_x, tip_y, player_angle])
            last_shot = current_time

def handle_enemy_shooting():
    current_time = pygame.time.get_ticks()

    for enemy in enemies:
        tip_x = enemy["x"] + math.cos(enemy["angle"]) * ENEMY_HEIGHT
        tip_y = enemy["y"] + math.sin(enemy["angle"]) * ENEMY_HEIGHT

        if current_time - enemy["last_shot"] >= ENEMY_FIRE_DELAY:
            enemy_bullets.append([
                tip_x,
                tip_y,
                enemy["angle"],
            ])

            enemy["last_shot"] = current_time
            

def reset_game():
    global player_x, player_y
    global player_health, score
    global bullets, enemies, enemy_bullets
    global game_over
    global last_shot


    player_x = SCREEN_WIDTH // 2
    player_y = SCREEN_HEIGHT // 2

    player_health = PLAYER_MAX_HEALTH

    score = 0

    bullets.clear()
    enemy_bullets.clear()

    enemies.clear()
    for _ in range(ENEMY_COUNT):
        enemies.append(spawn_enemy())    

    last_shot = 0
    game_over = False

def draw_game_over():
    screen.fill((0, 0, 0))

    pygame.draw.line(
        screen,
        (80, 80, 80),
        (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 45),
        (SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT // 2 - 45),
        2,
    )

    game_over_text = font.render(
        "GAME OVER",
        True,
        (255, 70, 70),
    )

    score_text = font.render(
        f"Score: {score}",
        True,
        (255, 255, 255),
    )

    high_score_text = font.render(
        f"High Score: {high_score}",
        True,
        (255, 215, 0)
    )

    replay_text = font.render(
        "Press Space to Replay",
        True,
        (180, 180, 180),
    )

    screen.blit(
        game_over_text,
        (
            SCREEN_WIDTH // 2 - game_over_text.get_width() //2,
            SCREEN_HEIGHT // 2 - 80,
        ),
    )

    screen.blit(
        replay_text,
        (
            SCREEN_WIDTH // 2 - replay_text.get_width() // 2,
            SCREEN_HEIGHT // 2 - 20,
        ),
    )

    screen.blit(
        score_text,
        (
            SCREEN_WIDTH // 2 - score_text.get_width() // 2,
            SCREEN_HEIGHT // 2 + 40,
        ),
    )

    screen.blit(
        high_score_text,
        (
            SCREEN_WIDTH // 2 - high_score_text.get_width() // 2,
            SCREEN_HEIGHT // 2 + 90,
        ),
    )

    pygame.display.update()
# =====================
# Game Objects
# =====================
bullets = []
enemy_bullets = []
enemies = []
score = 0
high_score = 0
reset_game()
# =====================
# Game Loop
# =====================

running = True
while running:
    if game_over:
        draw_game_over()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()

        clock.tick(60)
        continue

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
    
    handle_shooting() 

    handle_enemy_shooting()   

    update_bullets()

    update_enemy_bullets()

    update_enemies()

    draw()

    pygame.display.update()
    clock.tick(60)
    
pygame.quit()