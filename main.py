import pygame
import sys
import time

from constants import *
from map import Map
from player import Player
import tasks

# Pygame Initialization ###
pygame.init()
pygame.display.set_caption("Uhmong-Us")
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN])
###

# Image Loading & Processing ###
display = pygame.display.set_mode(
    (SCREEN_X, SCREEN_Y),
    pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.SCALED  # for non-1080p screens
)

visible_map_image = pygame.image.load('images/BCCA_map/BCCA_map_visible.png').convert()
shadow_map_image = pygame.image.load('images/BCCA_map/BCCA_map_shadow.png').convert()

task_surface = pygame.Surface((SCREEN_X, SCREEN_Y))
task_surface.set_colorkey((18, 52, 86))

vent_arrow_image = pygame.image.load('images/hud/arrow.png').convert()
vent_arrow_image.set_colorkey((255, 255, 255))
###

# Surface Setup ###
shadow_surface = pygame.Surface((shadow_map_image.get_width(), shadow_map_image.get_height()))
shadow_surface.set_colorkey("#123456")

shadow_limiter_surface = pygame.Surface((SCREEN_X, SCREEN_Y))
shadow_limiter_surface.set_colorkey("#098765")
###

# Font Initialization ###
pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)
###


def smooth_scroll(game_map_instance: Map, current_x: int, current_y: int, smoothness_level: int, shadow_range: int):
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
                redraw_game_window(shadow_range)
        else:
            while game_map_instance.x < current_x or game_map_instance.y > current_y:
                game_map_instance.x -= round(game_map_instance.x - current_x, 1) / smoothness_level
                game_map_instance.y -= round(game_map_instance.y - current_y, 1) / smoothness_level
                if game_map_instance.x == last_x and game_map_instance.y == last_y:
                    break
                last_x = game_map_instance.x
                last_y = game_map_instance.y
                redraw_game_window(shadow_range)
    else:
        if game_map_instance.y < current_y:
            while game_map_instance.x > current_x or game_map_instance.y < current_y:
                game_map_instance.x -= round(game_map_instance.x - current_x, 1) / smoothness_level
                game_map_instance.y -= round(game_map_instance.y - current_y, 1) / smoothness_level
                if game_map_instance.x == last_x and game_map_instance.y == last_y:
                    break
                last_x = game_map_instance.x
                last_y = game_map_instance.y
                redraw_game_window(shadow_range)
        else:
            while game_map_instance.x > current_x or game_map_instance.y > current_y:
                game_map_instance.x -= round(game_map_instance.x - current_x, 1) / smoothness_level
                game_map_instance.y -= round(game_map_instance.y - current_y, 1) / smoothness_level
                if game_map_instance.x == last_x and game_map_instance.y == last_y:
                    break
                last_x = game_map_instance.x
                last_y = game_map_instance.y
                redraw_game_window(shadow_range)
    game_map_instance.x = current_x
    game_map_instance.y = current_y


def check_for_collisions(rect: pygame.Rect, wall_rects: list[pygame.Rect]):
    return [wall for wall in wall_rects if rect.colliderect(wall)]


def start_task():
    for task_info in game_map.get_task_rects:
        if player_1.general_hitbox.colliderect(task_info[0]):
            player_1.in_task = task_info[1]
            if task_info[1] == "Clean Windows":
                clean_windows_task.renew_task_surface()
            elif task_info[1] == "Wipe down Tables":
                wipe_tables_task.renew_task_surface()
            elif task_info[1] == "Reset Wifi":
                reset_wifi_task.renew_task_surface()
            elif task_info[1] == "Plug-In Laptops":
                plug_in_laptops_task.renew_task_surface()
            elif task_info[1] == "Check Temperature":
                check_temperature_task.renew_task_surface()
            return

    player_1.in_task = "None"


