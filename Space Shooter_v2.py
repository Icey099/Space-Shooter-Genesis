# =====================
# Imports
# =====================
import math
import pygame
import random

pygame.init()
pygame.mixer.init()
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

SCOUT = {
    "health": 15,
    "speed": 1.0,
    "half_base": 20,
    "height": 32,
    "color": (255, 180, 80),
    "can_shoot": False,
}

FIGHTER = {
    "health": 30,
    "speed": 0.67,
    "half_base": 25,
    "height": 40,
    "color": (255, 70, 70),
    "can_shoot": True,
}

TANK = {
    "health": 70,
    "speed": 0.25,
    "half_base": 35,
    "height": 55,
    "color": (180, 60, 255),
    "can_shoot": True,
}


SPAWN_DELAY = 500
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
# Sounds
# =====================
laser_sound = pygame.mixer.Sound("Assets/Sounds/laser.mp3")
explosion_sound = pygame.mixer.Sound("Assets/Sounds/explosion.mp3")
enemy_laser_sound = pygame.mixer.Sound("Assets/Sounds/enemy_laser.mp3")
player_hit_sound = pygame.mixer.Sound("Assets/Sounds/player_hit.wav")
game_over_sound = pygame.mixer.Sound("Assets/Sounds/game_over.mp3")

laser_sound.set_volume(0.1)
explosion_sound.set_volume(0.15)
enemy_laser_sound.set_volume(0.1)
player_hit_sound.set_volume(0.15)
game_over_sound.set_volume(1.0)
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

def spawn_enemy(enemy_type):
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
        "type": enemy_type,
        "health": enemy_type["health"],
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
    global score, spawn_timer

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
                    explosion_sound.play()
                    enemies.remove(enemy) 
                    score += 1
                    spawn_timer = pygame.time.get_ticks()
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

        hit = False
        if distance < PLAYER_HIT_RADIUS:
            player_hit_sound.play()
            enemy_bullets.remove(bullet)

            player_health -= ENEMY_DAMAGE

            if player_health <= 0:
                if score > high_score:
                    high_score = score
                game_over = True
                game_over_sound.play()
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
            enemy_bullets.remove(bullet)    

            continue

def get_enemy_type(scout_count, fighter_count, tank_count):
    if score < 10:
        return SCOUT
    
    elif score < 25:
        if scout_count < 4:
            return SCOUT
        return FIGHTER
    
    elif score < 50:
        if scout_count < 3:
            return SCOUT
        return FIGHTER
    
    else:
        if scout_count < 3:
            return SCOUT
        if fighter_count < 1:
            return FIGHTER
        return TANK

