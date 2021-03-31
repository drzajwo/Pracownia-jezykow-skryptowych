import pygame
import json
from pygame.locals import QUIT, K_ESCAPE, K_LEFT, K_RIGHT

# TODO: Menu, Pause, Scores, Saving Score, Sound for ball hitting elements, End game factors

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

is_running = True
is_game_over = False

# ======== SOUNDS ========

pygame.mixer.music.load("sounds/intro.mp3")
pygame.mixer.music.set_volume(0.4)


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

# TODO: add colors and lives
class Block(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.image.load("images/blue_block.png")
        self.rect = self.surf.get_rect(center=(x, y))
        # self.surf = pygame.transform.scale(self.surf, (40, 20))


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
    return blocks_collection


# ======== MAIN LOOP ========

player = Player(610, 940)
ball = Ball(620, 720)

live_hearts = pygame.sprite.Group()
for i in range(player.lives):
    heart = HealthHeart(i*20 + 40)
    live_hearts.add(heart)

blocks = load_level(1)

while is_running:
    for events in pygame.event.get():
        if events.type == QUIT:
            is_running = False

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
            is_game_over = True
        ball.pos_x = 620
        ball.pos_y = 720
        ball.direction_x = "left"
        ball.direction_y = "up"
        # Todo: save score

    # ======== DISPLAY INFO ========
    # Health
    for live_heart in live_hearts:
        screen.blit(live_heart.surf, live_heart.rect)

    # TODO: Score


    CLOCK.tick(60)
    pygame.display.flip()

pygame.quit()
