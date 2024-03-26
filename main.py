import pygame
import random
import os

WIDTH = 500
HEIGHT = 600
FPS = 50

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Инициализация pygame и создание окна
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
icon = pygame.image.load("img/tir-game-icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Игра Тир")
clock = pygame.time.Clock()


# Функция для загрузки изображения
def load_image(name):
    path = os.path.join('img', name)
    try:
        image = pygame.image.load(path).convert_alpha()
    except pygame.error as e:
        print(f'Cannot load image: {name}')
        raise SystemExit(e)
    return image


# Спрайт мишени
mob_image = load_image('apple-50.png')


def create_mob():
    apple = pygame.sprite.Sprite()
    apple.image = mob_image
    apple.rect = apple.image.get_rect()
    apple.rect.x = random.randrange(WIDTH - apple.rect.width)
    apple.rect.y = random.randrange(-100, -40)
    apple.speedy = random.randrange(1, 8)
    apple.speedx = random.randrange(-3, 3)
    all_sprites.add(apple)
    mobs.add(apple)


def update_mob(mob):
    mob.rect.x += mob.speedx
    mob.rect.y += mob.speedy
    if mob.rect.top > HEIGHT + 10 or mob.rect.left < -25 or mob.rect.right > WIDTH + 20:
        mob.rect.x = random.randrange(WIDTH - mob.rect.width)
        mob.rect.y = random.randrange(-100, -40)
        mob.speedy = random.randrange(1, 8)


def shoot(x, y):
    bullet = pygame.sprite.Sprite()
    bullet.image = pygame.Surface((10, 20))
    bullet.image.fill(YELLOW)
    bullet.rect = bullet.image.get_rect()
    bullet.rect.bottom = y
    bullet.rect.centerx = x
    bullet.speedy = -10
    all_sprites.add(bullet)
    bullets.add(bullet)


def update_bullet(bullet):
    bullet.rect.y += bullet.speedy
    if bullet.rect.bottom < 0:
        bullet.kill()


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = pygame.sprite.Sprite()
player.image = pygame.Surface((40, 25))
player.image.fill(GREEN)
player.rect = player.image.get_rect()
player.rect.centerx = WIDTH / 2
player.rect.bottom = HEIGHT - 10
player.speedx = 0

all_sprites.add(player)

for i in range(8):
    create_mob()

color = (186, 184, 168)
counter = 0
font_size = 30
font = pygame.font.Font(None, font_size)
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shoot(player.rect.centerx, player.rect.top)

    player.speedx = 0
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_LEFT]:
        player.speedx = -8
    if keystate[pygame.K_RIGHT]:
        player.speedx = 8
    player.rect.x += player.speedx
    if player.rect.right > WIDTH:
        player.rect.right = WIDTH
    if player.rect.left < 0:
        player.rect.left = 0

    for mob in mobs:
        update_mob(mob)

    for bullet in bullets:
        update_bullet(bullet)

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        counter += 1
        create_mob()

    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False

    screen.fill(color)
    all_sprites.draw(screen)
    counter_text = font.render(f"Сбито яблок: {counter}", True, YELLOW)
    screen.blit(counter_text, (10, 10))
    pygame.display.flip()

pygame.quit()
