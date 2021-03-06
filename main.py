import pygame
import sys

from map import Map
from player import Player

# Pygame Initialization ###
pygame.init()
pygame.display.set_caption("Uhmong-Us")
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN])
###

# Constant Variables ###
SCREEN_X = 1920
SCREEN_Y = 1080
SCREEN_HALF_X = SCREEN_X // 2
SCREEN_HALF_Y = SCREEN_Y // 2
###

# Surface Setup ###
shadow_surface = pygame.Surface((8200, 2200))
shadow_surface.set_colorkey("#123456")
###

# Image Loading & Processing ###
display = pygame.display.set_mode((SCREEN_X, SCREEN_Y), pygame.FULLSCREEN)
visible_map_image = pygame.image.load('images/BCCA_map/BCCA_map_visible.png').convert()
shadow_map_image = pygame.image.load('images/BCCA_map/BCCA_map_shadow.png').convert()

vent_arrow_image = pygame.image.load('images/hud/arrow.png').convert()
vent_arrow_image.set_colorkey((255, 255, 255))
###

# Font Initialization ###
pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 32)
###


def smooth_scroll(game_map_instance, current_x, current_y, smoothness_level):
    current_x -= player_1.half_width
    current_y -= player_1.half_height
    last_x = game_map_instance.x
    last_y = game_map_instance.y
    if game_map_instance.x < current_x:
        if game_map_instance.y < current_y:
            while game_map_instance.x < current_x or game_map_instance.y < current_y:
                game_map_instance.x -= round(game_map_instance.x - current_x, 1) / smoothness_level
                game_map_instance.y -= round(game_map_instance.y - current_y, 1) / smoothness_level
                if game_map_instance.x == last_x and game_map_instance.y == last_y:
                    break
                last_x = game_map_instance.x
                last_y = game_map_instance.y
                redraw_game_window(do_ray_casting)
        else:
            while game_map_instance.x < current_x or game_map_instance.y > current_y:
                game_map_instance.x -= round(game_map_instance.x - current_x, 1) / smoothness_level
                game_map_instance.y -= round(game_map_instance.y - current_y, 1) / smoothness_level
                if game_map_instance.x == last_x and game_map_instance.y == last_y:
                    break
                last_x = game_map_instance.x
                last_y = game_map_instance.y
                redraw_game_window(do_ray_casting)
    else:
        if game_map_instance.y < current_y:
            while game_map_instance.x > current_x or game_map_instance.y < current_y:
                game_map_instance.x -= round(game_map_instance.x - current_x, 1) / smoothness_level
                game_map_instance.y -= round(game_map_instance.y - current_y, 1) / smoothness_level
                if game_map_instance.x == last_x and game_map_instance.y == last_y:
                    break
                last_x = game_map_instance.x
                last_y = game_map_instance.y
                redraw_game_window(do_ray_casting)
        else:
            while game_map_instance.x > current_x or game_map_instance.y > current_y:
                game_map_instance.x -= round(game_map_instance.x - current_x, 1) / smoothness_level
                game_map_instance.y -= round(game_map_instance.y - current_y, 1) / smoothness_level
                if game_map_instance.x == last_x and game_map_instance.y == last_y:
                    break
                last_x = game_map_instance.x
                last_y = game_map_instance.y
                redraw_game_window(do_ray_casting)
    game_map_instance.x = current_x
    game_map_instance.y = current_y


def check_for_collisions(rect, columns):
    return [wall for wall in columns if rect.colliderect(wall)]


def transport_vents(player):
    # vent coordinates are hard coded for now
    if player.in_vent == 1:
        smooth_scroll(game_map, 786, -624, 3)
    elif player.in_vent == 2:
        smooth_scroll(game_map, -839, -299, 3)
    elif player.in_vent == 3:
        smooth_scroll(game_map, -2139, -1174, 3)
    elif player.in_vent == 4:
        smooth_scroll(game_map, -3039, 151, 3)
    elif player.in_vent == 5:
        smooth_scroll(game_map, -4564, -1374, 3)
    elif player.in_vent == 6:
        smooth_scroll(game_map, -5264, 126, 3)
    elif player.in_vent == 7:
        smooth_scroll(game_map, -6239, 51, 3)
    elif player.in_vent == 8:
        smooth_scroll(game_map, -6789, -1149, 3)


