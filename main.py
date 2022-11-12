import math
import random

import pygame
import sys
import time

from constants import *
from entities.map import Map
from entities.player import Player
from entities import tasks

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
task_bar_image = pygame.image.load('images/hud/task_bar.png').convert()
task_bar_image.set_colorkey((255, 255, 255))

use_button_image = pygame.image.load('images/hud/use_button.png').convert()
use_button_image.set_colorkey((255, 255, 255))
use_button_disabled_image = pygame.image.load('images/hud/use_button_disabled.png').convert()
use_button_disabled_image.set_colorkey((255, 255, 255))
report_button_image = pygame.image.load('images/hud/report_button.png').convert()
report_button_image.set_colorkey((255, 255, 255))
report_button_disabled_image = pygame.image.load('images/hud/report_button_disabled.png').convert()
report_button_disabled_image.set_colorkey((255, 255, 255))

minimap_image = pygame.image.load('images/hud/minimap.png').convert()
minimap_image.set_colorkey((255, 255, 255))
minimap_image.set_alpha(220)
sabotage_minimap_image = pygame.image.load('images/hud/sabotage_minimap.png').convert()
sabotage_minimap_image.set_colorkey((255, 255, 255))
sabotage_minimap_image.set_alpha(220)
minimap_player_locator_image = pygame.image.load('images/hud/minimap_player_locator.png').convert()
minimap_player_locator_image.set_colorkey((255, 255, 255))
minimap_task_locator_image = pygame.image.load('images/hud/minimap_task_locator.png').convert()
minimap_task_locator_image.set_colorkey((255, 255, 255))
door_open_image = pygame.image.load('images/hud/door_open_icon.png').convert()
door_open_image.set_colorkey((255, 255, 255))
door_closed_full_image = pygame.image.load('images/hud/door_closed_full_icon.png').convert()
door_closed_full_image.set_colorkey((255, 255, 255))
door_closed_half_image = pygame.image.load('images/hud/door_closed_half_icon.png').convert()
door_closed_half_image.set_colorkey((255, 255, 255))
door_closed_danger_image = pygame.image.load('images/hud/door_closed_danger_icon.png').convert()
door_closed_danger_image.set_colorkey((255, 255, 255))
door_disabled_image = pygame.image.load('images/hud/door_disabled_icon.png').convert()
door_disabled_image.set_colorkey((255, 255, 255))
map_icon_image = pygame.image.load('images/hud/map_icon.png').convert()
map_icon_image.set_colorkey((255, 255, 255))
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
    return any((wall for wall in wall_rects if rect.colliderect(wall)))


def start_task():
    for task_info in (game_map.get_task_rects[task["index"]] for task in player_1.tasks):
        if player_1.general_hitbox.colliderect(task_info["rect"]):
            player_1.in_task = task_info["name"]
            if task_info["name"] == "Clean Windows":
                clean_windows_task.renew_task_surface()
            elif task_info["name"] == "Wipe down Tables":
                wipe_tables_task.renew_task_surface()
            elif task_info["name"] == "Reset Wifi":
                reset_wifi_task.renew_task_surface()
            elif task_info["name"] == "Plug-In Laptops":
                plug_in_laptops_task.renew_task_surface()
            elif task_info["name"] == "Check Temperature":
                check_temperature_task.renew_task_surface()
            elif task_info["name"] == "Nominate For Awards":
                nominate_task.renew_task_surface()
            elif task_info["name"] == "Collect Trash":
                collect_trash.renew_task_surface()
            elif task_info["name"] == "Refill Hand-Sanitizer":
                refill_hand_sanitizer.renew_task_surface()
            elif task_info["name"] == "Check Inbox":
                check_inbox.renew_task_surface()
            elif task_info["name"] == "Do Flashcards":
                do_flashcards.renew_task_surface()
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


