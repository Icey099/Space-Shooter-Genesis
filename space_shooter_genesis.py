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
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (10, 10, 30)
# =====================
# Player
# =====================
PLAYER_SPEED = 3
PLAYER_HIT_RADIUS = 50
PLAYER_MAX_HEALTH = 100
PLAYER_DAMAGE = 10
PLAYER_GUN_OFFSET = 40

PLAYER_HEALTH_BAR_WIDTH = 55
PLAYER_HEALTH_BAR_HEIGHT = 4
PLAYER_HEALTH_BAR_COLOR = (0, 220, 0)
HEALTH_BAR_OFFSET = 45

# =====================
# Enemy
# =====================
ENEMY_HIT_RADIUS = 25
ENEMY_COUNT = 5

ENEMY_DAMAGE = 10
PLAYER_BULLET_DAMAGE = 10
ENEMY_HEALTH_BAR_WIDTH = 35
ENEMY_HEALTH_BAR_HEIGHT = 3
ENEMY_HEALTH_BAR_COLOR = (220, 40, 40)

SCOUT = {
    "health": 15,
    "speed": 1.0,
    "can_shoot": False,
    "offset": 22
}

FIGHTER = {
    "health": 30,
    "speed": 0.67,
    "can_shoot": True,
    "offset": 28
}