def draw_vent_arrows(player, image):
    global left_vent_arrow
    global right_vent_arrow
    if player.in_vent == 1:
        left_vent_arrow = None
        right_vent_arrow = display.blit(pygame.transform.rotate(image, 10.0),
                                        (1050 - player_1.half_width, 540 - player_1.half_height))
    elif player.in_vent == 2:
        left_vent_arrow = display.blit(pygame.transform.rotate(pygame.transform.flip(image, True, False), 10.0),
                                       (870 - player_1.half_width, 570 - player_1.half_height))
        right_vent_arrow = display.blit(pygame.transform.rotate(image, -30.0),
                                        (1030 - player_1.half_width, 605 - player_1.half_height))
    elif player.in_vent == 3:
        left_vent_arrow = display.blit(pygame.transform.rotate(pygame.transform.flip(image, True, False), -30.0),
                                       (870 - player_1.half_width, 510 - player_1.half_height))
        right_vent_arrow = display.blit(pygame.transform.rotate(image, 45.0),
                                        (1020 - player_1.half_width, 490 - player_1.half_height))
    elif player.in_vent == 4:
        left_vent_arrow = display.blit(pygame.transform.rotate(pygame.transform.flip(image, True, False), 45.0),
                                       (870 - player_1.half_width, 605 - player_1.half_height))
        right_vent_arrow = None

    if player.in_vent == 5:
        left_vent_arrow = display.blit(pygame.transform.rotate(image, 80.0),
                                       (970 - player_1.half_width, 450 - player_1.half_height))
        right_vent_arrow = display.blit(pygame.transform.rotate(image, 10.0),
                                        (1050 - player_1.half_width, 540 - player_1.half_height))
    elif player.in_vent == 6:
        left_vent_arrow = display.blit(pygame.transform.rotate(pygame.transform.flip(image, True, False), 80.0),
                                       (935 - player_1.half_width, 645 - player_1.half_height))
        right_vent_arrow = display.blit(pygame.transform.rotate(image, -8.0),
                                        (1045 - player_1.half_width, 570 - player_1.half_height))
    elif player.in_vent == 7:
        left_vent_arrow = display.blit(pygame.transform.rotate(pygame.transform.flip(image, True, False), -8.0),
                                       (870 - player_1.half_width, 545 - player_1.half_height))
        right_vent_arrow = display.blit(pygame.transform.rotate(image, -70.0),
                                        (985 - player_1.half_width, 640 - player_1.half_height))
    elif player.in_vent == 8:
        left_vent_arrow = display.blit(pygame.transform.rotate(pygame.transform.flip(image, True, False), -70.0),
                                       (920 - player_1.half_width, 450 - player_1.half_height))
        right_vent_arrow = display.blit(pygame.transform.rotate(pygame.transform.flip(image, True, False), 10.0),
                                        (870 - player_1.half_width, 570 - player_1.half_height))


def redraw_game_window(ray_casting):
    game_map.draw_map_image(display, shadow_surface, ray_casting, do_draw_collision)
    if do_draw_collision:
        game_map.draw_collision(display)
    if player_1.in_vent:
        draw_vent_arrows(player_1, vent_arrow_image)
    player_1.draw_player(display)
    # player_1.draw_hitboxes(display)
    pygame.display.update()