def update_enemies():
    global player_health, game_over, spawn_timer

    scout_count = 0
    fighter_count = 0
    tank_count = 0

    for enemy in enemies:
        if enemy["type"] == SCOUT:
            scout_count += 1
        elif enemy["type"] == FIGHTER:
            fighter_count += 1
        else:
            tank_count +=1

    for enemy in enemies[:]:
        angle = math.atan2(
            player_y - enemy["y"],
            player_x - enemy["x"],
        )

        if enemy["type"] == SCOUT:
            angle += math.radians(35)
        
        enemy["angle"] = angle

        
        enemy["x"] += math.cos(enemy["angle"]) * enemy["type"]["speed"]
        enemy["y"] += math.sin(enemy["angle"]) * enemy["type"]["speed"]

        dx = player_x - enemy["x"]
        dy = player_y - enemy["y"]
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < (PLAYER_HIT_RADIUS + ENEMY_HIT_RADIUS):
            player_hit_sound.play()
            explosion_sound.play()
            player_health -= PLAYER_DAMAGE

            if player_health <= 0:
                global high_score

                if score > high_score:
                    high_score = score
                game_over = True
                game_over_sound.play()
            enemies.remove(enemy)
            break

    current_time = pygame.time.get_ticks()

    if len(enemies) < ENEMY_COUNT:
        if current_time - spawn_timer >= SPAWN_DELAY:

            enemy_type = get_enemy_type(
                scout_count, 
                fighter_count,
                tank_count,
            )

            enemies.append(spawn_enemy(enemy_type))

            spawn_timer = current_time


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
            enemy["type"]["color"],
            enemy["type"]["half_base"],
            enemy["type"]["height"]
        )

        draw_health_bar(
            screen,
            enemy["x"],
            enemy["y"],
            enemy["health"],
            enemy["type"]["health"],
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
            laser_sound.play()
            last_shot = current_time

def handle_enemy_shooting():
    current_time = pygame.time.get_ticks()

    for enemy in enemies:

        if not enemy["type"]["can_shoot"]:
            continue

        tip_x = enemy["x"] + math.cos(enemy["angle"]) * enemy["type"]["height"]
        tip_y = enemy["y"] + math.sin(enemy["angle"]) * enemy["type"]["height"]

        if current_time - enemy["last_shot"] >= ENEMY_FIRE_DELAY:
            enemy_bullets.append([
                tip_x,
                tip_y,
                enemy["angle"],
            ])
            enemy_laser_sound.play()

            enemy["last_shot"] = current_time
            

def reset_game():
    global player_x, player_y
    global player_health, score
    global bullets, enemies, enemy_bullets
    global game_over, spawn_timer
    global last_shot
    global confirm_quit, quit_selection


    player_x = SCREEN_WIDTH // 2
    player_y = SCREEN_HEIGHT // 2

    player_health = PLAYER_MAX_HEALTH

    score = 0

    bullets.clear()
    enemy_bullets.clear()

    spawn_timer = pygame.time.get_ticks()
    enemies.clear()
    for _ in range(ENEMY_COUNT):
        enemies.append(spawn_enemy((SCOUT)))

    last_shot = 0
    game_over = False

    confirm_quit = False
    quit_selection = 0

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

    quit_text = font.render(
        "Press ESC to Quit",
        True,
        (180, 180, 180)
    )

    screen.blit(
        game_over_text,
        (
            SCREEN_WIDTH // 2 - game_over_text.get_width() //2,
            SCREEN_HEIGHT // 2 - 80,
        ),
    )

    screen.blit(
        score_text,
        (
            SCREEN_WIDTH // 2 - score_text.get_width() // 2,
            SCREEN_HEIGHT // 2 - 20,
        ),
    )

    screen.blit(
        high_score_text,
        (
            SCREEN_WIDTH // 2 - high_score_text.get_width() // 2,
            SCREEN_HEIGHT // 2 + 30,
        ),
    )

    screen.blit(
        replay_text,
        (
            SCREEN_WIDTH // 2 - replay_text.get_width() // 2,
            SCREEN_HEIGHT // 2 + 90,
        ),
    )

    screen.blit(
        quit_text,
        (
        SCREEN_WIDTH // 2 - quit_text.get_width() // 2,
        SCREEN_HEIGHT // 2 + 130,
        ),
    )


    if confirm_quit:
        draw_quit_confirmation()

    pygame.display.update()

def draw_quit_confirmation():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(170)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    box = pygame.Rect(190, 170 , 450, 220)

    pygame.draw.rect(screen, (35, 35, 50), box, border_radius=12)
    pygame.draw.rect(screen, (170, 170, 170), box, 2, border_radius=12)

    title = font.render("Quit Game?", True, (255, 90, 90))
    screen.blit(
        title,
        (
        box.centerx - title.get_width() // 2,
        box.top + 35,
        ),
        )

    if quit_selection == 0:
        no = font.render("[ No ]", True, (255, 230, 0))
        yes = font.render("Yes", True, (180, 180, 180))
    else:
        no = font.render("No", True, (180, 180, 180))
        yes = font.render("[ Yes ]", True, (255, 230, 0))

    button_y = box.bottom - 70
    spacing = 80

    total_width = no.get_width() + spacing + yes.get_width()

    start_x = box.centerx - total_width // 2

    screen.blit(no, (start_x, button_y))
    screen.blit(yes, (start_x + no.get_width() + spacing, button_y))
# =====================
# Game Objects
# =====================
bullets = []
enemy_bullets = []
enemies = []
score = 0
high_score = 0
spawn_timer = 0
confirm_quit = False
quit_selection = 0
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
                if not confirm_quit:

                    if event.key == pygame.K_SPACE:
                        reset_game()

                    elif event.key == pygame.K_ESCAPE:
                        confirm_quit = True
                        quit_selection = 0

                else:
                    if event.key in (pygame.K_a, pygame.K_LEFT):
                        quit_selection = 0
                    elif event.key in (pygame.K_d, pygame.K_RIGHT):
                        quit_selection = 1

                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):

                        if quit_selection == 1:
                            running = False
                        else:
                            confirm_quit = False
                    
                    elif event.key == pygame.K_ESCAPE:
                        confirm_quit = False
                    

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