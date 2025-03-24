import pygame
from sys import exit

"""
1. Add game over screen
2. Add universal (Available for all pieces) melee attack
3. Make it so that when someone dies splat.mp3 plays and 1 second later fatality.mp3
"""

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Chess Fighter")
clock = pygame.time.Clock()
font = pygame.font.Font('assets/font/pixeltype.ttf', 50)

# -------------
# MENU SETUP
# -------------
menu_surface = pygame.image.load('assets/visuals/menu.png').convert()
play_button_rect = pygame.Rect(400, 60, 140, 60)

in_menu = True
while in_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                in_menu = False

    screen.blit(menu_surface, (0, 0))
    pygame.display.update()
    clock.tick(60)

# -------------
# AUDIO SETUP
# -------------
pygame.mixer.music.load('assets/audio/epicmusic.mp3')
pygame.mixer.music.set_volume(0.3)  # Lower the music volume
pygame.mixer.music.play(-1)  # Loop indefinitely

# Load death sounds
splat_sound = pygame.mixer.Sound('assets/audio/splat.mp3')
fatality_sound = pygame.mixer.Sound('assets/audio/fatality.mp3')
fatality_sound.set_volume(100.0)  # Increase fatality volume

# -------------
# CONSTANTS
# -------------
SPEED = 15
GRAVITY = 0.5

COOLDOWN = 5000
KNIGHT_COOLDOWN = 7000
BISHOP_COOLDOWN = 2000
ROOK_COOLDOWN = 3000
QUEEN_COOLDOWN = 4000
KING_COOLDOWN = 5000

RESPAWN_TIME = 2000
SPAWN_POSITIONS = [(700, 280), (100, 280)]
MAX_HEALTH = 100
BLAST_DAMAGE = 3
BLAST_DURATION = 5000
BLAST_TICK_RATE = 100
WINDBURST_DAMAGE = 50
SLASH_DAMAGE = 34
SLASH_DURATION = 500

ROOK_PROJECTILE_SPEED = 30
ROOK_DAMAGE = 50

QUEEN_ATTACK_SPEED = 20
QUEEN_DAMAGE = 100

KING_DAMAGE = 20
KING_TINT_DURATION = 200
KILL_THRESHOLD = 8
BISHOP_THRESHOLD = 10
ROOK_THRESHOLD = BISHOP_THRESHOLD + 2   # 12
QUEEN_THRESHOLD = ROOK_THRESHOLD + 2     # 14
KING_THRESHOLD = QUEEN_THRESHOLD + 2     # 16
WINDBURST_DURATION = 200

# Universal melee constants
UNIVERSAL_MELEE_DAMAGE = 20
UNIVERSAL_MELEE_DURATION = 300  # milliseconds
UNIVERSAL_MELEE_COOLDOWN = 1000

# -------------
# PLAYER INITIALIZATIONS
# -------------
# Player 1 variables
x1, y1 = SPAWN_POSITIONS[0]
fall_speed1 = 0
on_ground1 = True
current_sprite1 = pygame.image.load('assets/visuals/pawn1.png').convert_alpha()
player1_rect = current_sprite1.get_rect(bottomright=(x1, y1))
health1 = MAX_HEALTH
kills1 = 0

# Attack flags for transformation-specific moves
blast1_active = False
blast1_end_time = 0
blast1_damage_timer = 0
respawn1_active = False
respawn1_timer = 0
windburst1_active = False
windburst1_timer = 0
windburst1_applied = False
slash1_active = False
slash1_timer = 0
slash1_applied = False
slash1_rect = None
rook1_active = False
rook1_projectile_rect = None
rook_projectile_direction1 = None
rook_facing1 = None
queen_active1 = False
queen_attack_rect1 = None
queen_attack_direction1 = None
king_active1 = False
king_attack_timer1 = 0
king_tint_active1 = False
king_tint_end_time1 = 0
dev_button_down1 = False
attack_key_pressed1 = False
next_attack_time1 = 0
last_cooldown1 = 0
attack_pending_cooldown1 = False
cooldown_start_time1 = None
facing_right1 = True
delete_press_count1 = 0

# Universal melee attack for player1
universal_melee_active1 = False
universal_melee_timer1 = 0
universal_melee_applied1 = False
next_universal_melee_attack1 = 0

# Player 2 variables
x2, y2 = SPAWN_POSITIONS[1]
fall_speed2 = 0
on_ground2 = True
current_sprite2 = pygame.image.load('assets/visuals/pawn.png').convert_alpha()
player2_rect = current_sprite2.get_rect(bottomright=(x2, y2))
health2 = MAX_HEALTH
kills2 = 0