# mainloop
game_map = Map(visible_map_image, shadow_map_image)
clock = pygame.time.Clock()
player_1 = Player(SCREEN_HALF_X, SCREEN_HALF_Y, (255, 0, 0), game_map, True, 0)
is_ghost = False
do_ray_casting = True
do_draw_collision = True
running_game = True
left_vent_arrow = None
right_vent_arrow = None
while running_game:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v:
                if player_1.in_vent == 0 and player_1.is_traitor:
                    if 886 > game_map.x > 686:
                        if -524 > game_map.y > -724:
                            player_1.in_vent = 1
                    elif -739 > game_map.x > -939:
                        if -199 > game_map.y > -399:
                            player_1.in_vent = 2
                    elif -2039 > game_map.x > -2239:
                        if -1074 > game_map.y > -1274:
                            player_1.in_vent = 3
                    elif -2939 > game_map.x > -3139:
                        if 251 > game_map.y > 51:
                            player_1.in_vent = 4

                    elif -4464 > game_map.x > -4764:
                        if -1274 > game_map.y > -1474:
                            player_1.in_vent = 5
                    elif -5164 > game_map.x > -5364:
                        if 226 > game_map.y > 26:
                            player_1.in_vent = 6
                    elif -6139 > game_map.x > -6339:
                        if 151 > game_map.y > -51:
                            player_1.in_vent = 7
                    elif -6689 > game_map.x > -6889:
                        if -1049 > game_map.y > -1249:
                            player_1.in_vent = 8
                else:
                    player_1.in_vent = 0

            # Code to enable vent travel with WASD ###
            # elif event.key == pygame.K_w:
            #     if player_1.in_vent == 5:
            #         player_1.in_vent = 6
            #     elif player_1.in_vent == 8:
            #         player_1.in_vent = 7

            # elif event.key == pygame.K_s:
            #     if player_1.in_vent == 6:
            #         player_1.in_vent = 5
            #     elif player_1.in_vent == 7:
            #         player_1.in_vent = 8

            # elif event.key == pygame.K_a:
            #     if player_1.in_vent == 2:
            #         player_1.in_vent = 1
            #     elif player_1.in_vent == 3:
            #         player_1.in_vent = 2
            #     elif player_1.in_vent == 4:
            #         player_1.in_vent = 3
            #     elif player_1.in_vent == 8:
            #         player_1.in_vent = 5
            #     elif player_1.in_vent == 7:
            #         player_1.in_vent = 6

            # elif event.key == pygame.K_d:
            #     if player_1.in_vent == 1:
            #         player_1.in_vent = 2
            #     elif player_1.in_vent == 2:
            #         player_1.in_vent = 3
            #     elif player_1.in_vent == 3:
            #         player_1.in_vent = 4
            #     elif player_1.in_vent == 5:
            #         player_1.in_vent = 8
            #     elif player_1.in_vent == 6:
            #         player_1.in_vent = 7
            ###

            elif event.key == pygame.K_x:
                is_ghost = not is_ghost
            elif event.key == pygame.K_LEFT:
                game_map.x += 1
            elif event.key == pygame.K_RIGHT:
                game_map.x -= 1
            elif event.key == pygame.K_UP:
                game_map.y += 1
            elif event.key == pygame.K_DOWN:
                game_map.y -= 1
            elif event.key == pygame.K_c:
                print(f"{game_map.x}, {game_map.y}")
            elif event.key == pygame.K_r:
                do_ray_casting = not do_ray_casting
            elif event.key == pygame.K_l:
                do_draw_collision = not do_draw_collision

            if player_1.in_vent != 0:
                transport_vents(player_1)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if event.button == 1:
                if player_1.in_vent == 1:
                    if right_vent_arrow:
                        if right_vent_arrow.collidepoint(mouse_position):
                            player_1.in_vent = 2
                elif player_1.in_vent == 2:
                    if left_vent_arrow:
                        if left_vent_arrow.collidepoint(mouse_position):
                            player_1.in_vent = 1
                    if right_vent_arrow:
                        if right_vent_arrow.collidepoint(mouse_position):
                            player_1.in_vent = 3
                elif player_1.in_vent == 3:
                    if left_vent_arrow:
                        if left_vent_arrow.collidepoint(mouse_position):
                            player_1.in_vent = 2
                    if right_vent_arrow:
                        if right_vent_arrow.collidepoint(mouse_position):
                            player_1.in_vent = 4
                elif player_1.in_vent == 4:
                    if left_vent_arrow:
                        if left_vent_arrow.collidepoint(mouse_position):
                            player_1.in_vent = 3
                elif player_1.in_vent == 5:
                    if left_vent_arrow:
                        if left_vent_arrow.collidepoint(mouse_position):
                            player_1.in_vent = 6
                    if right_vent_arrow:
                        if right_vent_arrow.collidepoint(mouse_position):
                            player_1.in_vent = 8
                elif player_1.in_vent == 6:
                    if left_vent_arrow:
                        if left_vent_arrow.collidepoint(mouse_position):
                            player_1.in_vent = 5
                    if right_vent_arrow:
                        if right_vent_arrow.collidepoint(mouse_position):
                            player_1.in_vent = 7
                elif player_1.in_vent == 7:
                    if left_vent_arrow:
                        if left_vent_arrow.collidepoint(mouse_position):
                            player_1.in_vent = 6
                    if right_vent_arrow:
                        if right_vent_arrow.collidepoint(mouse_position):
                            player_1.in_vent = 8
                elif player_1.in_vent == 8:
                    if left_vent_arrow:
                        if left_vent_arrow.collidepoint(mouse_position):
                            player_1.in_vent = 7
                    if right_vent_arrow:
                        if right_vent_arrow.collidepoint(mouse_position):
                            player_1.in_vent = 5
                if player_1.in_vent != 0:
                    transport_vents(player_1)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        if player_1.in_vent == 0:
            for pixel in range(game_map.y_velocity):
                if not (check_for_collisions(player_1.w_hitbox, game_map.get_wall_rects) and not is_ghost):
                    game_map.y += 1
    if keys[pygame.K_a]:
        if player_1.in_vent == 0:
            for pixel in range(game_map.x_velocity):
                if not (check_for_collisions(player_1.a_hitbox, game_map.get_wall_rects) and not is_ghost):
                    game_map.x += 1
    if keys[pygame.K_s]:
        if player_1.in_vent == 0:
            for pixel in range(game_map.y_velocity):
                if not (check_for_collisions(player_1.s_hitbox, game_map.get_wall_rects) and not is_ghost):
                    game_map.y -= 1
    if keys[pygame.K_d]:
        if player_1.in_vent == 0:
            for pixel in range(game_map.x_velocity):
                if not (check_for_collisions(player_1.d_hitbox, game_map.get_wall_rects) and not is_ghost):
                    game_map.x -= 1

    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    redraw_game_window(do_ray_casting)

    clock.tick(60)
pygame.quit()
sys.exit()
