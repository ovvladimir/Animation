import os
import sys
import random
import pygame

pygame.init()

SIZE_WINDOW = 1000, 500
FPS = 60
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE_WINDOW)
BG = pygame.transform.scale(pygame.image.load('Image/stars.jpg'), SIZE_WINDOW)

# Загружаем все изображения из папки "Image/Bat" и сохраняем в список images_bear
images_bear = []
path = 'Image/Bear'
for file_name in os.listdir(path):
    image = pygame.image.load(f'{path}/{file_name}')
    images_bear.append(image)

images_cat = []
image = pygame.image.load('Image/Cat/1.png')
images_cat.append(image)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.images = img
        self.index = 0  # первый кадр (костюм)
        self.range = len(self.images)
        self.image = self.images[self.index]
        if self.image == images_cat[0]:  # self.images == images_cat
            self.image = pygame.transform.rotozoom(self.image, 5, 0.5)
            self.image = pygame.transform.flip(self.image, False, False)
            self.images[0] = self.image
        self.rect = self.image.get_rect(center=(x // 2, y // 2))

    def update(self):
        # Анимация
        self.index += 0.1
        self.image = self.images[int(self.index % self.range)]
        # для вращения вокруг центра и динамики движения
        self.rect = self.image.get_rect(center=self.rect.center)
        # if self is bear:
        #   self.rect.centerx += 1


bear = AnimatedSprite(*SIZE_WINDOW, img=images_bear)
cat = AnimatedSprite(*SIZE_WINDOW, img=images_cat)
sprites = pygame.sprite.Group(bear, cat)
# sprites.remove(cat)  # спрятать
# sprites.add(cat)  # показать
bearW, bearH = bear.image.get_width(), bear.image.get_height()
catW, catH = cat.image.get_width(), cat.image.get_height()
K = int(bearH * 0.16)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit(0)

    bear.rect.centerx += 1
    cat.rect.centerx = bear.rect.centerx
    cat.rect.bottom = bear.rect.top + K
    if bear.rect.left > SIZE_WINDOW[0]:
        bear.rect.right = 0

    screen.blit(BG, (0, 0))
    sprites.update()
    sprites.draw(screen)
    pygame.display.update()
    clock.tick(FPS)