# Attack flags for transformation-specific moves
blast2_active = False
blast2_end_time = 0
blast2_damage_timer = 0
respawn2_active = False
respawn2_timer = 0
windburst2_active = False
windburst2_timer = 0
windburst2_applied = False
slash2_active = False
slash2_timer = 0
slash2_applied = False
slash2_rect = None
rook2_active = False
rook2_projectile_rect = None
rook_projectile_direction2 = None
rook_facing2 = None
queen_active2 = False
queen_attack_rect2 = None
queen_attack_direction2 = None
king_active2 = False
king_attack_timer2 = 0
king_tint_active2 = False
king_tint_end_time2 = 0
dev_button_down2 = False
attack_key_pressed2 = False
next_attack_time2 = 0
last_cooldown2 = 0
attack_pending_cooldown2 = False
cooldown_start_time2 = None
facing_right2 = False
esc_press_count2 = 0

# Universal melee attack for player2
universal_melee_active2 = False
universal_melee_timer2 = 0
universal_melee_applied2 = False
next_universal_melee_attack2 = 0

# Game over control variables
game_over = False
game_over_time = 0
fatality_played = False
winner = None

# Load all other sprites (sprite loading remains unchanged)
base_sprite1 = pygame.image.load('assets/visuals/pawn1.png').convert_alpha()
base_sprite2 = pygame.image.load('assets/visuals/pawn.png').convert_alpha()
blast_sprite = pygame.transform.scale(
    pygame.image.load('assets/visuals/blast.png').convert_alpha(), (128, 128)
)
knight_sprite1 = pygame.image.load('assets/visuals/knight1.png').convert_alpha()
knight_sprite1_flipped = pygame.transform.flip(knight_sprite1, True, False)
knight_sprite2 = pygame.image.load('assets/visuals/knight.png').convert_alpha()
knight_sprite2_flipped = pygame.transform.flip(knight_sprite2, True, False)
bishop_sprite1 = pygame.image.load('assets/visuals/bishop1.png').convert_alpha()
bishop_sprite2 = pygame.image.load('assets/visuals/bishop.png').convert_alpha()
rook_sprite = pygame.image.load('assets/visuals/rook1.png').convert_alpha()
rook_sprite_flipped = pygame.transform.flip(rook_sprite, True, False)
rook_sprite_p2 = pygame.image.load('assets/visuals/rook.png').convert_alpha()
rook_sprite_p2_flipped = pygame.transform.flip(rook_sprite_p2, True, False)
rook_projectile_img = pygame.image.load('assets/visuals/rook_projectile.png').convert_alpha()
rook_projectile_img = pygame.transform.scale(
    rook_projectile_img,
    (rook_projectile_img.get_width() // 20, rook_projectile_img.get_height() // 20)
)
slash_sprite_right = pygame.image.load('assets/visuals/slash1.png').convert_alpha()
slash_sprite_left = pygame.image.load('assets/visuals/slash.png').convert_alpha()
windburst_sprite = pygame.image.load('assets/visuals/windburst.png').convert_alpha()
queen_sprite1 = pygame.image.load('assets/visuals/queen.png').convert_alpha()
queen_sprite1_flipped = pygame.transform.flip(queen_sprite1, True, False)
queen_sprite2 = pygame.image.load('assets/visuals/queen1.png').convert_alpha()
queen_sprite2_flipped = pygame.transform.flip(queen_sprite2, True, False)
queen_wave_img = pygame.image.load('assets/visuals/queen_wave.png').convert_alpha()
queen_wave_img = pygame.transform.scale(queen_wave_img, (200, 150))
king_sprite1 = pygame.image.load('assets/visuals/king.png').convert_alpha()
king_sprite1_flipped = pygame.transform.flip(king_sprite1, True, False)
king_sprite2 = pygame.image.load('assets/visuals/king1.png').convert_alpha()
king_sprite2_flipped = pygame.transform.flip(king_sprite2, True, False)
sky_surface = pygame.image.load('assets/visuals/sky.png').convert()
ground_surface = pygame.image.load('assets/visuals/ground.png').convert()

# -------------
# MAIN GAME LOOP
# -------------
while True:
    current_time = pygame.time.get_ticks()

    # If game is over, run game over screen logic
    if game_over:
        if not fatality_played and current_time - game_over_time >= 1000:
            fatality_sound.play()
            fatality_played = True

        overlay = pygame.Surface((800, 400))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        game_over_text = font.render(f"{winner} Wins!", True, (255, 0, 0))
        prompt_text = font.render("Press any key to exit", True, (255, 255, 255))
        screen.blit(game_over_text, (250, 150))
        screen.blit(prompt_text, (150, 220))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                exit()
        clock.tick(60)
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()

    # ---------- DEV BUTTON: 10-Press Logic ----------
    if keys[pygame.K_DELETE]:
        if not dev_button_down1:
            delete_press_count1 += 1
            dev_button_down1 = True
            if delete_press_count1 >= 10:
                kills1 += 2
                delete_press_count1 = 0
    else:
        dev_button_down1 = False

    if keys[pygame.K_ESCAPE]:
        if not dev_button_down2:
            esc_press_count2 += 1
            dev_button_down2 = True
            if esc_press_count2 >= 10:
                kills2 += 2
                esc_press_count2 = 0
    else:
        dev_button_down2 = False

    # --- PLAYER 1 Controls (Arrow Keys) ---
    if not respawn1_active:
        if kills1 >= KING_THRESHOLD:
            current_sprite1 = king_sprite2 if facing_right1 else king_sprite2_flipped
        elif kills1 >= QUEEN_THRESHOLD:
            current_sprite1 = queen_sprite2 if facing_right1 else queen_sprite2_flipped
        elif kills1 >= ROOK_THRESHOLD:
            current_sprite1 = rook_sprite if (rook_facing1 if rook_facing1 is not None else facing_right1) else rook_sprite_flipped
        elif kills1 >= BISHOP_THRESHOLD:
            current_sprite1 = bishop_sprite1
        elif kills1 >= KILL_THRESHOLD:
            current_sprite1 = knight_sprite1_flipped if facing_right1 else knight_sprite1
        else:
            current_sprite1 = base_sprite1

        if keys[pygame.K_UP] and on_ground1:
            fall_speed1 = -15
            on_ground1 = False
        if keys[pygame.K_LEFT] and player1_rect.left > 0:
            x1 -= SPEED
            facing_right1 = False
        if keys[pygame.K_RIGHT] and player1_rect.right < 800:
            x1 += SPEED
            facing_right1 = True

        if keys[pygame.K_DOWN]:
            if not attack_key_pressed1 and current_time >= next_attack_time1:
                if kills1 >= KING_THRESHOLD:
                    king_active1 = True
                    king_attack_timer1 = current_time
                    if not respawn2_active:
                        health2 -= KING_DAMAGE
                        if kills2 >= KING_THRESHOLD:
                            health1 = min(health1 + KING_DAMAGE // 2, MAX_HEALTH)
                    last_cooldown1 = KING_COOLDOWN
                    attack_pending_cooldown1 = True
                    cooldown_start_time1 = None
                    king_tint_active1 = True
                    king_tint_end_time1 = current_time + KING_TINT_DURATION
                    king_active1 = False
                elif kills1 >= QUEEN_THRESHOLD:
                    if not queen_active1:
                        queen_active1 = True
                        queen_attack_rect1 = queen_wave_img.get_rect()
                        if facing_right1:
                            queen_attack_rect1.midleft = (0, y1)
                            queen_attack_direction1 = True
                        else:
                            queen_attack_rect1.midright = (800, y1)
                            queen_attack_direction1 = False
                    last_cooldown1 = QUEEN_COOLDOWN
                    attack_pending_cooldown1 = True
                    cooldown_start_time1 = None
                elif kills1 >= ROOK_THRESHOLD:
                    if not rook1_active:
                        rook1_active = True
                        rook1_projectile_rect = rook_projectile_img.get_rect(center=(x1, y1))
                        rook_projectile_direction1 = facing_right1
                        if rook_facing1 is None:
                            rook_facing1 = facing_right1
                    last_cooldown1 = ROOK_COOLDOWN
                    attack_pending_cooldown1 = True
                    cooldown_start_time1 = None
                elif kills1 >= BISHOP_THRESHOLD:
                    if not windburst1_active:
                        windburst1_active = True
                        windburst1_timer = current_time
                        windburst1_applied = False
                    last_cooldown1 = KNIGHT_COOLDOWN
                    attack_pending_cooldown1 = True
                    cooldown_start_time1 = None
                elif kills1 >= KILL_THRESHOLD:
                    if not slash1_active:
                        slash1_active = True
                        slash1_timer = current_time
                        slash1_applied = False
                        current_slash_sprite = slash_sprite_right if facing_right1 else slash_sprite_left
                        slash1_rect = current_slash_sprite.get_rect(center=(x1, y1))
                    last_cooldown1 = BISHOP_COOLDOWN
                    attack_pending_cooldown1 = True
                    cooldown_start_time1 = None
                else:
                    if not blast1_active:
                        blast1_active = True
                        blast1_end_time = current_time + BLAST_DURATION
                        blast1_damage_timer = current_time
                        current_sprite1 = blast_sprite
                    last_cooldown1 = COOLDOWN
                    attack_pending_cooldown1 = True
                    cooldown_start_time1 = None
                attack_key_pressed1 = True
        else:
            attack_key_pressed1 = False

        if keys[pygame.K_RCTRL] and current_time >= next_universal_melee_attack1:
            universal_melee_active1 = True
            universal_melee_timer1 = current_time
            universal_melee_applied1 = False
            next_universal_melee_attack1 = current_time + UNIVERSAL_MELEE_COOLDOWN

        if not on_ground1:
            fall_speed1 += GRAVITY
        y1 += fall_speed1
        if y1 >= 300:
            y1 = 300
            on_ground1 = True
            fall_speed1 = 0
        elif y1 > 280 and not on_ground1:
            y1 = 280
            on_ground1 = True
            fall_speed1 = 0

        player1_rect = current_sprite1.get_rect(center=(x1, y1))

    # --- PLAYER 2 Controls (WASD) ---
    if not respawn2_active:
        if kills2 >= KING_THRESHOLD:
            current_sprite2 = king_sprite1 if facing_right2 else king_sprite1_flipped
        elif kills2 >= QUEEN_THRESHOLD:
            current_sprite2 = queen_sprite1 if facing_right2 else queen_sprite1_flipped
        elif kills2 >= ROOK_THRESHOLD:
            current_sprite2 = rook_sprite_p2 if (rook_facing2 if rook_facing2 is not None else facing_right2) else rook_sprite_p2_flipped
        elif kills2 >= BISHOP_THRESHOLD:
            current_sprite2 = bishop_sprite2
        elif kills2 >= KILL_THRESHOLD:
            current_sprite2 = knight_sprite2_flipped if facing_right2 else knight_sprite2
        else:
            current_sprite2 = base_sprite2

        if keys[pygame.K_w] and on_ground2:
            fall_speed2 = -15
            on_ground2 = False
        if keys[pygame.K_a] and player2_rect.left > 0:
            x2 -= SPEED
            facing_right2 = False
        if keys[pygame.K_d] and player2_rect.right < 800:
            x2 += SPEED
            facing_right2 = True

        if keys[pygame.K_s]:
            if not attack_key_pressed2 and current_time >= next_attack_time2:
                if kills2 >= KING_THRESHOLD:
                    king_active2 = True
                    king_attack_timer2 = current_time
                    if not respawn1_active:
                        health1 -= KING_DAMAGE
                        if kills1 >= KING_THRESHOLD:
                            health2 = min(health2 + KING_DAMAGE // 2, MAX_HEALTH)
                    last_cooldown2 = KING_COOLDOWN
                    attack_pending_cooldown2 = True
                    cooldown_start_time2 = None
                    king_tint_active2 = True
                    king_tint_end_time2 = current_time + KING_TINT_DURATION
                    king_active2 = False
                elif kills2 >= QUEEN_THRESHOLD:
                    if not queen_active2:
                        queen_active2 = True
                        queen_attack_rect2 = queen_wave_img.get_rect()
                        if facing_right2:
                            queen_attack_rect2.midleft = (0, y2)
                            queen_attack_direction2 = True
                        else:
                            queen_attack_rect2.midright = (800, y2)
                            queen_attack_direction2 = False
                    last_cooldown2 = QUEEN_COOLDOWN
                    attack_pending_cooldown2 = True
                    cooldown_start_time2 = None
                elif kills2 >= ROOK_THRESHOLD:
                    if not rook2_active:
                        rook2_active = True
                        rook2_projectile_rect = rook_projectile_img.get_rect(center=(x2, y2))
                        rook_projectile_direction2 = facing_right2
                        if rook_facing2 is None:
                            rook_facing2 = facing_right2
                    last_cooldown2 = ROOK_COOLDOWN
                    attack_pending_cooldown2 = True
                    cooldown_start_time2 = None
                elif kills2 >= BISHOP_THRESHOLD:
                    if not windburst2_active:
                        windburst2_active = True
                        windburst2_timer = current_time
                        windburst2_applied = False
                    last_cooldown2 = KNIGHT_COOLDOWN
                    attack_pending_cooldown2 = True
                    cooldown_start_time2 = None
                elif kills2 >= KILL_THRESHOLD:
                    if not slash2_active:
                        slash2_active = True
                        slash2_timer = current_time
                        slash2_applied = False
                        current_slash_sprite = slash_sprite_right if facing_right2 else slash_sprite_left
                        slash2_rect = current_slash_sprite.get_rect(center=(x2, y2))
                    last_cooldown2 = BISHOP_COOLDOWN
                    attack_pending_cooldown2 = True
                    cooldown_start_time2 = None
                else:
                    if not blast2_active:
                        blast2_active = True
                        blast2_end_time = current_time + BLAST_DURATION
                        blast2_damage_timer = current_time
                        current_sprite2 = blast_sprite
                    last_cooldown2 = COOLDOWN
                    attack_pending_cooldown2 = True
                    cooldown_start_time2 = None
                attack_key_pressed2 = True
        else:
            attack_key_pressed2 = False

        if keys[pygame.K_LCTRL] and current_time >= next_universal_melee_attack2:
            universal_melee_active2 = True
            universal_melee_timer2 = current_time
            universal_melee_applied2 = False
            next_universal_melee_attack2 = current_time + UNIVERSAL_MELEE_COOLDOWN

        if not on_ground2:
            fall_speed2 += GRAVITY
        y2 += fall_speed2
        if y2 >= 300:
            y2 = 300
            on_ground2 = True
            fall_speed2 = 0
        elif y2 > 280 and not on_ground2:
            y2 = 280
            on_ground2 = True
            fall_speed2 = 0

        player2_rect = current_sprite2.get_rect(center=(x2, y2))

    # --- Cooldown Management for transformation-specific attacks ---
    if (not blast1_active and not slash1_active and not windburst1_active and not queen_active1 and not king_active1 and
            attack_pending_cooldown1 and cooldown_start_time1 is None):
        cooldown_start_time1 = current_time
        next_attack_time1 = current_time + last_cooldown1
        attack_pending_cooldown1 = False

    if (not blast2_active and not slash2_active and not windburst2_active and not queen_active2 and not king_active2 and
            attack_pending_cooldown2 and cooldown_start_time2 is None):
        cooldown_start_time2 = current_time
        next_attack_time2 = current_time + last_cooldown2
        attack_pending_cooldown2 = False

    # --- Process Universal Melee Attacks ---
    if universal_melee_active1:
        if current_time - universal_melee_timer1 < UNIVERSAL_MELEE_DURATION:
            if facing_right1:
                melee_rect1 = pygame.Rect(player1_rect.right, player1_rect.top, 30, player1_rect.height)
            else:
                melee_rect1 = pygame.Rect(player1_rect.left - 30, player1_rect.top, 30, player1_rect.height)
            if not universal_melee_applied1 and melee_rect1.colliderect(player2_rect) and not respawn2_active:
                health2 -= UNIVERSAL_MELEE_DAMAGE
                universal_melee_applied1 = True
        else:
            universal_melee_active1 = False

    if universal_melee_active2:
        if current_time - universal_melee_timer2 < UNIVERSAL_MELEE_DURATION:
            if facing_right2:
                melee_rect2 = pygame.Rect(player2_rect.right, player2_rect.top, 30, player2_rect.height)
            else:
                melee_rect2 = pygame.Rect(player2_rect.left - 30, player2_rect.top, 30, player2_rect.height)
            if not universal_melee_applied2 and melee_rect2.colliderect(player1_rect) and not respawn1_active:
                health1 -= UNIVERSAL_MELEE_DAMAGE
                universal_melee_applied2 = True
        else:
            universal_melee_active2 = False

    # --- SLASH ATTACK LOGIC ---
    if slash1_active:
        if current_time - slash1_timer < SLASH_DURATION:
            current_slash_sprite = slash_sprite_right if facing_right1 else slash_sprite_left
            slash1_rect = current_slash_sprite.get_rect(center=(x1, y1))
            if not slash1_applied and slash1_rect.colliderect(player2_rect) and not respawn2_active:
                health2 -= SLASH_DAMAGE
                if kills2 >= KING_THRESHOLD:
                    health1 = min(health1 + SLASH_DAMAGE // 2, MAX_HEALTH)
                slash1_applied = True
        else:
            slash1_active = False

    if slash2_active:
        if current_time - slash2_timer < SLASH_DURATION:
            current_slash_sprite = slash_sprite_right if facing_right2 else slash_sprite_left
            slash2_rect = current_slash_sprite.get_rect(center=(x2, y2))
            if not slash2_applied and slash2_rect.colliderect(player1_rect) and not respawn1_active:
                health1 -= SLASH_DAMAGE
                if kills1 >= KING_THRESHOLD:
                    health2 = min(health2 + SLASH_DAMAGE // 2, MAX_HEALTH)
                slash2_applied = True
        else:
            slash2_active = False

    # --- WINDBURST ATTACK LOGIC ---
    if windburst1_active:
        if current_time - windburst1_timer < WINDBURST_DURATION:
            if not windburst1_applied and abs(y2 - y1) <= 10 and not respawn2_active:
                health2 -= WINDBURST_DAMAGE
                if kills2 >= KING_THRESHOLD:
                    health1 = min(health1 + WINDBURST_DAMAGE // 2, MAX_HEALTH)
                windburst1_applied = True
        else:
            windburst1_active = False
    if windburst2_active:
        if current_time - windburst2_timer < WINDBURST_DURATION:
            if not windburst2_applied and abs(y1 - y2) <= 10 and not respawn1_active:
                health1 -= WINDBURST_DAMAGE
                if kills1 >= KING_THRESHOLD:
                    health2 = min(health2 + WINDBURST_DAMAGE // 2, MAX_HEALTH)
                windburst2_applied = True
        else:
            windburst2_active = False

    # --- BLAST ATTACK LOGIC ---
    if blast1_active:
        if current_time >= blast1_end_time:
            blast1_active = False
            if kills1 >= KING_THRESHOLD:
                current_sprite1 = king_sprite2 if facing_right1 else king_sprite2_flipped
            elif kills1 >= QUEEN_THRESHOLD:
                current_sprite1 = queen_sprite2 if facing_right1 else queen_sprite2_flipped
            elif kills1 >= ROOK_THRESHOLD:
                current_sprite1 = rook_sprite if (rook_facing1 if rook_facing1 is not None else facing_right1) else rook_sprite_flipped
            elif kills1 >= BISHOP_THRESHOLD:
                current_sprite1 = bishop_sprite1
            elif kills1 >= KILL_THRESHOLD:
                current_sprite1 = knight_sprite1_flipped if facing_right1 else knight_sprite1
            else:
                current_sprite1 = base_sprite1
        else:
            current_sprite1 = blast_sprite
            player1_rect = current_sprite1.get_rect(center=(x1, y1))

    if blast2_active:
        if current_time >= blast2_end_time:
            blast2_active = False
            if kills2 >= KING_THRESHOLD:
                current_sprite2 = king_sprite1 if facing_right2 else king_sprite1_flipped
            elif kills2 >= QUEEN_THRESHOLD:
                current_sprite2 = queen_sprite1 if facing_right2 else queen_sprite1_flipped
            elif kills2 >= ROOK_THRESHOLD:
                current_sprite2 = rook_sprite_p2 if (rook_facing2 if rook_facing2 is not None else facing_right2) else rook_sprite_p2_flipped
            elif kills2 >= BISHOP_THRESHOLD:
                current_sprite2 = bishop_sprite2
            elif kills2 >= KILL_THRESHOLD:
                current_sprite2 = knight_sprite2_flipped if facing_right2 else knight_sprite2
            else:
                current_sprite2 = base_sprite2
        else:
            current_sprite2 = blast_sprite
            player2_rect = current_sprite2.get_rect(center=(x2, y2))

    if blast1_active and player1_rect.colliderect(player2_rect) and not respawn2_active:
        if current_time - blast1_damage_timer >= BLAST_TICK_RATE:
            health2 -= BLAST_DAMAGE
            if kills2 >= KING_THRESHOLD:
                health1 = min(health1 + BLAST_DAMAGE // 2, MAX_HEALTH)
            blast1_damage_timer = current_time

    if blast2_active and player2_rect.colliderect(player1_rect) and not respawn1_active:
        if current_time - blast2_damage_timer >= BLAST_TICK_RATE:
            health1 -= BLAST_DAMAGE
            if kills1 >= KING_THRESHOLD:
                health2 = min(health2 + BLAST_DAMAGE // 2, MAX_HEALTH)
            blast2_damage_timer = current_time

    # --- ROOK ATTACK LOGIC ---
    if rook1_active and rook1_projectile_rect is not None:
        if rook_projectile_direction1:
            rook1_projectile_rect.x += ROOK_PROJECTILE_SPEED
        else:
            rook1_projectile_rect.x -= ROOK_PROJECTILE_SPEED
        if rook1_projectile_rect.colliderect(player2_rect) and not respawn2_active:
            health2 -= ROOK_DAMAGE
            if kills2 >= KING_THRESHOLD:
                health1 = min(health1 + ROOK_DAMAGE // 2, MAX_HEALTH)
            rook1_active = False
            rook1_projectile_rect = None
        if rook1_projectile_rect is not None and (rook1_projectile_rect.right < 0 or rook1_projectile_rect.left > 800):
            rook1_active = False
            rook1_projectile_rect = None

    if rook2_active and rook2_projectile_rect is not None:
        if rook_projectile_direction2:
            rook2_projectile_rect.x += ROOK_PROJECTILE_SPEED
        else:
            rook2_projectile_rect.x -= ROOK_PROJECTILE_SPEED
        if rook2_projectile_rect.colliderect(player1_rect) and not respawn1_active:
            health1 -= ROOK_DAMAGE
            if kills1 >= KING_THRESHOLD:
                health2 = min(health2 + ROOK_DAMAGE // 2, MAX_HEALTH)
            rook2_active = False
            rook2_projectile_rect = None
        if rook2_projectile_rect is not None and (rook2_projectile_rect.right < 0 or rook2_projectile_rect.left > 800):
            rook2_active = False
            rook2_projectile_rect = None

    # --- QUEEN ATTACK LOGIC ---
    if queen_active1 and queen_attack_rect1 is not None:
        if queen_attack_direction1:
            queen_attack_rect1.x += QUEEN_ATTACK_SPEED
        else:
            queen_attack_rect1.x -= QUEEN_ATTACK_SPEED
        if queen_attack_rect1.colliderect(player2_rect) and not respawn2_active:
            health2 -= QUEEN_DAMAGE
            if kills2 >= KING_THRESHOLD:
                health1 = min(health1 + QUEEN_DAMAGE // 2, MAX_HEALTH)
            queen_active1 = False
            queen_attack_rect1 = None
        if queen_attack_rect1 is not None and (queen_attack_rect1.right < 0 or queen_attack_rect1.left > 800):
            queen_active1 = False
            queen_attack_rect1 = None

    if queen_active2 and queen_attack_rect2 is not None:
        if queen_attack_direction2:
            queen_attack_rect2.x += QUEEN_ATTACK_SPEED
        else:
            queen_attack_rect2.x -= QUEEN_ATTACK_SPEED
        if queen_attack_rect2.colliderect(player1_rect) and not respawn1_active:
            health1 -= QUEEN_DAMAGE
            if kills1 >= KING_THRESHOLD:
                health2 = min(health2 + QUEEN_DAMAGE // 2, MAX_HEALTH)
            queen_active2 = False
            queen_attack_rect2 = None
        if queen_attack_rect2 is not None and (queen_attack_rect2.right < 0 or queen_attack_rect2.left > 800):
            queen_active2 = False
            queen_attack_rect2 = None

    # --- CHECK FOR KILLS AND RESPAWN / GAME OVER ---
    # For player 1:
    if health1 <= 0:
        if kills2 >= KING_THRESHOLD:
            splat_sound.play()
            game_over = True
            game_over_time = current_time
            winner = "Player 2"
        else:
            splat_sound.play()
            kills2 += 1
            health1 = MAX_HEALTH
            respawn1_active = True
            respawn1_timer = current_time
            rook_facing1 = None
            rook_projectile_direction1 = None

    # For player 2:
    if health2 <= 0:
        if kills1 >= KING_THRESHOLD:
            splat_sound.play()
            game_over = True
            game_over_time = current_time
            winner = "Player 1"
        else:
            splat_sound.play()
            kills1 += 1
            health2 = MAX_HEALTH
            respawn2_active = True
            respawn2_timer = current_time
            rook_facing2 = None
            rook_projectile_direction2 = None

    if not game_over:
        if respawn1_active and current_time - respawn1_timer >= RESPAWN_TIME:
            x1, y1 = SPAWN_POSITIONS[0]
            respawn1_active = False
        if respawn2_active and current_time - respawn2_timer >= RESPAWN_TIME:
            x2, y2 = SPAWN_POSITIONS[1]
            respawn2_active = False

    # --- SWITCH TO TRANSFORMATION SPRITES AFTER REACHING THRESHOLDS ---
    if not blast1_active and not slash1_active:
        if kills1 >= KING_THRESHOLD:
            current_sprite1 = king_sprite2 if facing_right1 else king_sprite2_flipped
        elif kills1 >= QUEEN_THRESHOLD:
            current_sprite1 = queen_sprite2 if facing_right1 else queen_sprite2_flipped
        elif kills1 >= ROOK_THRESHOLD:
            current_sprite1 = rook_sprite if (rook_facing1 if rook_facing1 is not None else facing_right1) else rook_sprite_flipped
        elif kills1 >= BISHOP_THRESHOLD:
            current_sprite1 = bishop_sprite1
        elif kills1 >= KILL_THRESHOLD:
            current_sprite1 = knight_sprite1_flipped if facing_right1 else knight_sprite1
        else:
            current_sprite1 = base_sprite1

    if not blast2_active and not slash2_active:
        if kills2 >= KING_THRESHOLD:
            current_sprite2 = king_sprite1 if facing_right2 else king_sprite1_flipped
        elif kills2 >= QUEEN_THRESHOLD:
            current_sprite2 = queen_sprite1 if facing_right2 else queen_sprite1_flipped
        elif kills2 >= ROOK_THRESHOLD:
            current_sprite2 = rook_sprite_p2 if (rook_facing2 if rook_facing2 is not None else facing_right2) else rook_sprite_p2_flipped
        elif kills2 >= BISHOP_THRESHOLD:
            current_sprite2 = bishop_sprite2
        elif kills2 >= KILL_THRESHOLD:
            current_sprite2 = knight_sprite2_flipped if facing_right2 else knight_sprite2
        else:
            current_sprite2 = base_sprite2

    # --- RENDERING ---
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))

    cooldown_bar_width = 200
    cooldown_bar_height = 10
    if cooldown_start_time1 is not None:
        ratio1 = (current_time - cooldown_start_time1) / last_cooldown1
    else:
        ratio1 = 1 if current_time >= next_attack_time1 else 0
    ratio1 = max(0, min(1, ratio1))
    fill_width1 = int(ratio1 * cooldown_bar_width)
    pygame.draw.rect(screen, (169, 169, 169), (600, 350, cooldown_bar_width, cooldown_bar_height))
    pygame.draw.rect(screen, (0, 191, 255), (600, 350, fill_width1, cooldown_bar_height))

    if cooldown_start_time2 is not None:
        ratio2 = (current_time - cooldown_start_time2) / last_cooldown2
    else:
        ratio2 = 1 if current_time >= next_attack_time2 else 0
    ratio2 = max(0, min(1, ratio2))
    fill_width2 = int(ratio2 * cooldown_bar_width)
    pygame.draw.rect(screen, (169, 169, 169), (20, 350, cooldown_bar_width, cooldown_bar_height))
    pygame.draw.rect(screen, (0, 191, 255), (20, 350, fill_width2, cooldown_bar_height))

    if slash1_active and slash1_rect:
        current_slash_sprite = slash_sprite_right if facing_right1 else slash_sprite_left
        screen.blit(current_slash_sprite, slash1_rect)
    if slash2_active and slash2_rect:
        current_slash_sprite = slash_sprite_right if facing_right2 else slash_sprite_left
        screen.blit(current_slash_sprite, slash2_rect)

    if windburst1_active:
        windburst_rect = pygame.Rect(0, y1 - windburst_sprite.get_height() // 2, 800, windburst_sprite.get_height())
        scaled_windburst = pygame.transform.scale(windburst_sprite, (800, windburst_sprite.get_height()))
        screen.blit(scaled_windburst, windburst_rect)
    if windburst2_active:
        windburst_rect = pygame.Rect(0, y2 - windburst_sprite.get_height() // 2, 800, windburst_sprite.get_height())
        scaled_windburst = pygame.transform.scale(windburst_sprite, (800, windburst_sprite.get_height()))
        screen.blit(scaled_windburst, windburst_rect)

    if rook1_active and rook1_projectile_rect:
        screen.blit(rook_projectile_img, rook1_projectile_rect)
    if rook2_active and rook2_projectile_rect:
        screen.blit(rook_projectile_img, rook2_projectile_rect)

    if queen_active1 and queen_attack_rect1:
        screen.blit(queen_wave_img, queen_attack_rect1)
    if queen_active2 and queen_attack_rect2:
        screen.blit(queen_wave_img, queen_attack_rect2)

    if not respawn1_active:
        screen.blit(current_sprite1, player1_rect)
    if not respawn2_active:
        screen.blit(current_sprite2, player2_rect)

    pygame.draw.rect(screen, (255, 0, 0), (600, 370, max(health1, 0) * 2, 20))
    pygame.draw.rect(screen, (255, 0, 0), (20, 370, max(health2, 0) * 2, 20))

    score1 = font.render(str(kills1), True, (255, 255, 255))
    score2 = font.render(str(kills2), True, (255, 255, 255))
    screen.blit(score1, (750, 10))
    screen.blit(score2, (30, 10))

    if king_tint_active1 or king_tint_active2:
        red_tint = pygame.Surface((800, 400))
        red_tint.set_alpha(100)
        red_tint.fill((255, 0, 0))
        screen.blit(red_tint, (0, 0))
        if current_time >= king_tint_end_time1:
            king_tint_active1 = False
        if current_time >= king_tint_end_time2:
            king_tint_active2 = False

    pygame.display.update()
    clock.tick(60)
