import pygame
import pygame.freetype
import json
from pygame.locals import QUIT, K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE

# TODO: scores to list not single, README

pygame.init()

CLOCK = pygame.time.Clock()

# SCREEN PROPS
SCREEN_HEIGHT = 960
SCREEN_WIDTH = 1280
BORDER_OFFSET = 40

# GAME PROPS
BALL_X_VELOCITY = 3.0
BALL_Y_VELOCITY = 3.0

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Breakout UJ")
GAME_FONT = pygame.freetype.Font("fonts/TrainOne-regular.ttf", 18)

default_btn_bg_color = (120, 165, 55)
hovered_btn_bg_color = (120, 255, 55)

is_running = True
current_level = 1
max_level = 5
score = 0
mode = 'menu'

# ======== SOUNDS ========

pygame.mixer.music.load("sounds/intro.mp3")
pygame.mixer.music.set_volume(0.4)


# TODO: uncomment when "releasing"
# pygame.mixer.music.play(-1)


# ======== PLAYER ========

class Player(pygame.sprite.Sprite):
    lives = 3

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.image.load("images/player_1.png")
        self.rect = self.surf.get_rect(center=(x, y))

    def decrease_live(self):
        self.lives -= 1

    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-6, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(6, 0)

        if self.rect.left < BORDER_OFFSET:
            self.rect.left = BORDER_OFFSET
        if self.rect.right >= SCREEN_WIDTH - BORDER_OFFSET:
            self.rect.right = SCREEN_WIDTH - BORDER_OFFSET


class HealthHeart(pygame.sprite.Sprite):

    def __init__(self, x_pos):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.image.load("images/heart.png")
        self.rect = self.surf.get_rect(center=(x_pos, 13))


# ======== BLOCKS ========

