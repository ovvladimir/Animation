import pygame
import os
import sys
import random
import ast
from colors import COLOR


def load_images(path) -> list:
    for file_name in os.listdir(path):
        images_list.append(pygame.image.load(path + os.sep + file_name))


def mask():
    for sp in collideGroup:
        # collideColor = sp.image.get_at((30, 15))
        sp.mask = pygame.mask.from_threshold(sp.image, collideColor, (1, 1, 1, 255))


class Menu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.text_list = [
            'space - somersault', 'm   -   menu', 'c    -   color selection',
            'z    -   -transparency', 'x    -   +transparency',
            '↓    -   to lie', '↑    -    jamp', '→  -   go', '←  -   stop']
        self.text_pos = [10, 0]
        self.width_string = []
        for string in self.text_list:
            self.width_string.append(text.size(string)[0])
        self.max_width_string = max(self.width_string)
        self.max_height_string = text.get_height() + text.get_descent()
        self.top = text.get_height() - text.get_ascent()
        self.image = pygame.Surface((
            self.text_pos[0] + self.max_width_string,
            self.text_pos[1] + self.top + len(self.text_list) * self.max_height_string),
            flags=pygame.SRCALPHA)
        for txt in self.text_list:
            self.text_render = text.render(txt, True, WHITE, None)
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
        self.rect.x -= SPEED
        if self.rect.x <= -WIDTH_WIN:
            self.rect.x = WIDTH_WIN
            self.index = random.randrange(self.range)
            self.image = self.images[self.index]
            mask()


class Stars(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed = random.randint(1, 2)
        self.size = random.randint(1, 3)
        self.pos = random.randrange(WIDTH_WIN), random.randrange(HEIGHT_WIN - int(he * .7))
        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, pygame.Color(
            random.choice(COLOR[238:262])), [self.size, self.size], self.size)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = WIDTH_WIN


