# === CodeCats: The Bug Hunt ===
import pgzrun
import pygame
import random

WIDTH = 640
HEIGHT = 480
TITLE = "CodeCats – The Bug Hunt"
TILE_SIZE = 64
TILE_COLS = WIDTH // TILE_SIZE
TILE_ROWS = HEIGHT // TILE_SIZE

music.set_volume(0.5)
music.play('bg_music')

game_state = 'menu'
sound_on = True
show_start_message = True
current_level = 1
MAX_LEVEL = 3
show_help = False

start_button = Rect((220, 150), (200, 50))
sound_button = Rect((220, 220), (200, 50))
exit_button = Rect((220, 290), (200, 50))
help_button = Rect((580, 10), (50, 30))

floor_tiles = []
wall_tiles = []
hero = None
enemies = []
terminal = None
tilemap = []
current_direction = [0, 0]

# === hero class ===
class CodeCat:
    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.x = col * TILE_SIZE
        self.y = row * TILE_SIZE
        self.state = 'idle'
        self.frame = 0
        self.frame_timer = 0
        self.walk_target = None

    def draw(self):
        image = self.get_current_sprite()
        screen.blit(image, (self.x, self.y))

    def get_current_sprite(self):
        frames = ['codecat/cat_idle1', 'codecat/cat_idle2'] if self.state == 'idle' else ['codecat/cat_walk1', 'codecat/cat_walk2']
        return frames[self.frame % len(frames)]

    def update(self, dt):
        self.frame_timer += dt
        if self.frame_timer >= 0.3:
            self.frame += 1
            self.frame_timer = 0
        if self.walk_target:
            tx, ty = self.walk_target
            dx, dy = tx - self.x, ty - self.y
            step = 4
            self.x += step if dx > 0 else -step if dx < 0 else 0
            self.y += step if dy > 0 else -step if dy < 0 else 0
            if abs(dx) <= step and abs(dy) <= step:
                self.x, self.y = tx, ty
                self.walk_target = None
                self.state = 'idle'

    def try_move(self, dx, dy):
        new_col = self.col + dx
        new_row = self.row + dy
        if tilemap[new_row][new_col] == 'F' and not self.walk_target:
            self.col, self.row = new_col, new_row
            self.walk_target = (new_col * TILE_SIZE, new_row * TILE_SIZE)
            self.state = 'walk'

# === enemy class ===
class BugEnemy:
    def __init__(self, name, folder, col, row):
        self.name = name
        self.folder = folder
        self.col = col
        self.row = row
        self.x = col * TILE_SIZE
        self.y = row * TILE_SIZE
        self.state = 'idle'
        self.frame = 0
        self.frame_timer = 0
        self.walk_target = None
        self.wait_timer = 0

    def draw(self):
        screen.blit(self.get_current_sprite(), (self.x, self.y))

    def get_current_sprite(self):
        frames = [f'{self.folder}/{self.name}_idle1', f'{self.folder}/{self.name}_idle2'] if self.state == 'idle' else [f'{self.folder}/{self.name}_walk1', f'{self.folder}/{self.name}_walk2']
        return frames[self.frame % len(frames)]

    def update(self, dt):
        self.frame_timer += dt
        if self.frame_timer >= 0.3:
            self.frame += 1
            self.frame_timer = 0
        if self.walk_target:
            tx, ty = self.walk_target
            dx, dy = tx - self.x, ty - self.y
            step = 2 + current_level
            self.x += step if dx > 0 else -step if dx < 0 else 0
            self.y += step if dy > 0 else -step if dy < 0 else 0
            if abs(dx) <= step and abs(dy) <= step:
                self.x, self.y = tx, ty
                self.walk_target = None
                self.state = 'idle'
        else:
            self.wait_timer += dt
            if self.wait_timer >= 1.0:
                self.wait_timer = 0
                self.try_random_move()

    def try_random_move(self):
        dx, dy = random.choice([(0,-1), (0,1), (-1,0), (1,0)])
        new_col = self.col + dx
        new_row = self.row + dy
        if tilemap[new_row][new_col] == 'F':
            self.col = new_col
            self.row = new_row
            self.walk_target = (new_col * TILE_SIZE, new_row * TILE_SIZE)
            self.state = 'walk'

