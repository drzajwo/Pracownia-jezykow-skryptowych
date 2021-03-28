import pygame
import json
from pygame.locals import QUIT, K_ESCAPE, K_LEFT, K_RIGHT

pygame.init()

CLOCK = pygame.time.Clock()

# SCREEN PROPS
SCREEN_HEIGHT = 960
SCREEN_WIDTH = 1280
BORDER_OFFSET = 40

# GAME PROPS
BALL_X_VELOCITY = 8.0
BALL_Y_VELOCITY = 9.0

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Breakout UJ")

is_running = True

# ======== SOUNDS ========

pygame.mixer.music.load("sounds/intro.mp3")
pygame.mixer.music.set_volume(0.4)


# pygame.mixer.music.play(-1)


# ======== PLAYER ========

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.image.load("images/player_1.png").convert()
        self.rect = self.surf.get_rect(center=(x, y))

    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-6, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(6, 0)

        if self.rect.left < BORDER_OFFSET:
            self.rect.left = BORDER_OFFSET
        if self.rect.right >= SCREEN_WIDTH - BORDER_OFFSET:
            self.rect.right = SCREEN_WIDTH - BORDER_OFFSET


# ======== BLOCKS ========

class Block(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.image.load("images/blue_block.png").convert()
        self.rect = self.surf.get_rect(center=(x, y))
        # self.surf = pygame.transform.scale(self.surf, (40, 20))


# ======== BALL ========

# TODO: Move ball, check borders, speed
class Ball(pygame.sprite.Sprite):
    pos_x = 0
    pos_y = 0
    velocity = 20.0
    direction_x = "left"
    direction_y = "up"

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.image.load("images/ball.png").convert()
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
        if pygame.time.get_ticks() - self.counter >= self.velocity:
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

def generate_level(level):
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
        # TODO: get info how to change globally declared props
        BALL_X_VELOCITY = float(ball_props['xVelocity'])
        BALL_Y_VELOCITY = float(ball_props['yVelocity'])
    return blocks_collection


# ======== MAIN LOOP ========

player = Player(610, 940)
ball = Ball(620, 720)

blocks = generate_level(1)

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

    CLOCK.tick(60)
    pygame.display.flip()

pygame.quit()
