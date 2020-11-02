import pygame, sys
from player import Player

pygame.init()
clock = pygame.time.Clock()
screen_w, screen_h = 800, 800

moving_rect = pygame.Rect(350, 350, 100, 100)
x_speed, y_speed = (5, 4)

other_rect = pygame.Rect(300, 600, 200, 100)
other_speed = 2

screen = pygame.display.set_mode((screen_w, screen_h))
display = screen.subsurface(moving_rect.x - 100, moving_rect.y - 100, 300, 300)

def bouncing_rect():
    global x_speed, y_speed, other_speed
    moving_rect.x += x_speed
    moving_rect.y += y_speed

    # collision with screen borders
    if moving_rect.right >= screen_w - 50 or moving_rect.left <= 50:
        x_speed *= -1
    if moving_rect.bottom >= screen_w - 50 or moving_rect.top <= 50:
        y_speed *= -1

    # move other rect
    other_rect.y += other_speed
    if other_rect.top <= 0 or other_rect.bottom >= screen_h:
        other_speed *= -1

    # collision with rect
    collision_tolerance = 10
    if moving_rect.colliderect(other_rect):
        if abs(other_rect.top - moving_rect.bottom) < collision_tolerance and y_speed > 0:
            y_speed *= -1
        if abs(other_rect.bottom - moving_rect.top) < collision_tolerance and y_speed < 0:
            y_speed *= -1
        if abs(other_rect.right - moving_rect.left) < collision_tolerance and x_speed < 0:
            x_speed *= -1
        if abs(other_rect.left - moving_rect.right) < collision_tolerance and x_speed > 0:
            x_speed *= -1

    pygame.draw.rect(screen, (255, 255, 255), moving_rect)
    pygame.draw.rect(screen, (255, 0, 0), other_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    display = screen.subsurface(moving_rect.x - 50, moving_rect.y - 50, 200, 200)
    

    screen.fill((50, 50, 50))
    bouncing_rect()
    pygame.display.flip()
    clock.tick(60)