def generate_level(level):
    global tilemap, floor_tiles, wall_tiles, hero, enemies, terminal
    tilemap = [['W'] * TILE_COLS for _ in range(TILE_ROWS)]
    for _ in range(200):
        r, c = random.randint(1, TILE_ROWS - 2), random.randint(1, TILE_COLS - 2)
        tilemap[r][c] = 'F'

    floor_tiles, wall_tiles = [], []
    for r in range(TILE_ROWS):
        for c in range(TILE_COLS):
            tile = Actor('tile_floor' if tilemap[r][c] == 'F' else 'tile_wall')
            tile.topleft = (c * TILE_SIZE, r * TILE_SIZE)
            (floor_tiles if tilemap[r][c] == 'F' else wall_tiles).append(tile)

    spawnable = [(r, c) for r in range(TILE_ROWS) for c in range(TILE_COLS) if tilemap[r][c] == 'F']
    random.shuffle(spawnable)
    hero_r, hero_c = spawnable.pop()
    term_r, term_c = spawnable.pop()
    hero = CodeCat(hero_c, hero_r)
    terminal = Actor('tile_terminal')
    terminal.topleft = (term_c * TILE_SIZE, term_r * TILE_SIZE)
    terminal.row, terminal.col = term_r, term_c

    enemies.clear()
    for _ in range(level):
        r, c = spawnable.pop()
        enemies.append(BugEnemy('stackroach', 'stackroach', c, r))

def draw():
    screen.clear()
    if game_state == 'menu':
        draw_menu()
    elif game_state == 'game':
        draw_game()
    elif game_state == 'victory':
        screen.draw.text("YOU WIN!", center=(WIDTH//2, HEIGHT//2), fontsize=64, color="white")
    elif game_state == 'game_over':
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=64, color="red")

def draw_menu():
    screen.fill((0, 0, 0))
    screen.draw.text("CODECATS", center=(WIDTH // 2, 80), fontsize=48, color="white")
    for btn, text in [(start_button, "Start Game"), (sound_button, f"Sound: {'ON' if sound_on else 'OFF'}"), (exit_button, "Exit")]:
        screen.draw.filled_rect(btn, (50, 50, 50))
        screen.draw.text(text, center=btn.center, fontsize=32, color="white")
    screen.draw.filled_rect(help_button, (80, 80, 80))
    screen.draw.text("?", center=help_button.center, fontsize=28, color="white")
    if show_help:
        screen.draw.filled_rect(Rect((100, 80), (440, 320)), (0, 0, 0))
        screen.draw.text("CodeCats is a light roguelike where you control a programmer kitten trapped in a computer.", topleft=(110, 90), width=420, fontsize=20, color="white")
        screen.draw.text("Controls: WASD to move, E to activate terminal.", topleft=(110, 150), fontsize=20, color="white")
        screen.draw.text("Objective: Clean all terminals and complete 3 phases.", topleft=(110, 180), fontsize=20, color="white")
        screen.draw.text("Villains: StackRoach and OverflowFly (for now)", topleft=(110, 210), fontsize=20, color="white")
        screen.draw.text("Click ? again to close.", topleft=(110, 280), fontsize=18, color="white")

def draw_game():
    for tile in floor_tiles + wall_tiles:
        tile.draw()
    for bug in enemies:
        bug.draw()
    if terminal:
        terminal.draw()
    hero.draw()
    if show_start_message:
        screen.draw.text("Let's squish some bugs!", center=(WIDTH//2, HEIGHT//2), fontsize=36, color="white")

def on_mouse_down(pos):
    global game_state, sound_on, show_start_message, current_level, show_help
    if game_state == 'menu':
        if start_button.collidepoint(pos):
            current_level = 1
            generate_level(current_level)
            game_state = 'game'
            show_start_message = True
            clock.schedule_unique(hide_start_message, 2.0)
        elif sound_button.collidepoint(pos):
            sound_on = not sound_on
            if sound_on:
                music.play('bg_music')
            else:
                music.stop()
        elif exit_button.collidepoint(pos):
            pygame.quit()
        elif help_button.collidepoint(pos):
            show_help = not show_help

def on_key_down(key):
    global terminal
    if game_state != 'game':
        return
    if key == keys.E:
        if terminal and abs(hero.col - terminal.col) <= 1 and abs(hero.row - terminal.row) <= 1:
            if sound_on:
                sounds.terminal_beep.stop()
                sounds.terminal_beep.play()
            terminal = None
            next_level()
    if key == keys.W: current_direction[:] = 0, -1
    elif key == keys.S: current_direction[:] = 0, 1
    elif key == keys.A: current_direction[:] = -1, 0
    elif key == keys.D: current_direction[:] = 1, 0

def on_key_up(key):
    if key in [keys.W, keys.S, keys.A, keys.D]:
        current_direction[:] = 0, 0

def update(dt):
    if game_state == 'game':
        hero.update(dt)
        for bug in enemies:
            bug.update(dt)
        if not hero.walk_target and any(current_direction):
            hero.try_move(*current_direction)
        check_collisions()

def check_collisions():
    global game_state
    for bug in enemies:
        if hero.col == bug.col and hero.row == bug.row:
            game_state = 'game_over'
            music.stop()
            break

def hide_start_message():
    global show_start_message
    show_start_message = False

def next_level():
    global current_level, game_state
    current_level += 1
    if current_level > MAX_LEVEL:
        game_state = 'victory'
        music.stop()
    else:
        generate_level(current_level)

pgzrun.go()