def get_minimap_coords(map_x: int, map_y: int) -> tuple[int, int]:
    x = abs((map_x - SCREEN_HALF_X) // 8) + MINIMAP_X
    y = abs((map_y - SCREEN_HALF_Y) // 8) + MINIMAP_Y
    return x, y


def center_image_in_rect(image: pygame.Surface, rect: pygame.Rect):
    image_rect = image.get_rect()
    display.blit(image, ((rect.x + rect.width // 2) - image_rect.width // 2,
                         (rect.y + rect.height // 2) - image_rect.height // 2))


def draw_doors_ui(all_doors: dict):
    for door in all_doors.keys():
        room_info = all_doors[door]
        if game_map.door_data[door]["closed"]:
            if game_map.door_data[door]["timer"] > DOOR_CLOSED_TIME * 0.66 + DOOR_CLOSED_TIME:
                center_image_in_rect(door_closed_full_image, room_info["minimap_button_rect"])
            elif game_map.door_data[door]["timer"] > DOOR_CLOSED_TIME * 0.33 + DOOR_CLOSED_TIME:
                center_image_in_rect(door_closed_half_image, room_info["minimap_button_rect"])
            else:
                center_image_in_rect(door_closed_danger_image, room_info["minimap_button_rect"])
        else:
            if game_map.door_data[door]["timer"] == 0:
                center_image_in_rect(door_open_image, room_info["minimap_button_rect"])
            else:
                center_image_in_rect(door_disabled_image, room_info["minimap_button_rect"])


def draw_ui(progress: float):
    pygame.draw.rect(display, (0, 255, 0), (9, 9, math.ceil(392 * progress), 32))
    display.blit(task_bar_image, (5, 5))

    display.blit(map_icon_image, (1770, 50))

    task_list_surface = pygame.Surface((268, len(player_1.tasks) * 30 + 5), pygame.SRCALPHA)
    task_list_surface.fill((140, 140, 140, 180))
    use_button_enabled = False
    for i, task_info in enumerate(player_1.tasks):
        task_list_surface.blit(
            font.render(task_info["name"], False,
                        (0, 255, 0) if task_info["done"] else (255, 255, 255)), (5, i * 30 + 5))

        if player_1.in_task == "None":
            if player_1.general_hitbox.colliderect(game_map.get_task_rects[task_info["index"]]["rect"]):
                if not task_info["done"]:
                    use_button_enabled = True

    display.blit(task_list_surface, (5, 50))

    if use_button_enabled:
        display.blit(use_button_image, (1670, 830))
    else:
        display.blit(use_button_disabled_image, (1670, 830))

    # TODO: Add if (sees dead body) once dead bodies and multiplayer added to game
    display.blit(report_button_disabled_image, (1420, 830))

    if show_minimap:
        if player_1.is_traitor:
            display.blit(sabotage_minimap_image, (MINIMAP_X, MINIMAP_Y))

            draw_doors_ui(game_map.get_door_rect_info)
        else:
            display.blit(minimap_image, (MINIMAP_X, MINIMAP_Y))

            for task_info in player_1.tasks:
                if not task_info["done"]:
                    task_rect = game_map.get_task_rects[task_info["index"]]["rect"]
                    task_x, task_y = get_minimap_coords(
                        task_rect.x - game_map.x + SCREEN_HALF_X, task_rect.y - game_map.y + SCREEN_HALF_Y)
                    center_image_in_rect(minimap_task_locator_image,
                                         pygame.Rect(task_x, task_y, task_rect.w / 8, task_rect.h / 8))

        player_x, player_y = get_minimap_coords(game_map.x + player_1.half_width, game_map.y + player_1.half_height)
        center_image_in_rect(minimap_player_locator_image,
                             pygame.Rect(player_x, player_y, player_1.width / 8, player_1.height / 8))


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
            result = check_temperature_task.task(dt)
        elif player_1.in_task == "Nominate For Awards":
            result = nominate_task.task(dt)
        elif player_1.in_task == "Collect Trash":
            result = collect_trash.task(dt)
        elif player_1.in_task == "Refill Hand-Sanitizer":
            result = refill_hand_sanitizer.task(dt)
        elif player_1.in_task == "Check Inbox":
            result = check_inbox.task(dt)
        elif player_1.in_task == "Do Flashcards":
            result = do_flashcards.task(dt)
        if result:
            completed_task = next(t for t in player_1.tasks if t["name"] == player_1.in_task)
            completed_task["done"] = True
            game_map.tasks_to_render.remove(completed_task["index"])
            player_1.in_task = "None"

    draw_fps()
    draw_ui((100 / 4) * (4 - len(game_map.tasks_to_render)) / 100)
    pygame.display.update()


# mainloop
random_tasks = tuple(
    {"name": t["name"], "index": (random.choice(t["indexes"])), "done": False} for t in random.sample(TASK_LIST, 8))
player_1 = Player((255, 0, 0), True, 0, random_tasks)
game_map = Map(visible_map_image, shadow_map_image, {t["index"] for t in player_1.tasks})
clock = pygame.time.Clock()

clean_windows_task = tasks.CleanWindows(display)
wipe_tables_task = tasks.WipeDownTables(display)
reset_wifi_task = tasks.ResetWifi(display)
plug_in_laptops_task = tasks.PlugInLaptops(display)
check_temperature_task = tasks.CheckTemperature(display)
nominate_task = tasks.NominateForAwards(display)
collect_trash = tasks.CollectTrash(display)
refill_hand_sanitizer = tasks.RefillHandSanitizer(display)
check_inbox = tasks.CheckInbox(display)
do_flashcards = tasks.DoFlashcards(display)

show_minimap = False
minimap_button_rect = pygame.Rect(1770, 50, 100, 100)
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

            # Use Button
            elif event.key == pygame.K_e:
                if player_1.in_task == "None":
                    show_minimap = False
                    start_task()
                else:
                    player_1.in_task = "None"

            elif event.key == pygame.K_TAB:
                show_minimap = not show_minimap
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

                if minimap_button_rect.collidepoint(mouse_position):
                    show_minimap = not show_minimap

                if player_1.is_traitor and show_minimap:
                    for room in game_map.get_door_rect_info.keys():
                        if game_map.get_door_rect_info[room]["minimap_button_rect"].collidepoint(mouse_position):
                            game_map.close_door(room)

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
        running_game = False

    if player_1.view_distance != target_view_distance:
        smooth_shadow_transition(player_1, target_view_distance, 10)

    game_map.process_door_timers(dt)

    redraw_game_window(player_1.view_distance)

    clock.tick()

pygame.quit()
sys.exit()