TANK = {
    "health": 70,
    "speed": 0.25,
    "can_shoot": True,
    "offset": 35
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
pygame.display.set_caption("Space Shooter: Genesis")
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

pygame.mixer.music.load("Assets/Sounds/bgm.mp3")
pygame.mixer.music.set_volume(0.2)
# =====================
# Sprites
# =====================
player_ship = pygame.image.load("Assets/Images/player.png").convert_alpha()
player_ship = pygame.transform.scale(player_ship, (80, 80))

scout_ship = pygame.image.load("Assets/Images/scout.png").convert_alpha()
scout_ship = pygame.transform.scale(scout_ship, (75, 75))

fighter_ship = pygame.image.load("Assets/Images/fighter.png").convert_alpha()
fighter_ship = pygame.transform.scale(fighter_ship, (70, 70))

tank_ship = pygame.image.load("Assets/Images/tank.png").convert_alpha()
tank_ship = pygame.transform.scale(tank_ship, (80, 80))

player_bullet = pygame.image.load("Assets/Images/player_bullet.png").convert_alpha()
player_bullet = pygame.transform.scale(player_bullet, (48, 48))

enemy_bullet = pygame.image.load("Assets/Images/enemy_bullet.png").convert_alpha()
enemy_bullet = pygame.transform.scale(enemy_bullet, (32, 32))

background = pygame.image.load("Assets/Images/background.png").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
# =====================
# Game Objects
# =====================
bullets = []
enemy_bullets = []
enemies = []
particles = []
score = 0
high_score = 0
spawn_timer = 0
confirm_quit = False
quit_selection = 0

in_menu = True
# =====================
# Functions
# =====================
def draw_menu():
    screen.blit(background, (0, 0))

    title = pygame.font.SysFont(None, 72).render(
        "SPACE SHOOTER: GENESIS",
        True,
        (255, 255, 255),
    )

    start = font.render(
        "Press Enter to Start",
        True,
        (255, 220, 0),
    )

    quit_game = font.render(
        "Press Esc to Quit",
        True,
        (180, 180, 180),
    )

    controls = font.render(
        "Move: WASD/Arrow Keys  Aim: Mouse  Shoot: Left Click",
        True,
        (200, 200, 200),
    )

    screen.blit(
        title,
        (SCREEN_WIDTH // 2 - title.get_width() // 2,
        120,
        )
    )

    screen.blit(
        start,
        (SCREEN_WIDTH // 2 - start.get_width() // 2,
        260
        )
    )

    screen.blit(
        quit_game,
        (SCREEN_WIDTH // 2 - quit_game.get_width() // 2,
        310
        )
    )

    screen.blit(
        controls,
        (SCREEN_WIDTH // 2 - controls.get_width() // 2,
        450
        )
    )

    pygame.display.update()

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

        angle = bullet[2] + math.pi + random.uniform(-0.20, 0.20)
        particles.append({
            "x": bullet[0],
            "y": bullet[1],
            "dx": math.cos(angle) * random.uniform(0.5, 2),
            "dy": math.sin(angle) * random.uniform(0.5, 2),
            "radius": random.uniform(1, 2),
            "life": 8,
            "color": (180, 230, 255),
        })

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
                    create_explosion_particles(enemy["x"], enemy["y"])
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

        angle = bullet[2] + math.pi + random.uniform(-0.20, 0.20)
        particles.append({
            "x": bullet[0],
            "y": bullet[1],
            "dx": math.cos(angle) * random.uniform(0.5, 2),
            "dy": math.sin(angle) * random.uniform(0.5, 2),
            "radius": random.uniform(1, 2),
            "life": 8,
            "color": (255, 70, 70),
        })

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
                pygame.mixer.music.stop()
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

def create_explosion_particles(x, y):
    for _ in range(20):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(2, 6)

        particles.append({
            "x": x,
            "y": y,
            "dx": math.cos(angle) * speed,
            "dy": math.sin(angle) * speed,
            "radius": random.randint(2, 5),
            "life": 30,
            "color": (
                random.randint(220, 255),
                random.randint(100, 220),
                0,
            ),
        })

def create_engine_particles():
    angle = player_angle + math.pi + random.uniform(-0.2, 0.2)

    x = player_x + math.cos(angle) * 35
    y = player_y + math.sin(angle) * 35

    particles.append({
            "x": x,
            "y": y,
            "dx": math.cos(angle) * random.uniform(2, 4),
            "dy": math.sin(angle) * random.uniform(2, 4),
            "radius": random.uniform(1.5, 3),
            "life": 15,
            "color": random.choice([
                (180, 255, 255),
                (120, 220, 255),
                (70, 150, 255),
            ]),
        })
    
def update_particles():
    for particle in particles[:]:
        particle["x"] += particle["dx"]
        particle["y"] += particle["dy"]

        particle["radius"] -= 0.08
        particle["life"] -= 1

        if particle["life"] <= 0 or particle["radius"] < 1:
            particles.remove(particle)

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
            create_explosion_particles(enemy["x"], enemy["y"])
            player_health -= PLAYER_DAMAGE

            if player_health <= 0:
                global high_score

                if score > high_score:
                    high_score = score
                game_over = True
                pygame.mixer.music.stop()
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
    screen.blit(background, (0, 0))

    rotated_player = pygame.transform.rotate(
        player_ship,
        -math.degrees(player_angle) - 90
    )
    rect = rotated_player.get_rect(center=(player_x, player_y))
    screen.blit(rotated_player, rect)

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
        if enemy["type"] == SCOUT:
            enemy_ship = scout_ship
        elif enemy["type"] == FIGHTER:
            enemy_ship = fighter_ship
        else:
            enemy_ship = tank_ship

        rotated_enemy = pygame.transform.rotate(
            enemy_ship,
            -math.degrees(enemy["angle"]) - 90
        )

        rect = rotated_enemy.get_rect(center=(enemy["x"], enemy["y"]))
        screen.blit(rotated_enemy, rect)

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
        rotated_player_bullet = pygame.transform.rotate(
            player_bullet,
            -math.degrees(bullet[2])
        )
        rect = rotated_player_bullet.get_rect(
            center=(bullet[0], bullet[1])
        )

        screen.blit(rotated_player_bullet, rect)
        
    for bullet in enemy_bullets:
        rotated_enemy_bullet = pygame.transform.rotate(
            enemy_bullet,
            -math.degrees(bullet[2]) + 180
        )
        rect = rotated_enemy_bullet.get_rect(
            center=(bullet[0], bullet[1])
        )

        screen.blit(rotated_enemy_bullet, rect)

    for particle in particles:
            pygame.draw.circle(
                screen,
                particle["color"],
                (int(particle["x"]), int(particle["y"])),
                int(particle["radius"]),
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

    tip_x = player_x + math.cos(player_angle) * PLAYER_GUN_OFFSET
    tip_y = player_y + math.sin(player_angle) * PLAYER_GUN_OFFSET
    
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

        tip_x = enemy["x"] + math.cos(enemy["angle"]) * enemy["type"]["offset"]
        tip_y = enemy["y"] + math.sin(enemy["angle"]) * enemy["type"]["offset"]

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
    pygame.mixer.music.play(-1)


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
# Game Loop
# =====================

running = True
while running:
    if in_menu:
        draw_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running == False
            
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    in_menu = False
                    reset_game()

                elif event.key == pygame.K_ESCAPE:
                    running = False

        clock.tick(60)
        continue

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

    create_engine_particles()
    
    handle_shooting() 

    handle_enemy_shooting()   

    update_bullets()

    update_enemy_bullets()

    update_particles()

    update_enemies()

    draw()

    pygame.display.update()
    clock.tick(60)
    
pygame.quit()