class Bat(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.images = img
        self.time = 0
        self.range = len(self.images)
        self.image = self.images[self.time]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = pygame.math.Vector2(self.rect.center)
        self.bat_zoom = .4
        self.zoom = 0

    def update(self):
        bat_angle = self.direction.angle_to(cat.position - self.direction)
        self.images = [pygame.transform.rotozoom(
            image, 180 - bat_angle, self.bat_zoom) for image in images_bat]
        self.time += 0.2
        self.image = self.images[int(self.time % self.range)]
        self.rect = self.image.get_rect(center=self.rect.center)
        if self.zoom == 0:
            self.bat_zoom += .001
            if self.bat_zoom > .7:
                self.zoom = 1
        elif self.zoom == 1:
            self.bat_zoom -= .001
            if self.bat_zoom < .4:
                self.zoom = 0


class Bat2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = images_list[3]
        self.rect = self.image.get_rect(
            bottomleft=(random.randint(WIDTH_WIN, WIDTH_WIN * 2), HEIGHT_WIN - he))
        self.group = pygame.sprite.GroupSingle(self)
        self.vel = 0
        self.score = 0

    def gravi(self):
        self.vel += GRAVI if self.rect.left < WIDTH_WIN else 0
        self.rect.centery += self.vel
        while pygame.sprite.spritecollideany(
                self, collideGroup, pygame.sprite.collide_mask):
            self.rect.centery -= GRAVI
            self.vel = 0

    def update(self):
        self.gravi()
        self.rect.centerx -= SPEED * 2
        if self.rect.right < 0:
            self.rect.left = random.randint(WIDTH_WIN, WIDTH_WIN * 2)
        if pygame.sprite.spritecollideany(
                cat, self.group, pygame.sprite.collide_circle_ratio(0.75)):
            self.rect.left = random.randint(WIDTH_WIN, WIDTH_WIN * 2)
            self.score += 1


class Cat(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.images = img
        [self_image.set_colorkey((0, 0, 0)) for self_image in self.images]
        self.time = 0
        self.range = len(self.images[:-4])
        self.range_jump_up = -4
        self.range_jump_down = -3
        self.range_down = -2
        self.range_stop = -1
        self.rot = 0
        self.image = self.images[self.time]
        self.rect = self.image.get_rect(center=(x, y))
        self.position = pygame.math.Vector2(self.rect.center)
        self.velocity = pygame.math.Vector2()
        self.velocity.x = SPEED
        self.width = self.image.get_width() // 2

    def flip(self):
        self.velocity.y = -5
        if self.rot > -300:
            self.rot -= 10
        else:
            self.rot = 0
            somersault[0] = False
        self.images = [pygame.transform.rotate(image, self.rot) for image in images_cat]

    def animation(self):
        self.time += dt
        self.image = self.images[int(self.time % self.range)]
        if down[0]:
            self.image = self.images[self.range_down]
        elif self.velocity.y < 0:
            self.image = self.images[self.range_jump_up]
        elif self.velocity.y > 4:
            self.image = self.images[self.range_jump_down]
        elif SPEED == 0:
            self.image = self.images[self.range_stop]

    def gravitation(self):
        self.velocity.y += GRAVI
        self.position += self.velocity

    def antigravity(self):
        # pygame.sprite.collide_mask
        while pygame.sprite.spritecollideany(
                self, collideGroup, pygame.sprite.collide_rect_ratio(0.97)):
            self.position.y -= GRAVI
            self.velocity.y = 0
            self.rect.centery = int(self.position.y)

            if jump[0]:
                self.velocity.y = -15
                self.velocity.x = 3
            else:
                self.velocity.x = SPEED

    def update(self):
        if somersault[0]:
            self.flip()
        self.animation()
        self.image.set_alpha(alpha)  # прозрачность изображения

        self.gravitation()
        if self.position.x > WIDTH_WIN + self.width:
            self.position.x = -self.width
        self.rect = self.image.get_rect(center=list(map(int, self.position)))
        self.antigravity()


'-----------------------------------------------------------------------------'

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
WIDTH_WIN, HEIGHT_WIN = 960, 720
DAY_BG_COLOR, NIGHT_BG_COLOR = (100, 0, 255), (5, 0, 50)
screen = pygame.display.set_mode((WIDTH_WIN, HEIGHT_WIN))  # pygame.NOFRAME
pygame.mouse.set_visible(False)
text = pygame.font.SysFont('Arial', 22)

userevent = pygame.USEREVENT
pygame.time.set_timer(userevent, 60000)

key = {
    'type_quit': pygame.QUIT,
    'type_down': pygame.KEYDOWN,
    'type_up': pygame.KEYUP,
    'escape': pygame.K_ESCAPE,
    'up': pygame.K_UP,
    'space': pygame.K_SPACE,
    'down': pygame.K_DOWN,
    'right': pygame.K_RIGHT,
    'left': pygame.K_LEFT,
    'c': pygame.K_c,
    'z': pygame.K_z,
    'x': pygame.K_x,
    'm': pygame.K_m
}

FPS = 60
clock = pygame.time.Clock()
alpha = 255
jump = [False]
down = [False]
somersault = [False]
menu_on_off = [True, False]
day_night = [False, True]
WHITE = (255, 255, 255)
SPEED = 0
GRAVI = 1
NUMBER_OF_STARS = 150
COLOR_CAT = ['red', 'green', 'royal blue', 'orange', 'olive drab', 'sienna4']

images_list = []
load_images('Images')

images_list[1] = images_list[1].convert()  # для установки прозрачности
images_cat = []
images_bat = []
with open('texture.txt') as f:
    for lines in f:
        line = ast.literal_eval(lines)
        if 'cat' in line.keys():
            X, Y, W, h = line[str(*line.keys())].values()
            for n, w in enumerate(W):
                images_cat.append(images_list[1].subsurface((X[n], Y[n], w, h)))
        elif 'bat' in line.keys():
            X, Y, W, h = line[str(*line.keys())].values()
            for n, w in enumerate(W):
                images_bat.append(images_list[0].subsurface((X[n], Y[n], w, h)))
            height_bat = h

we, he = images_list[2].get_width() // 2, images_list[2].get_height() // 2
images_earth = [
    images_list[2].subsurface((0, 0, we, he)),
    images_list[2].subsurface((we, 0, we, he)),
    images_list[2].subsurface((0, he, we, he)),
    images_list[2].subsurface((we, he, we, he))
]

menu = Menu()
cat = Cat(WIDTH_WIN // 2, HEIGHT_WIN // 2, images_cat)
bat = Bat(WIDTH_WIN - height_bat, 0, images_bat)
bat2 = Bat2()

earth1 = Earth(0, HEIGHT_WIN - he, images_earth)
earth2 = Earth(WIDTH_WIN, HEIGHT_WIN - he, images_earth)

sprites = pygame.sprite.LayeredUpdates()
sprites.add(earth1, earth2, layer=1)
sprites.add(menu, layer=2)
sprites.add(bat, layer=2)
sprites.add(cat, bat2, layer=3)
collideGroup = pygame.sprite.Group(earth1, earth2)

for _ in range(NUMBER_OF_STARS):
    stars = Stars()
    sprites.add(stars, layer=0)
stars_list = sprites.remove_sprites_of_layer(0)

obj = [pygame.Surface((200, 20), pygame.SRCALPHA)]
obj[0].fill((200, 200, 20, 255))
objW, objH = obj[0].get_width(), obj[0].get_height()
for i in range(3):
    obj_sprite = Earth(WIDTH_WIN + objW * i, HEIGHT_WIN / 2.2 - objH * i * 3, obj)
    sprites.add(obj_sprite, layer=1)
    collideGroup.add(obj_sprite)
obj_sprite = sprites.get_sprites_from_layer(1)[-1]

collideColor = images_list[2].get_at((30, 30))
mask()

run = True
while run:
    dt = clock.tick(FPS) / 150.
    for e in pygame.event.get():
        if e.type == key['type_quit']:
            run = False
        elif e.type == userevent:
            day_night.reverse()
            if day_night[0]:
                sprites.add(stars_list, layer=0)
            elif not day_night[0]:
                sprites.remove_sprites_of_layer(0)
        elif e.type == key['type_down']:
            if e.key == key['escape']:
                run = False
            elif e.key == key['up']:
                jump[0] = True
            elif e.key == key['space']:
                somersault[0] = True
            elif e.key == key['down']:
                down[0] = True
            elif e.key == key['right']:
                SPEED = 1
            elif e.key == key['left']:
                SPEED = 0
            elif e.key == key['c'] and not somersault[0]:
                clr = random.choice(COLOR_CAT)  # цвет кота
                for c, cat_color in enumerate(cat.images):
                    originalColor = cat_color.get_at((90, 108 if c == 10 else 40))
                    ar = pygame.PixelArray(cat_color)
                    ar.replace(originalColor, pygame.Color(clr), 0.1)
                    del ar
                    images_cat = cat.images
            elif e.key == key['z']:
                alpha -= 25 if alpha > 5 else 5 if alpha > 0 else 0
            elif e.key == key['x']:
                alpha += 25 if alpha < 250 else 5 if alpha < 255 else 0
            elif e.key == key['m']:
                menu_on_off.reverse()
                if menu_on_off[0]:
                    sprites.add(menu, layer=2)
                elif not menu_on_off[0]:
                    sprites.remove(menu)
        elif e.type == key['type_up']:
            if e.key == key['down'] or e.key == key['up']:
                down[0] = False
                jump[0] = False

    if obj_sprite.rect.right == 0:
        obj_sprite.image.fill(pygame.Color(random.choice(COLOR)))

    sprites.update()
    screen.fill(NIGHT_BG_COLOR if day_night[0] else DAY_BG_COLOR)
    screen.blit(
        text.render(f'{bat2.score}', True, WHITE, None), (WIDTH_WIN // 2, 5))
    sprites.draw(screen)
    pygame.display.update()
    pygame.display.set_caption(f'CAT   FPS: {int(clock.get_fps())}')

sys.exit(0)
