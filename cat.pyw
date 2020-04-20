import pygame
import os
import sys
import random
from colors import COLOR

os.environ['SDL_VIDEO_CENTERED'] = '1'
COLOR_CAT = ['red', 'green', 'royal blue', 'orange', 'olive drab', 'sienna4']

pygame.init()
SIZE_WINDOW = WIDTH_WIN, HEIGHT_WIN = 960, 720
BACKGROUND_COLOR = (100, 0, 255)
screen = pygame.display.set_mode(SIZE_WINDOW)  # pygame.NOFRAME

userevent = pygame.USEREVENT
pygame.time.set_timer(userevent, 60000)

FPS = 60
clock = pygame.time.Clock()
alpha = 255
jump = [False]
down = [False]
somersault = [False]
menu_on_off = [True, False]
day_night = [False, True]
SPEED = 0
GRAVI = 1


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


class Menu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.text = pygame.font.SysFont('Arial', 22)
        self.text_list = [
            'space - somersault', 'm   -   menu', 'c    -   color selection',
            'z    -   -transparency', 'x    -   +transparency',
            '↓    -   to lie', '↑    -    jamp', '→  -   go', '←  -   stop']
        self.text_pos = [10, 0]
        self.width_string = []
        for string in self.text_list:
            self.width_string.append(self.text.size(string)[0])
        self.max_width_string = max(self.width_string)
        self.max_height_string = self.text.get_height() + self.text.get_descent()
        self.top = self.text.get_height() - self.text.get_ascent()
        self.image = pygame.Surface((
            self.text_pos[0] + self.max_width_string,
            self.text_pos[1] + self.top + len(self.text_list) * self.max_height_string),
            flags=pygame.SRCALPHA)
        for txt in self.text_list:
            self.text_render = self.text.render(txt, True, (255, 255, 255), None)
            self.image.blit(self.text_render, self.text_pos)
            self.text_pos[1] += self.max_height_string
        self.rect = self.image.get_rect(topleft=(0, 0))


class Earth(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.images = img
        self.index = 0
        self.range = len(self.images)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(int(x), int(y)))

    def update(self):
        if self == background1 or self == background2:
            self.rect.x -= SPEED * 2
        else:
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
        if somersault[0]:
            self.velocity.y = -5
            if self.rot > -300:
                self.rot -= 10
            else:
                self.rot = 0
                somersault[0] = False
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
        while pygame.sprite.spritecollideany(self, collideGroup, pygame.sprite.collide_rect_ratio(0.97)):
            self.position.y -= GRAVI
            self.velocity.y = 0
            self.rect.centery = int(self.position.y)

            if jump[0]:
                self.velocity.y = -15
                self.velocity.x = 3
            else:
                self.velocity.x = 0


menu = Menu()
cat = AnimatedSprite(WIDTH_WIN // 2, HEIGHT_WIN // 2, images_cat)

earth1 = Earth(0, HEIGHT_WIN - images_earth[0].get_height(), images_earth)
earth2 = Earth(WIDTH_WIN, HEIGHT_WIN - images_earth[0].get_height(), images_earth)

images_bg[0] = pygame.transform.scale(images_bg[0], (WIDTH_WIN, HEIGHT_WIN - 200))
background1 = Earth(0, 0, images_bg)
background2 = Earth(WIDTH_WIN, 0, images_bg)

sprites = pygame.sprite.LayeredUpdates()
sprites.add(earth1, earth2, layer=1)
sprites.add(menu, layer=2)
sprites.add(cat, layer=3)
collideGroup = pygame.sprite.Group(earth1, earth2)

obj = [pygame.Surface((200, 20), pygame.SRCALPHA)]
obj[0].fill((200, 200, 20, 255))
objW, objH = obj[0].get_width(), obj[0].get_height()
for i in range(3):
    obj_sprite = Earth(WIDTH_WIN + objW * i, HEIGHT_WIN / 2.2 - objH * i * 3, obj)
    sprites.add(obj_sprite, layer=1)
    collideGroup.add(obj_sprite)
obj_sprite = sprites.get_sprites_from_layer(1)[-1]
'''
collideColor = images_earth[0].get_at((30, 30))
for sp in collideGroup:
    # collideColor = sp.image.get_at((10, 10))
    sp.mask = pygame.mask.from_threshold(sp.image, collideColor, (1, 1, 1, 255))
# в def gravitation()
# pygame.sprite.spritecollideany(self, collideGroup, pygame.sprite.collide_mask)
'''

run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        elif e.type == userevent:
            day_night.reverse()
            if day_night[0]:
                sprites.add(background1, background2, layer=0)
            elif not day_night[0]:
                sprites.remove(background1, background2)
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                run = False
            elif e.key == pygame.K_UP:
                jump[0] = True
            elif e.key == pygame.K_SPACE:
                somersault[0] = True
            elif e.key == pygame.K_DOWN:
                down[0] = True
            elif e.key == pygame.K_RIGHT:
                SPEED = 1
            elif e.key == pygame.K_LEFT:
                SPEED = 0
            elif e.key == pygame.K_c and not somersault[0]:
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
            elif e.key == pygame.K_m:
                menu_on_off.reverse()
                if menu_on_off[0]:
                    sprites.add(menu, layer=2)
                elif not menu_on_off[0]:
                    sprites.remove(menu)
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
