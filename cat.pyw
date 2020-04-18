import pygame
import os
import sys
import random
from colors import COLOR

os.environ['SDL_VIDEO_CENTERED'] = '1'
COLOR_CAT = ['red', 'green', 'royal blue', 'orange', 'olive drab', 'sienna4']
'''
userevent = pygame.USEREVENT
pygame.time.set_timer(userevent, 3000)
'''

pygame.init()
SIZE_WINDOW = WIDTH_WIN, HEIGHT_WIN = 960, 720
BACKGROUND_COLOR = (100, 0, 255)
screen = pygame.display.set_mode(SIZE_WINDOW)  # pygame.NOFRAME

FPS = 60
clock = pygame.time.Clock()
jump = [False]
down = [False]
rotate_jump = [False]
SPEED = 0
GRAVI = 1
alpha = 255


def load_images(path) -> list:
    images = []
    for file_name in os.listdir(path):
        image = pygame.image.load(path + os.sep + file_name)
        images.append(image)
    return images


# images_cat = load_images('Image/Cat')
images_earth = load_images('Image/Earth')
images_bg = load_images('Image/BG')
imCat = load_images('Image/CatTexture')
imCat[0] = imCat[0].convert()  # для установки прозрачности клавишами z и x
R = [168, 165, 170, 173, 170, 168, 170, 174, 172, 159, 167, 168]
images_cat = []
h = imCat[0].get_height()
for n, r in enumerate(R):
    images_cat.append(imCat[0].subsurface((sum(R[:n]), 0, r, h)))


class Background(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Image/BG/bg.jpg')
        self.image = pygame.transform.scale(self.image, SIZE_WINDOW)
        self.rect = self.image.get_rect(topleft=(int(x), int(y)))


class Earth(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.images = img
        self.index = 0
        self.range = len(self.images)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(int(x), int(y)))

    def update(self):
        self.rect.x -= SPEED
        if self.rect.x <= -WIDTH_WIN:
            self.rect.x = WIDTH_WIN
            self.index = random.randrange(self.range)
            self.image = self.images[self.index]


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.images = img
        [self_image.set_colorkey((0, 0, 0)) for self_image in self.images]
        self.index = 0
        self.range = len(self.images[:-4])
        self.range_jump_up = -4
        self.range_jump_down = -3
        self.range_down = -2
        self.range_stop = -1
        self.rot = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2()
        self.width = self.image.get_width() // 2
        # pygame.draw.ellipse(self.image.copy(), (0, 0, 0, 0), self.rect)

    def update(self):
        if rotate_jump[0]:
            self.velocity.y = -5
            if self.rot > -300:
                self.rot -= 10
            else:
                self.rot = 0
                rotate_jump[0] = False
            self.images = [pygame.transform.rotate(image, self.rot) for image in images_cat]
        self.index += 0.1
        self.image = self.images[int(self.index % self.range)]
        if down[0]:
            self.image = self.images[self.range_down]
        elif self.velocity.y < 0:
            self.image = self.images[self.range_jump_up]
        elif self.velocity.y > 3:
            self.image = self.images[self.range_jump_down]
        elif SPEED == 0:
            self.image = self.images[self.range_stop]

        self.position += self.velocity
        self.rect = self.image.get_rect(center=(int(self.position.x), int(self.position.y)))

        self.position.x += SPEED
        if self.position.x > WIDTH_WIN + self.width:
            self.position.x = -self.width
        '''
        self.rect.centerx += SPEED
        if self.rect.left > WIDTH_WIN:
            self.rect.right = 0
        self.position.x = self.rect.centerx
        '''
        self.image.set_alpha(alpha)  # прозрачность изображения
        self.gravitation()  # гравитация

    def gravitation(self):
        self.velocity.y += GRAVI
        while pygame.sprite.spritecollideany(self, collidGroup, pygame.sprite.collide_rect_ratio(0.97)):
            self.position.y -= GRAVI
            self.velocity.y = 0
            self.rect.centery = int(self.position.y)

            if jump[0]:
                self.velocity.y = -15
                self.velocity.x = 3
            else:
                self.velocity.x = 0


# bg1 = Background(0, 0)
images_bg[0] = pygame.transform.scale(images_bg[0], (WIDTH_WIN, HEIGHT_WIN - 200))
bg1 = Earth(0, 0, images_bg)
bg2 = Earth(WIDTH_WIN, 0, images_bg)

cat = AnimatedSprite(WIDTH_WIN // 2, HEIGHT_WIN // 2, images_cat)

earth1 = Earth(0, HEIGHT_WIN - images_earth[0].get_height(), images_earth)
earth2 = Earth(WIDTH_WIN, HEIGHT_WIN - images_earth[0].get_height(), images_earth)

sprites = pygame.sprite.Group(bg1, bg2, earth1, earth2)
collidGroup = pygame.sprite.Group(earth1, earth2)

obj = [pygame.Surface((200, 20), pygame.SRCALPHA)]
obj[0].fill((200, 200, 20, 255))
objW, objH = obj[0].get_width(), obj[0].get_height()
for i in range(3):
    obj_sprite = Earth(WIDTH_WIN + objW * i, HEIGHT_WIN / 2.2 - objH * i * 3, obj)
    sprites.add(obj_sprite)
    collidGroup.add(obj_sprite)

sprites.add(cat)
sprites.remove(bg1, bg2)

run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                run = False
            elif e.key == pygame.K_UP:
                jump[0] = True
            elif e.key == pygame.K_SPACE:
                rotate_jump[0] = True
            elif e.key == pygame.K_DOWN:
                down[0] = True
            elif e.key == pygame.K_RIGHT:
                SPEED = 1
            elif e.key == pygame.K_LEFT:
                SPEED = 0
            elif e.key == pygame.K_c and not rotate_jump[0]:  # e.type == userevent:
                clr = random.choice(COLOR_CAT)  # цвет кота
                for c, cat_color in enumerate(cat.images):
                    originalColor = cat_color.get_at((90, 105 if c == 10 else 40))
                    ar = pygame.PixelArray(cat_color)
                    ar.replace(originalColor, pygame.Color(clr), 0.1)
                    del ar
                    images_cat = cat.images
            elif e.key == pygame.K_z:
                alpha -= 25 if alpha > 5 else 5 if alpha > 0 else 0
            elif e.key == pygame.K_x:
                alpha += 25 if alpha < 250 else 5 if alpha < 255 else 0
        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_DOWN or e.key == pygame.K_UP:
                down[0] = False
                jump[0] = False

    if obj_sprite.rect.right == 0:
        obj_sprite.image.fill(pygame.Color(random.choice(COLOR)))

    screen.fill(BACKGROUND_COLOR)
    sprites.update()
    sprites.draw(screen)
    pygame.display.update()
    pygame.display.set_caption(f'CAT   FPS: {int(clock.get_fps())}')
    clock.tick(FPS)

sys.exit(0)