def transport_vents(player: Player):
    # vent coordinates are hard coded for now
    if player.in_vent == 1:
        smooth_scroll(game_map, 786, -624, 3, player.view_distance)
    elif player.in_vent == 2:
        smooth_scroll(game_map, -839, -299, 3, player.view_distance)
    elif player.in_vent == 3:
        smooth_scroll(game_map, -2139, -1174, 3, player.view_distance)
    elif player.in_vent == 4:
        smooth_scroll(game_map, -3039, 151, 3, player.view_distance)
    elif player.in_vent == 5:
        smooth_scroll(game_map, -4564, -1374, 3, player.view_distance)
    elif player.in_vent == 6:
        smooth_scroll(game_map, -5264, 126, 3, player.view_distance)
    elif player.in_vent == 7:
        smooth_scroll(game_map, -6239, 51, 3, player.view_distance)
    elif player.in_vent == 8:
        smooth_scroll(game_map, -6789, -1149, 3, player.view_distance)


def smooth_shadow_transition(player: Player, target: int, speed: int):
    if player.view_distance > target:
        player.view_distance -= speed
    elif player.view_distance < target:
        player.view_distance += speed


def draw_shadow_limiter(shadow_range: int):
    shadow_limiter_surface.fill((40, 40, 40))
    shadow_limiter_surface.blit(shadow_map_image, (game_map.x, game_map.y))
    pygame.draw.circle(shadow_limiter_surface, "#098765", (SCREEN_HALF_X, SCREEN_HALF_Y), shadow_range)
    display.blit(shadow_limiter_surface, (0, 0))


def draw_vent_arrows(player: Player):
    global left_vent_arrow
    global right_vent_arrow

    if player.in_vent == 1:
        left_vent_arrow = None

        right_vent_arrow = display.blit(
            pygame.transform.rotate(vent_arrow_image, 10.0),
            (1050 - player_1.half_width, 540 - player_1.half_height))
    elif player.in_vent == 2:
        left_vent_arrow = display.blit(
            pygame.transform.rotate(pygame.transform.flip(vent_arrow_image, True, False), 10.0),
            (870 - player_1.half_width, 570 - player_1.half_height))

        right_vent_arrow = display.blit(
            pygame.transform.rotate(vent_arrow_image, -30.0),
            (1030 - player_1.half_width, 605 - player_1.half_height))
    elif player.in_vent == 3:
        left_vent_arrow = display.blit(
            pygame.transform.rotate(pygame.transform.flip(vent_arrow_image, True, False), -30.0),
            (870 - player_1.half_width, 510 - player_1.half_height))

        right_vent_arrow = display.blit(
            pygame.transform.rotate(vent_arrow_image, 45.0),
            (1020 - player_1.half_width, 490 - player_1.half_height))
    elif player.in_vent == 4:
        left_vent_arrow = display.blit(
            pygame.transform.rotate(pygame.transform.flip(vent_arrow_image, True, False), 45.0),
            (870 - player_1.half_width, 605 - player_1.half_height))

        right_vent_arrow = None

    if player.in_vent == 5:
        left_vent_arrow = display.blit(
            pygame.transform.rotate(vent_arrow_image, 80.0),
            (970 - player_1.half_width, 450 - player_1.half_height))

        right_vent_arrow = display.blit(
            pygame.transform.rotate(vent_arrow_image, 10.0),
            (1050 - player_1.half_width, 540 - player_1.half_height))
    elif player.in_vent == 6:
        left_vent_arrow = display.blit(
            pygame.transform.rotate(pygame.transform.flip(vent_arrow_image, True, False), 80.0),
            (935 - player_1.half_width, 645 - player_1.half_height))

        right_vent_arrow = display.blit(
            pygame.transform.rotate(vent_arrow_image, -8.0),
            (1045 - player_1.half_width, 570 - player_1.half_height))
    elif player.in_vent == 7:
        left_vent_arrow = display.blit(
            pygame.transform.rotate(pygame.transform.flip(vent_arrow_image, True, False), -8.0),
            (870 - player_1.half_width, 545 - player_1.half_height))

        right_vent_arrow = display.blit(
            pygame.transform.rotate(vent_arrow_image, -70.0),
            (985 - player_1.half_width, 640 - player_1.half_height))
    elif player.in_vent == 8:
        left_vent_arrow = display.blit(
            pygame.transform.rotate(pygame.transform.flip(vent_arrow_image, True, False), -70.0),
            (920 - player_1.half_width, 450 - player_1.half_height))

        right_vent_arrow = display.blit(
            pygame.transform.rotate(pygame.transform.flip(vent_arrow_image, True, False), 10.0),
            (870 - player_1.half_width, 570 - player_1.half_height))


