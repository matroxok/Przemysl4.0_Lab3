import pygame
import random
import RPi.GPIO as GPIO
from sensor import sensor_init

SW1, SW2, SW4 = 17, 4, 2
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

vl, dev = sensor_init()
pygame.init()
WIDTH, HEIGHT = 600, 400
GROUND = 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino run")
font = pygame.font.SysFont("Arial", 30)
clock = pygame.time.Clock()

dino_y = GROUND - 40
vel = 0
cactus_x = WIDTH
score = 0
speed = 5
game_over = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if GPIO.input(SW4) == 0:
        running = False

    if not game_over:
        distance = min(vl.get_distance(dev), 255)
        speed = 5 + (255 - distance) // 20

        if GPIO.input(SW1) == 0 and dino_y == GROUND - 40:
            vel = -15
        vel += 1
        dino_y += vel
        if dino_y > GROUND - 40:
            dino_y = GROUND - 40
            vel = 0

        cactus_x -= speed
        if cactus_x < -20:
            cactus_x = WIDTH + random.randint(0, 200)
            score += 1
    else:
        if GPIO.input(SW2) == 0:
            dino_y = GROUND - 40
            vel = 0
            cactus_x = WIDTH
            score = 0
            game_over = False

    dino = pygame.Rect(80, dino_y, 40, 40)
    cactus = pygame.Rect(cactus_x, GROUND - 50, 20, 50)
    if dino.colliderect(cactus):
        game_over = True

    screen.fill((135, 206, 235))
    pygame.draw.rect(screen, (240, 230, 140), (0, GROUND, WIDTH, HEIGHT - GROUND))
    pygame.draw.rect(screen, (0, 150, 0), dino)
    pygame.draw.rect(screen, (200, 0, 0), cactus)
    screen.blit(font.render(f"Punkty: {score}  Predkosc: {speed}", True, (0, 0, 0)), (10, 10))
    if game_over:
        screen.blit(font.render("KONIEC - SW2 restart, SW4 wyjscie", True, (200, 0, 0)), (60, 150))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
GPIO.cleanup()