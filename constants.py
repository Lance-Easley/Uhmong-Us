from enums.Sabotages import Sabotage
from enums.Tasks import Tasks

# Variables ###
SCREEN_X = 1920
SCREEN_Y = 1080
SCREEN_HALF_X = SCREEN_X // 2
SCREEN_HALF_Y = SCREEN_Y // 2
TASK_LIST = (
    {"task": Tasks.CHECK_INBOX, "indexes": [0]},
    {"task": Tasks.REFILL_HAND_SANITIZER, "indexes": [1, 2]},
    {"task": Tasks.CHECK_TEMPERATURE, "indexes": [3]},
    {"task": Tasks.RESET_WIFI, "indexes": [4]},
    {"task": Tasks.PLUG_IN_LAPTOPS,  "indexes": [5, 6]},
    {"task": Tasks.WIPE_DOWN_TABLES, "indexes": [7, 8, 9, 10]},
    {"task": Tasks.CLEAN_WINDOWS, "indexes": [11, 12, 13, 14, 15, 16, 17, 18]},
    {"task": Tasks.NOMINATE_FOR_AWARDS, "indexes": [19]},
    {"task": Tasks.COLLECT_TRASH, "indexes": [20, 21, 22, 23, 24, 25, 26, 27]},
    {"task": Tasks.DO_FLASHCARDS, "indexes": [28]}
)
MINIMAP_X = 447
MINIMAP_Y = 402
DOOR_CLOSED_TIME = 20
SABOTAGE_COOLDOWN_TIMES = {
    Sabotage.LIGHTS: 40,
    Sabotage.LEFT_AC: 40,
    Sabotage.RIGHT_AC: 40,
    Sabotage.ZOOM_MEETING: 40,
    Sabotage.SPOILED_FOOD: 40
}
DOOMSDAY_CLOCK_TIME = 60
MAX_VIEW_DISTANCE = 400
MIN_VIEW_DISTANCE = 100
###