def draw_fps():
    fps_text = font.render(f"{clock.get_fps():2.0f} FPS", False, (180, 180, 180))
    display.blit(fps_text, (SCREEN_X - fps_text.get_width() - 1, 0))


def redraw_game_window(shadow_range: int):
    game_map.draw_map_image(display, shadow_surface, do_draw_collision)
    draw_shadow_limiter(shadow_range)
    if do_draw_collision:
        game_map.draw_collision(display)
        game_map.draw_coordinates(display, font)
    if player_1.in_vent:
        draw_vent_arrows(player_1)
    player_1.draw_player(display)
    if player_1.in_task != "None":
        result = False
        if player_1.in_task == "Clean Windows":
            result = clean_windows_task.task(dt)
        elif player_1.in_task == "Wipe down Tables":
            result = wipe_tables_task.task(dt)
        elif player_1.in_task == "Reset Wifi":
            result = reset_wifi_task.task(dt)
        elif player_1.in_task == "Plug-In Laptops":
            result = plug_in_laptops_task.task(dt)
        elif player_1.in_task == "Check Temperature":
            result = check_temperature_task.task()
        if result:
            player_1.in_task = "None"
    draw_fps()
    pygame.display.update()


# mainloop
game_map = Map(visible_map_image, shadow_map_image)
clock = pygame.time.Clock()
player_1 = Player(SCREEN_HALF_X, SCREEN_HALF_Y, (255, 0, 0), game_map, True, 0)
clean_windows_task = tasks.CleanWindows(SCREEN_HALF_X, SCREEN_HALF_Y, display)
wipe_tables_task = tasks.WipeDownTables(SCREEN_HALF_X, SCREEN_HALF_Y, display)
reset_wifi_task = tasks.ResetWifi(SCREEN_HALF_X, SCREEN_HALF_Y, display)
plug_in_laptops_task = tasks.PlugInLaptops(SCREEN_HALF_X, SCREEN_HALF_Y, display)
check_temperature_task = tasks.CheckTemperature(SCREEN_HALF_X, SCREEN_HALF_Y, display)
is_ghost = False
do_draw_collision = False
running_game = True
left_vent_arrow = None
right_vent_arrow = None
target_view_distance = player_1.view_distance
previous_time = time.monotonic()
while running_game:
    dt = time.monotonic() - previous_time
    previous_time = time.monotonic()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_w or event.key == pygame.K_s:
                pass
            elif event.key == pygame.K_v:
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

            elif event.key == pygame.K_t:
                if player_1.in_task == "None":
                    start_task()
                else:
                    player_1.in_task = "None"

            elif event.key == pygame.K_x:
                is_ghost = not is_ghost
            elif event.key == pygame.K_c:
                print(f"{game_map.x}, {game_map.y}")
            elif event.key == pygame.K_l:
                do_draw_collision = not do_draw_collision
            elif event.key == pygame.K_1:
                target_view_distance = 100
            elif event.key == pygame.K_2:
                target_view_distance = 400
            elif event.key == pygame.K_3:
                target_view_distance = 950

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if event.button == 1:
                if player_1.in_vent == 1:
                    if right_vent_arrow and right_vent_arrow.collidepoint(mouse_position):
                        player_1.in_vent = 2
                elif player_1.in_vent == 2:
                    if left_vent_arrow and left_vent_arrow.collidepoint(mouse_position):
                        player_1.in_vent = 1
                    elif right_vent_arrow and right_vent_arrow.collidepoint(mouse_position):
                        player_1.in_vent = 3
                elif player_1.in_vent == 3:
                    if left_vent_arrow and left_vent_arrow.collidepoint(mouse_position):
                        player_1.in_vent = 2
                    elif right_vent_arrow and right_vent_arrow.collidepoint(mouse_position):
                        player_1.in_vent = 4
                elif player_1.in_vent == 4:
                    if left_vent_arrow and left_vent_arrow.collidepoint(mouse_position):
                        player_1.in_vent = 3
                elif player_1.in_vent == 5:
                    if left_vent_arrow and left_vent_arrow.collidepoint(mouse_position):
                        player_1.in_vent = 6
                    elif right_vent_arrow and right_vent_arrow.collidepoint(mouse_position):
                        player_1.in_vent = 8
                elif player_1.in_vent == 6:
                    if left_vent_arrow and left_vent_arrow.collidepoint(mouse_position):
                        player_1.in_vent = 5
                    elif right_vent_arrow and right_vent_arrow.collidepoint(mouse_position):
                        player_1.in_vent = 7
                elif player_1.in_vent == 7:
                    if left_vent_arrow and left_vent_arrow.collidepoint(mouse_position):
                        player_1.in_vent = 6
                    elif right_vent_arrow and right_vent_arrow.collidepoint(mouse_position):
                        player_1.in_vent = 8
                elif player_1.in_vent == 8:
                    if left_vent_arrow and left_vent_arrow.collidepoint(mouse_position):
                        player_1.in_vent = 7
                    elif right_vent_arrow and right_vent_arrow.collidepoint(mouse_position):
                        player_1.in_vent = 5

    if player_1.in_vent != 0:
        transport_vents(player_1)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        if player_1.in_vent == 0 and player_1.in_task == "None":
            speed_modifier = 1
            if keys[pygame.K_a] or keys[pygame.K_d]:
                speed_modifier = 0.7
            for pixel in range(int(game_map.y_velocity * speed_modifier * dt)):
                if check_for_collisions(player_1.w_hitbox, game_map.get_wall_rects) and not is_ghost:
                    break
                game_map.y += 1
    if keys[pygame.K_a]:
        if player_1.in_vent == 0 and player_1.in_task == "None":
            speed_modifier = 1
            if keys[pygame.K_w] or keys[pygame.K_s]:
                speed_modifier = 0.7
            for pixel in range(int(game_map.x_velocity * speed_modifier * dt)):
                if check_for_collisions(player_1.a_hitbox, game_map.get_wall_rects) and not is_ghost:
                    break
                game_map.x += 1
    if keys[pygame.K_s]:
        if player_1.in_vent == 0 and player_1.in_task == "None":
            speed_modifier = 1
            if keys[pygame.K_a] or keys[pygame.K_d]:
                speed_modifier = 0.7
            for pixel in range(int(game_map.y_velocity * speed_modifier * dt)):
                if check_for_collisions(player_1.s_hitbox, game_map.get_wall_rects) and not is_ghost:
                    break
                game_map.y -= 1
    if keys[pygame.K_d]:
        if player_1.in_vent == 0 and player_1.in_task == "None":
            speed_modifier = 1
            if keys[pygame.K_w] or keys[pygame.K_s]:
                speed_modifier = 0.7
            for pixel in range(int(game_map.x_velocity * speed_modifier * dt)):
                if check_for_collisions(player_1.d_hitbox, game_map.get_wall_rects) and not is_ghost:
                    break
                game_map.x -= 1

    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    if player_1.view_distance != target_view_distance:
        smooth_shadow_transition(player_1, target_view_distance, 10)

    redraw_game_window(player_1.view_distance)

    clock.tick(50)
pygame.quit()
sys.exit()
