from enums.Sabotages import Sabotage

# Variables ###
SCREEN_X = 1920
SCREEN_Y = 1080
SCREEN_HALF_X = SCREEN_X // 2
SCREEN_HALF_Y = SCREEN_Y // 2
TASK_LIST = (
    {"name": "Check Inbox", "indexes": [0]},
    {"name": "Refill Hand-Sanitizer", "indexes": [1, 2]},
    {"name": "Check Temperature", "indexes": [3]},
    {"name": "Reset Wifi", "indexes": [4]},
    {"name": "Plug-In Laptops", "indexes": [5, 6]},
    {"name": "Wipe down Tables", "indexes": [7, 8, 9, 10]},
    {"name": "Clean Windows", "indexes": [11, 12, 13, 14, 15, 16, 17, 18]},
    {"name": "Nominate For Awards", "indexes": [19]},
    {"name": "Collect Trash", "indexes": [20, 21, 22, 23, 24, 25, 26, 27]},
    {"name": "Do Flashcards", "indexes": [28]}
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
