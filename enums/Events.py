from enum import Enum


class Events(Enum):
    LIGHTS_OFF = 1
    LIGHTS_ON = 2
    AC_LEFT = 3
    AC_RIGHT = 4
    AC_ONLINE = 5
    SPOILED_FOOD = 5
    FOOD_REMOVED = 7
    MEETING_OFFLINE = 8
    MEETING_ONLINE = 9
    IMPOSTER_WIN = 10
    CREWMATE_WIN = 11
