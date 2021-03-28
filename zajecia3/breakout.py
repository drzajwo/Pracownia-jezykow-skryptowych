import pygame
import json
from pygame.locals import QUIT, K_ESCAPE, K_LEFT, K_RIGHT

pygame.init()

CLOCK = pygame.time.Clock()

SCREEN_HEIGHT = 960
SCREEN_WIDTH = 1280

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Breakout UJ")

is_running = True

pygame.mixer.music.load("sounds/intro.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)


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

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Block(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.image.load("images/blue_block.png").convert()
        self.rect = self.surf.get_rect(center=(x, y))
        # self.surf = pygame.transform.scale(self.surf, (40, 20))


# TODO: Move ball, check borders, speed
class Ball(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.image.load("images/ball.png").convert()
        self.rect = self.surf.get_rect(center=(x, y))

    def update(self):
        pass


def generate_level(level):
    blocks_collection = pygame.sprite.Group()
    # open json file and parse
    with open("levels/" + str(level) + ".json") as json_file:
        data = json.load(json_file)
        for block_data in data['blocks']:
            # load block lives etc.
            new_block = Block(block_data['x'], block_data['y'])
            blocks_collection.add(new_block)
    return blocks_collection


player = Player(610, 940)
ball = Ball(620, 920)

blocks = generate_level(1)

while is_running:
    for events in pygame.event.get():
        if events.type == QUIT:
            is_running = False

    pressed_key = pygame.key.get_pressed()
    player.update(pressed_key)

    screen.fill((0, 0, 0))

    screen.blit(player.surf, player.rect)
    screen.blit(ball.surf, ball.rect)

    for block in blocks:
        screen.blit(block.surf, block.rect)

    if pygame.sprite.spritecollideany(ball, blocks):
        delete_block = pygame.sprite.spritecollideany(ball, blocks)
        delete_block.kill()

    CLOCK.tick(60)
    pygame.display.flip()

pygame.quit()