class Block(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.image.load("images/blue_block.png")
        self.rect = self.surf.get_rect(center=(x, y))


# ======== BALL ========

class Ball(pygame.sprite.Sprite):
    pos_x = 0
    pos_y = 0
    velocity = 20.0
    direction_x = "left"
    direction_y = "up"

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.image.load("images/ball.png")
        self.pos_x = x
        self.pos_y = y
        self.rect = self.surf.get_rect(center=(x, y))
        self.counter = pygame.time.get_ticks()

    def toggle_x(self):
        if self.direction_x == "right":
            self.direction_x = "left"
        else:
            self.direction_x = "right"

    def toggle_y(self):
        if self.direction_y == "up":
            self.direction_y = "down"
        else:
            self.direction_y = "up"

    def update(self):
        self.counter = pygame.time.get_ticks()
        # LEFT MOVEMENT
        if self.direction_x == "left":
            self.pos_x -= BALL_X_VELOCITY
            if self.pos_x <= BORDER_OFFSET:
                self.toggle_x()
        # RIGHT MOVEMENT
        if self.direction_x == "right":
            self.pos_x += BALL_X_VELOCITY
            if self.pos_x >= SCREEN_WIDTH - BORDER_OFFSET:
                self.toggle_x()
        # UP MOVEMENT
        if self.direction_y == "up":
            self.pos_y -= BALL_Y_VELOCITY
            if self.pos_y <= BORDER_OFFSET:
                self.toggle_y()
        # DOWN MOVEMENT
        if self.direction_y == "down":
            self.pos_y += BALL_Y_VELOCITY

        self.rect = self.surf.get_rect(center=(self.pos_x, self.pos_y))


# ======== LEVEL GEN ========

def load_level(level):
    global BALL_X_VELOCITY, BALL_Y_VELOCITY
    blocks_collection = pygame.sprite.Group()
    # open json file and parse
    with open("levels/" + str(level) + ".json") as json_file:
        data = json.load(json_file)
        # Loading blocks
        for block_data in data['blocks']:
            # load block lives etc.
            new_block = Block(block_data['x'], block_data['y'])
            blocks_collection.add(new_block)
        # Loading ball props
        ball_props = data['ball']
        BALL_X_VELOCITY = float(ball_props['xVelocity'])
        BALL_Y_VELOCITY = float(ball_props['yVelocity'])
        json_file.close()
    return blocks_collection


# ======== SCORE SAVING ========
# TODO: IMPROVE: save json with 5 best scores
def read_high_score():
    try:
        with open("save/scores.txt", "r") as file:
            level_score = file.read()
            file.close()
            return int(level_score)
    except FileNotFoundError:
        return 0


def save_score():
    global score
    current_high_score = read_high_score()
    if score < current_high_score:
        return
    with open("save/scores.txt", "w") as file:
        file.write(str(score))
        file.close()


# ======== GAME LOOP ========

def reset_game_states():
    global player, ball, live_hearts, score, current_level
    score = 0
    current_level = 1
    player = Player(610, 940)
    ball = Ball(620, 720)

    live_hearts = pygame.sprite.Group()
    for i in range(player.lives):
        heart = HealthHeart(i * 20 + 40)
        live_hearts.add(heart)


player = Player(610, 940)
ball = Ball(620, 720)

live_hearts = pygame.sprite.Group()
for i in range(player.lives):
    heart = HealthHeart(i * 20 + 40)
    live_hearts.add(heart)

blocks = load_level(1)


def game_loop():
    global score

    pressed_key = pygame.key.get_pressed()
    player.update(pressed_key)
    ball.update()

    screen.fill((0, 0, 0))

    # ======== INITIALIZING OBJECTS ========

    screen.blit(player.surf, player.rect)
    screen.blit(ball.surf, ball.rect)

    for block in blocks:
        screen.blit(block.surf, block.rect)

    # ======== COLLISIONS ========
    # ball hits block
    if pygame.sprite.spritecollideany(ball, blocks):
        delete_block = pygame.sprite.spritecollideany(ball, blocks)
        delete_block.kill()
        score += 10
        # check on which part was hit made
        if delete_block.rect.left < ball.rect.centerx < delete_block.rect.right:
            ball.toggle_y()
        elif ball.rect.centerx == delete_block.rect.left or ball.rect.centerx == delete_block.rect.right:
            ball.toggle_x()
            ball.toggle_y()
        else:
            ball.toggle_x()

    # ball hits player platform
    if ball.rect.colliderect(player):
        ball.direction_y = "up"
        # toggle direction if player movement is in opposite direction
        if pressed_key[K_LEFT] and ball.direction_x == "right":
            ball.direction_x = "left"
        if pressed_key[K_RIGHT] and ball.direction_x == "left":
            ball.direction_x = "right"

    # ======== GAME CONDITIONS ========
    # Check if ball is in the game
    if ball.pos_y >= SCREEN_HEIGHT:
        player.decrease_live()
        heart_to_remove = live_hearts.sprites().pop(player.lives)
        live_hearts.remove(heart_to_remove)
        if player.lives == 0:
            save_score()
            change_mode('over')
        ball.pos_x = 620
        ball.pos_y = 720
        ball.direction_x = "left"
        ball.direction_y = "up"

    # Handle finished level
    if len(blocks) == 0:
        change_mode('complete')

    # ======== DISPLAY INFO ========
    # Health
    for live_heart in live_hearts:
        screen.blit(live_heart.surf, live_heart.rect)

    # Score
    GAME_FONT.render_to(screen, (640, 7), str(score), (255, 0, 0))


# ======== MENU ========

class Button:
    text_color = (255, 0, 0)
    background_color = default_btn_bg_color

    def __init__(self, text, x_pos, y_pos, rect, action):
        self.text = text
        self.rect = rect
        self.action = action
        self.x = x_pos
        self.y = y_pos

    def click(self):
        self.action()

    def print(self):
        pygame.draw.rect(screen, self.background_color, self.rect)
        GAME_FONT.render_to(screen, (self.x, self.y), self.text, self.text_color)


rect1 = pygame.Rect(115, 175, 120, 60)
rect2 = pygame.Rect(115, 275, 120, 60)
rect3 = pygame.Rect(115, 375, 120, 60)


def change_mode(new_mode):
    global mode
    mode = new_mode


navigation_buttons = [
    Button("START", 140, 200, rect1, lambda: change_mode('game')),
    Button("SCORES", 140, 300, rect2, lambda: change_mode('scores')),
    Button("EXIT", 140, 400, rect3, lambda: change_mode('exit')),
]


def main_menu():
    global blocks, current_level, player
    screen.fill((0, 0, 0))
    reset_game_states()
    blocks = load_level(1)
    for btn in navigation_buttons:
        btn.print()


# ======== SCORES SCREEN ========
back_rect = pygame.Rect(520, 775, 245, 60)
back_button = Button("BACK TO MAIN MENU", 540, 800, back_rect, lambda: change_mode('menu'))


def scores_screen():
    screen.fill((0, 0, 0))
    red_color = (255, 0, 0)
    GAME_FONT.render_to(screen, (580, 400), 'Best scores:', red_color)
    back_button.print()


# ======== PAUSE ========
def pause_screen():
    red_color = (255, 0, 0)
    GAME_FONT.render_to(screen, (540, 400), 'GAME PAUSED', red_color)
    GAME_FONT.render_to(screen, (540, 440), 'PRESS "ESC" KEY TO RESUME', red_color)
    back_button.print()


# ======== LEVEL COMPLETE ========
def level_complete_screen():
    screen.fill((0, 0, 0))
    red_color = (255, 0, 0)
    GAME_FONT.render_to(screen, (540, 400), 'LEVEL COMPLETE', red_color)
    if current_level == max_level:
        GAME_FONT.render_to(screen, (540, 440), 'CONGRATULATIONS! YOU FINISHED GAME', red_color)
    else:
        GAME_FONT.render_to(screen, (540, 480), 'PRESS "SPACE" KEY TO CONTINUE', red_color)
    back_button.print()


# ======== GAME OVER ========

def game_over_screen():
    screen.fill((0, 0, 0))
    red_color = (255, 0, 0)
    GAME_FONT.render_to(screen, (540, 400), 'GAME OVER!', red_color)
    GAME_FONT.render_to(screen, (540, 440), 'YOUR SCORE IS:', red_color)
    GAME_FONT.render_to(screen, (540, 480), str(score), red_color)
    GAME_FONT.render_to(screen, (540, 520), 'PRESS "SPACE" KEY TO START AGAIN', red_color)
    back_button.print()


# ======== MAIN LOOP ========


# game modes: 'menu', 'game', 'pause', 'scores', 'complete', 'over', 'exit'
while is_running:
    # Game events
    for events in pygame.event.get():
        if events.type == QUIT:
            is_running = False
        # Pause handling
        if events.type == pygame.KEYDOWN:
            if events.key == K_ESCAPE:
                if mode == 'game':
                    change_mode('pause')
                elif mode == 'pause':
                    change_mode('game')
            elif events.key == K_SPACE:
                # Load next level
                if mode == 'complete':
                    if current_level < max_level:
                        current_level += 1
                        blocks = load_level(current_level)
                # Load first level
                elif mode == 'over':
                    reset_game_states()
                    blocks = load_level(1)
                    change_mode('game')
        # click buttons
        elif events.type == pygame.MOUSEBUTTONDOWN:
            for button in navigation_buttons:
                if button.rect.collidepoint(events.pos):
                    button.click()
            if back_button.rect.collidepoint(events.pos):
                back_button.click()
        # hover over buttons
        elif events.type == pygame.MOUSEMOTION:
            for button in navigation_buttons:
                if button.rect.collidepoint(events.pos):
                    button.background_color = hovered_btn_bg_color
                else:
                    button.background_color = default_btn_bg_color
            if back_button.rect.collidepoint(events.pos):
                back_button.background_color = hovered_btn_bg_color
            else:
                back_button.background_color = default_btn_bg_color

    # Handling different game modes
    if mode == 'menu':
        main_menu()
    elif mode == 'game':
        game_loop()
    elif mode == 'pause':
        pause_screen()
    elif mode == 'scores':
        scores_screen()
    elif mode == 'complete':
        level_complete_screen()
    elif mode == 'over':
        game_over_screen()
    elif mode == 'exit':
        is_running = False

    CLOCK.tick(60)
    pygame.display.flip()

pygame.quit()
