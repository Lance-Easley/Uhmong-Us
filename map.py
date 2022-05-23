import math
import pygame


class Map(object):
    def __init__(self, visible_map_image, shadow_map_image):
        self.x, self.y = -2665, -1207
        self.visible_map_image = visible_map_image
        self.shadow_map_image = shadow_map_image
        self.width = self.visible_map_image.get_rect().width
        self.height = self.visible_map_image.get_rect().height
        self.x_velocity = 375
        self.y_velocity = 375

        self.wall_segments = {
            # Outside: classrooms top wall
            ((4995, 300), (5300, 350)),
            ((5295, 350), (5300, 300)),
            # Outside: offices left wall
            ((4950, 395), (5000, 400)),
            ((4950, 400), (5000, 100)),
            # Outside: offices right wall
            ((6350, 100), (6400, 800)),

            # BCCA: top office middle wall
            ((5400, 300), (5900, 350)),
            ((5400, 350), (5900, 300)),
            # BCCA: top office right wall
            ((6000, 300), (6005, 350)),
            ((6000, 350), (6350, 300)),
            # BCCA: left office left wall
            ((4950, 500), (5000, 505)),
            ((4950, 800), (5000, 500)),
            # BCCA: left office bottom wall
            ((4900, 800), (5600, 850)),
            ((4900, 850), (5600, 800)),
            # BCCA: left office top wall
            ((5000, 550), (5600, 600)),
            ((5595, 600), (5600, 550)),
            # BCCA: right office top wall
            ((5700, 550), (5705, 600)),
            ((5700, 600), (6350, 550)),

            # BCCA: breakroom right wall
            ((4675, 800), (4675, 350)),
            # BCCA: breakroom bottom right wall
            ((4300, 800), (4750, 850)),
            ((4300, 850), (4750, 800)),
            # BCCA: breakroom bottom left wall
            ((4195, 800), (4200, 850)),
            ((4150, 805), (4200, 800)),
            # BCCA: breakroom left wall
            ((4100, 350), (4150, 1100)),

            # BCCA: lobby top left block
            ((4350, 1100), (4550, 1300)),
            ((4350, 1300), (4550, 1100)),
            # BCCA: lobby bottom left block
            ((4350, 1750), (4550, 1950)),
            ((4350, 1950), (4550, 1750)),
            # BCCA: lobby top right block
            ((6550, 1100), (6750, 1300)),
            ((6550, 1300), (6750, 1100)),
            # BCCA: lobby bottom right block
            ((6550, 1800), (6750, 2000)),
            ((6550, 2000), (6750, 1800)),
            # BCCA: lobby top right wall
            ((5650, 1200), (5655, 1250)),
            ((5650, 1250), (6350, 1200)),
            # BCCA: lobby top left wall
            ((4750, 1200), (5450, 1250)),
            ((5445, 1250), (5450, 1200)),
            # BCCA: lobby left top wall
            ((4750, 1200), (4800, 1400)),
            ((4750, 1400), (4800, 1395)),
            # BCCA: lobby left bottom wall
            ((4750, 1600), (4800, 1605)),
            ((4750, 1800), (4800, 1600)),
            # BCCA: lobby bottom left wall
            ((5445, 1750), (5450, 1800)),
            ((4750, 1800), (5450, 1750)),
            # BCCA: lobby bottom right wall
            ((5650, 1750), (6350, 1800)),
            ((5650, 1800), (5655, 1750)),
            # BCCA: lobby right top wall
            ((6300, 1395), (6350, 1400)),
            ((6300, 1400), (6350, 1200)),
            # BCCA: lobby right bottom wall
            ((6300, 1600), (6350, 1800)),
            ((6300, 1605), (6350, 1600)),

            # BCCA: supply bottom right wall
            ((3800, 1050), (4150, 1100)),
            ((3800, 1100), (3805, 1050)),
            # BCCA: supply middle wall
            ((3600, 600), (3650, 1050)),
            ((3600, 605), (3650, 600)),

            # BCCA: hallway top door stud
            ((3150, 1145), (3200, 1150)),
            ((3150, 1150), (3200, 1100)),
            # BCCA: hallway bottom door stud
            ((3150, 1300), (3200, 1350)),
            ((3150, 1305), (3200, 1300)),

            # BCCA: classroom1 right wall
            ((3325, 350), (3325, 1050)),
            # BCCA: classroom1 bottom right wall
            ((2250, 1050), (3700, 1100)),
            ((2250, 1100), (3700, 1050)),
            # BCCA: classroom1 block
            ((2500, 500), (2900, 900)),
            ((2500, 900), (2900, 500)),
            # BCCA: classroom1 bottom left wall
            ((1900, 1050), (2150, 1100)),
            ((1900, 1100), (2150, 1050)),
            # BCCA: classroom1 left top wall
            ((2050, 445), (2100, 450)),
            ((2050, 450), (2100, 350)),
            # BCCA: classroom1 left bottom wall
            ((2050, 550), (2100, 1050)),
            ((2050, 555), (2100, 550)),

            # BCCA: breakoutroom1 bottom left wall
            ((1500, 1050), (1750, 1100)),
            ((1500, 1100), (1750, 1050)),
            # BCCA: breakoutroom1 table
            ((1750, 745), (1900, 750)),
            ((1750, 750), (1900, 350)),
            # BCCA: breakoutroom1 left top wall
            ((1550, 350), (1600, 450)),
            ((1550, 450), (1600, 445)),
            # BCCA: breakoutroom1 left bottom wall
            ((1550, 550), (1600, 555)),
            ((1550, 1050), (1600, 550)),

            # BCCA: classroom3 right block
            ((1100, 600), (1300, 800)),
            ((1100, 800), (1300, 600)),
            # BCCA: classroom3 left block
            ((600, 600), (800, 800)),
            ((600, 800), (800, 600)),
            # BCCA: classroom3 middle wall
            ((350, 850), (300, 1100)),
            # BCCA: classroom3 bottom left wall
            ((1395, 1050), (1400, 1100)),
            ((300, 1100), (1400, 1050)),
            # BCCA: classroom3 middle right wall
            ((250, 850), (255, 900)),
            ((250, 900), (350, 850)),
            # BCCA: classroom3 middle left wall
            ((95, 895), (150, 900)),
            ((145, 900), (150, 850)),

            # BCCA: classroom4 top left wall
            ((300, 1350), (1400, 1400)),
            ((1395, 1400), (1400, 1350)),
            # BCCA: classroom4 middle wall
            ((350, 1600), (300, 1350)),
            # BCCA: classroom4 middle right wall
            ((250, 1550), (350, 1600)),
            ((250, 1600), (255, 1550)),
            # BCCA: classroom4 middle left wall
            ((145, 1550), (150, 1600)),
            ((95, 1555), (150, 1550)),
            # BCCA: classroom4 center top wall
            ((550, 1600), (750, 1650)),
            ((600, 1650), (750, 1600)),
            # BCCA: classroom4 center left wall
            ((550, 1950), (600, 1650)),
            # BCCA: classroom4 center bottom wall 
            ((550, 1950), (1050, 1900)),
            # BCCA: classroom4 center right wall
            ((1050, 1800), (1100, 1950)),
            ((1050, 1900), (1100, 1800)),

            # BCCA: breakoutroom2 top left wall
            ((1500, 1350), (1750, 1400)),
            ((1500, 1400), (1750, 1350)),
            # BCCA: breakoutroom2 top right wall
            ((1900, 1350), (2150, 1400)),
            ((1900, 1400), (2150, 1350)),
            # BCCA: breakoutroom2 left top wall
            ((1550, 1400), (1600, 1900)),
            ((1550, 1900), (1600, 1895)),
            # BCCA: breakoutroom2 left bottom wall
            ((1550, 2000), (1600, 2005)),
            ((1550, 2100), (1600, 2000)),
            # BCCA: breakoutroom2 table
            ((1750, 1500), (1900, 1950)),
            ((1750, 1950), (1900, 1500)),
            # BCCA: breakoutroom2 right top wall
            ((2050, 1895), (2100, 1900)),
            ((2050, 1900), (2100, 1400)),
            # BCCA: breakoutroom2 right bottom wall
            ((2050, 2000), (2100, 2100)),
            ((2050, 2005), (2100, 2000)),

            # BCCA: classroom2 top right wall
            ((2250, 1350), (2255, 1400)),
            ((2250, 1400), (3600, 1350)),
            # BCCA: classroom2 block
            ((2500, 1550), (2900, 1950)),
            ((2500, 1950), (2900, 1550)),
            # BCCA: classroom2 right wall
            ((3325, 1400), (3325, 2100)),

            # BCCA: bathroom top left door stud 
            ((3550, 1445), (3600, 1450)),
            ((3550, 1450), (3600, 1350)),
            # BCCA: bathroom bottom left door stud
            ((3550, 1550), (3600, 1600)),
            ((3550, 1650), (3600, 1550)),
            # BCCA: bathroom top right door stud
            ((3850, 1350), (3900, 1450)),
            ((3850, 1450), (3900, 1400)),
            # BCCA: bathroom bottom right door stud
            ((3850, 1550), (3900, 1650)),
            ((3850, 1555), (3900, 1550)),
            # BCCA: bathroom top middle wall
            ((3600, 1600), (3900, 1650)),
            # BCCA: bathroom middle wall
            ((3725, 1650), (3725, 2100)),
            # BCCA: bathroom top right wall
            ((3900, 1400), (4150, 1350)),
            # BCCA: bathroom right wall
            ((4100, 2100), (4150, 1350)),

            # BCCA: kitchen right wall
            ((7125, 450), (7125, 800)),
            # BCCA: kitchen bottom left wall
            ((5700, 800), (6900, 850)),
            ((5700, 850), (6900, 800)),
            # BCCA: kitchen bottom right wall
            ((7000, 800), (7250, 850)),
            ((7000, 850), (7250, 800)),

            # BCCA: meeting room bottom wall
            ((7350, 800), (8100, 850)),
            ((7350, 850), (7355, 800)),
            # BCCA: meeting room middle wall
            ((7450, 650), (7500, 655)),
            ((7450, 800), (7500, 650)),

            # BCCA: incubator top left wall
            ((6999, 1149), (7650, 1100)),
            # BCCA: incubator top right wall 
            ((7850, 1100), (7900, 1800)),
            # BCCA: incubator left top wall
            ((6950, 1100), (7000, 1550)),
            ((6950, 1550), (6999, 1149)),
            # BCCA: incubator left bottom wall
            ((6950, 1650), (7000, 1655)),
            ((6950, 2100), (7000, 1650)),
            # BCCA: incubator top entrance left wall
            ((7645, 1245), (7700, 1250)),
            ((7695, 1250), (7700, 1200)),
            # BCCA: incubator top entrance right wall
            ((7800, 1200), (7805, 1250)),
            ((7800, 1250), (7855, 1245)),
            # BCCA: incubator top room bottom left wall
            ((7095, 1450), (7100, 1500)),
            ((7000, 1500), (7100, 1450)),
            # BCCA: incubator top room bottom right wall
            ((7200, 1450), (7300, 1500)),
            ((7200, 1500), (7300, 1400)),
            # BCCA: incubator top room middle top wall
            ((7250, 1350), (7450, 1400)),
            ((7300, 1400), (7450, 1350)),
            # BCCA: incubator top room bottom right wall
            ((7550, 1350), (7650, 1400)),
            ((7550, 1400), (7600, 1350)),
            # BCCA: incubator top room right wall
            ((7600, 1350), (7650, 1100)),
            # BCCA: incubator bottom room top left wall
            ((7000, 1700), (7100, 1750)),
            ((7095, 1750), (7100, 1700)),
            # BCCA: incubator bottom room top right wall
            ((7200, 1700), (7300, 1800)),
            ((7200, 1750), (7300, 1700)),
            # BCCA: incubator bottom room top right wall
            ((7300, 1800), (7855, 1850)),
            ((7250, 1850), (7300, 1800)),
        }

        self.v_x = 0
        self.v_y = 0
        self.v_w = 1920
        self.v_h = 1080

        self.v_t = self.v_y
        self.v_b = self.v_y + self.v_h
        self.v_l = self.v_x
        self.v_r = self.v_x + self.v_w

        self.viewport = pygame.Rect(self.v_x, self.v_y, self.v_w, self.v_h)

        self.viewport_segments = [
            # Viewport: top
            {'a': {'x': self.v_x, 'y': self.v_y}, 'b': {'x': self.v_x + self.v_w - 1, 'y': self.v_y}},
            # Viewport: right
            {'a': {'x': self.v_x + self.v_w - 1, 'y': self.v_y},
             'b': {'x': self.v_x + self.v_w - 1, 'y': self.v_y + self.v_h - 1}},
            # Viewport: bottom
            {'a': {'x': self.v_x, 'y': self.v_y + self.v_h - 1},
             'b': {'x': self.v_x + self.v_w - 1, 'y': self.v_y + self.v_h - 1}},
            # Viewport: left
            {'a': {'x': self.v_x, 'y': self.v_y + self.v_h - 1}, 'b': {'x': self.v_x, 'y': self.v_y}},
        ]

    @property
    def get_wall_rects(self):
        return [
            pygame.Rect(self.x + 50, self.y + 300, 5250, 50),  # Outside: classrooms top wall [4:6]
            pygame.Rect(self.x + 50, self.y + 350, 50, 1750),  # Outside: classrooms left wall
            pygame.Rect(self.x + 50, self.y + 2100, 8100, 50),  # Outside: classrooms bottom wall
            pygame.Rect(self.x + 4950, self.y + 50, 1450, 50),  # Outside: offices top wall
            pygame.Rect(self.x + 4950, self.y + 100, 50, 300),  # Outside: offices left wall [6:8]
            pygame.Rect(self.x + 6350, self.y + 100, 50, 700),  # Outside: offices right wall [8]
            pygame.Rect(self.x + 6400, self.y + 400, 1750, 50),  # Outside: kitchen top wall
            pygame.Rect(self.x + 8100, self.y + 450, 50, 1650),  # Outside: student door wall

            pygame.Rect(self.x + 5400, self.y + 300, 500, 50),  # BCCA: top office middle wall [9:11]
            pygame.Rect(self.x + 6000, self.y + 300, 350, 50),  # BCCA: top office right wall [11:13]
            pygame.Rect(self.x + 4950, self.y + 500, 50, 300),  # BCCA: left office left wall [13:15]
            pygame.Rect(self.x + 4900, self.y + 800, 700, 50),  # BCCA: left office bottom wall [15:17]
            pygame.Rect(self.x + 5000, self.y + 550, 600, 50),  # BCCA: left office top wall [17:19]
            pygame.Rect(self.x + 5500, self.y + 600, 50, 200),  # BCCA: left office right wall
            pygame.Rect(self.x + 5700, self.y + 550, 650, 50),  # BCCA: right office top wall [19:21]
            pygame.Rect(self.x + 5750, self.y + 600, 50, 200),  # BCCA: right office right wall

            pygame.Rect(self.x + 4650, self.y + 350, 50, 450),  # BCCA: breakroom right wall [21]
            pygame.Rect(self.x + 4300, self.y + 800, 450, 50),  # BCCA: breakroom bottom right wall [21:23]
            pygame.Rect(self.x + 4150, self.y + 800, 50, 50),  # BCCA: breakroom bottom left wall [23:25]
            pygame.Rect(self.x + 4100, self.y + 350, 50, 750),  # BCCA: breakroom left wall [25:27]

            pygame.Rect(self.x + 4350, self.y + 1100, 200, 200),  # BCCA: lobby top left block [27:29]
            pygame.Rect(self.x + 4350, self.y + 1750, 200, 200),  # BCCA: lobby bottom left block [29:31]
            pygame.Rect(self.x + 6550, self.y + 1100, 200, 200),  # BCCA: lobby top right block [31:33]
            pygame.Rect(self.x + 6550, self.y + 1800, 200, 200),  # BCCA: lobby bottom right block [33:35]
            pygame.Rect(self.x + 5650, self.y + 1200, 700, 50),  # BCCA: lobby top right wall [35:37]
            pygame.Rect(self.x + 4750, self.y + 1200, 700, 50),  # BCCA: lobby top left wall [37:39]
            pygame.Rect(self.x + 4750, self.y + 1250, 50, 150),  # BCCA: lobby left top wall [39:41]
            pygame.Rect(self.x + 4750, self.y + 1600, 50, 150),  # BCCA: lobby left bottom wall [41:43]
            pygame.Rect(self.x + 4750, self.y + 1750, 700, 50),  # BCCA: lobby bottom left wall [43:45]
            pygame.Rect(self.x + 5650, self.y + 1750, 700, 50),  # BCCA: lobby bottom right wall [45:47]
            pygame.Rect(self.x + 6300, self.y + 1250, 50, 150),  # BCCA: lobby right top wall [47:49]
            pygame.Rect(self.x + 6300, self.y + 1600, 50, 150),  # BCCA: lobby right bottom wall [49:51]

            pygame.Rect(self.x + 3800, self.y + 1050, 300, 50),  # BCCA: supply bottom right wall [51:53]
            pygame.Rect(self.x + 3600, self.y + 600, 50, 450),  # BCCA: supply middle wall [53:55]
            pygame.Rect(self.x + 3350, self.y + 750, 250, 50),  # BCCA: supply middle left wall

            pygame.Rect(self.x + 3150, self.y + 1100, 50, 50),  # BCCA: hallway top door stud [55:57]
            pygame.Rect(self.x + 3150, self.y + 1300, 50, 50),  # BCCA: hallway bottom door stud [57:59]

            pygame.Rect(self.x + 3300, self.y + 350, 50, 700),  # BCCA: classroom1 right wall [59]
            pygame.Rect(self.x + 2250, self.y + 1050, 1450, 50),  # BCCA: classroom1 bottom right wall [60:62]
            pygame.Rect(self.x + 2500, self.y + 500, 400, 400),  # BCCA: classroom1 block [62:64]
            pygame.Rect(self.x + 1900, self.y + 1050, 250, 50),  # BCCA: classroom1 bottom left wall [64:66]
            pygame.Rect(self.x + 2050, self.y + 350, 50, 100),  # BCCA: classroom1 left top wall [66:68]
            pygame.Rect(self.x + 2050, self.y + 550, 50, 500),  # BCCA: classroom1 left bottom wall [68:70]

            pygame.Rect(self.x + 1500, self.y + 1050, 250, 50),  # BCCA: breakoutroom1 bottom left wall [70:72]
            pygame.Rect(self.x + 1750, self.y + 350, 150, 400),  # BCCA: breakoutroom1 table [72:74]
            pygame.Rect(self.x + 1550, self.y + 350, 50, 100),  # BCCA: breakoutroom1 left top wall [74:76]
            pygame.Rect(self.x + 1550, self.y + 550, 50, 500),  # BCCA: breakoutroom1 left bottom wall [76:78]

            pygame.Rect(self.x + 1100, self.y + 600, 200, 200),  # BCCA: classroom3 right block [78:80]
            pygame.Rect(self.x + 600, self.y + 600, 200, 200),  # BCCA: classroom3 left block [80:82]
            pygame.Rect(self.x + 300, self.y + 900, 50, 150),  # BCCA: classroom3 middle wall [82]
            pygame.Rect(self.x + 300, self.y + 1050, 1100, 50),  # BCCA: classroom3 bottom left wall [83:85]
            pygame.Rect(self.x + 250, self.y + 850, 100, 50),  # BCCA: classroom3 middle right wall [85:87]
            pygame.Rect(self.x + 100, self.y + 850, 50, 50),  # BCCA: classroom3 middle left wall [87:89]

            pygame.Rect(self.x + 300, self.y + 1350, 1100, 50),  # BCCA: classroom4 top left wall [89:91]
            pygame.Rect(self.x + 300, self.y + 1400, 50, 150),  # BCCA: classroom4 middle wall [91]
            pygame.Rect(self.x + 250, self.y + 1550, 100, 50),  # BCCA: classroom4 middle right wall [92:94]
            pygame.Rect(self.x + 100, self.y + 1550, 50, 50),  # BCCA: classroom4 middle left wall [94:96]
            pygame.Rect(self.x + 550, self.y + 1600, 200, 50),  # BCCA: classroom4 center top wall [96:98]
            pygame.Rect(self.x + 550, self.y + 1650, 50, 250),  # BCCA: classroom4 center left wall [98]
            pygame.Rect(self.x + 550, self.y + 1900, 500, 50),  # BCCA: classroom4 center bottom wall [99]
            pygame.Rect(self.x + 1050, self.y + 1800, 50, 150),  # BCCA: classroom4 center right wall [100:102]

            pygame.Rect(self.x + 1500, self.y + 1350, 250, 50),  # BCCA: breakoutroom2 top left wall [102:104]
            pygame.Rect(self.x + 1900, self.y + 1350, 250, 50),  # BCCA: breakoutroom2 top right wall [104:106]
            pygame.Rect(self.x + 1550, self.y + 1400, 50, 500),  # BCCA: breakoutroom2 left top wall [106:108]
            pygame.Rect(self.x + 1550, self.y + 2000, 50, 100),  # BCCA: breakoutroom2 left bottom wall [108:110]
            pygame.Rect(self.x + 1750, self.y + 1500, 150, 450),  # BCCA: breakoutroom2 table [110:112]
            pygame.Rect(self.x + 2050, self.y + 1400, 50, 500),  # BCCA: breakoutroom2 right top wall [112:114]
            pygame.Rect(self.x + 2050, self.y + 2000, 50, 100),  # BCCA: breakoutroom2 right bottom wall [114:116]

            pygame.Rect(self.x + 2250, self.y + 1350, 1350, 50),  # BCCA: classroom2 top right wall [116:118]
            pygame.Rect(self.x + 2500, self.y + 1550, 400, 400),  # BCCA: classroom2 block [118:120]
            pygame.Rect(self.x + 3300, self.y + 1400, 50, 700),  # BCCA: classroom2 right wall [120]

            pygame.Rect(self.x + 3550, self.y + 1400, 50, 50),  # BCCA: bathroom top left door stud [121:123]
            pygame.Rect(self.x + 3550, self.y + 1550, 50, 50),  # BCCA: bathroom bottom left door stud [123:125]
            pygame.Rect(self.x + 3850, self.y + 1400, 50, 50),  # BCCA: bathroom top right door stud [125:127]
            pygame.Rect(self.x + 3850, self.y + 1550, 50, 50),  # BCCA: bathroom bottom right door stud [237:129]
            pygame.Rect(self.x + 3550, self.y + 1600, 350, 50),  # BCCA: bathroom top middle wall [129]
            pygame.Rect(self.x + 3700, self.y + 1650, 50, 450),  # BCCA: bathroom middle wall [130]
            pygame.Rect(self.x + 3850, self.y + 1350, 300, 50),  # BCCA: bathroom top right wall [131]
            pygame.Rect(self.x + 4100, self.y + 1400, 50, 700),  # BCCA: bathroom right wall [132]

            pygame.Rect(self.x + 7100, self.y + 450, 50, 350),  # BCCA: kitchen right wall [133]
            pygame.Rect(self.x + 5700, self.y + 800, 1200, 50),  # BCCA: kitchen bottom left wall [134:136]
            pygame.Rect(self.x + 7000, self.y + 800, 250, 50),  # BCCA: kitchen bottom right wall [136:138]

            pygame.Rect(self.x + 7350, self.y + 800, 750, 50),  # BCCA: meeting room bottom wall [138:140]
            pygame.Rect(self.x + 7450, self.y + 650, 50, 150),  # BCCA: meeting room middle wall [140:142]

            pygame.Rect(self.x + 6950, self.y + 1100, 700, 50),  # BCCA: incubator top left wall [142]
            pygame.Rect(self.x + 7850, self.y + 1100, 250, 1000),  # BCCA: incubator top right wall [143]
            pygame.Rect(self.x + 6950, self.y + 1150, 50, 400),  # BCCA: incubator left top wall [144:146]
            pygame.Rect(self.x + 6950, self.y + 1650, 50, 450),  # BCCA: incubator left bottom wall [146:148]
            pygame.Rect(self.x + 7650, self.y + 1200, 50, 50),  # BCCA: incubator top entrance left wall [148:150]
            pygame.Rect(self.x + 7800, self.y + 1200, 50, 50),  # BCCA: incubator top entrance right wall [150:152]
            pygame.Rect(self.x + 7000, self.y + 1450, 100, 50),  # BCCA: incubator top room bottom left wall [152:154]
            pygame.Rect(self.x + 7200, self.y + 1450, 100, 50),  # BCCA: incubator top room bottom right wall [154:156]
            pygame.Rect(self.x + 7250, self.y + 1400, 50, 50),  # BCCA: incubator top room middle wall
            pygame.Rect(self.x + 7250, self.y + 1350, 200, 50),  # BCCA: incubator top room middle top wall [156:158]
            pygame.Rect(self.x + 7550, self.y + 1350, 50, 50),  # BCCA: incubator top room bottom right wall [158:160]
            pygame.Rect(self.x + 7600, self.y + 1150, 50, 250),  # BCCA: incubator top room right wall [160]
            pygame.Rect(self.x + 7000, self.y + 1700, 100, 50),  # BCCA: incubator bottom room top left wall [161:163]
            pygame.Rect(self.x + 7200, self.y + 1700, 100, 50),  # BCCA: incubator bottom room top right wall [163:165]
            pygame.Rect(self.x + 7250, self.y + 1750, 50, 50),  # BCCA: incubator bottom room middle wall
            pygame.Rect(self.x + 7250, self.y + 1800, 600, 50),  # BCCA: incubator bottom room top right wall [165:]
        ]

    # These convert methods confine ray-casting lines to be inside the viewport.
    # Returns either the coordinate or the limit of the viewport (top, bottom, left, or right)
    def conform_x_to_view_range(self, num: int):
        coordinate = num + self.x
        if coordinate < self.v_l:
            return self.v_l
        if coordinate > self.v_r:
            return self.v_r
        return coordinate

    def conform_y_to_view_range(self, num: int):
        coordinate = num + self.y
        if coordinate < self.v_t:
            return self.v_t
        if coordinate > self.v_b:
            return self.v_b
        return coordinate

    @property
    def get_wall_segments(self):
        return [
                   {'a': {'x': self.conform_x_to_view_range(seg[0][0]), 'y': self.conform_y_to_view_range(seg[0][1])},
                    'b': {'x': self.conform_x_to_view_range(seg[1][0]), 'y': self.conform_y_to_view_range(seg[1][1])}}
                   for seg in self.wall_segments
                   if
                   self.viewport.collidepoint((seg[0][0] + self.x, seg[0][1] + self.y)) or self.viewport.collidepoint(
                       (seg[1][0] + self.x, seg[1][1] + self.y))] + self.viewport_segments

    @property
    def get_task_rects(self):
        return [
            (pygame.Rect(self.x + 2450, self.y + 450, 500, 500), "Check Inbox"),  # Check Inbox

            (pygame.Rect(self.x + 3600, self.y + 1650, 50, 50), "Refill Hand-Sanitizer"),  # Refill Hand-Sanitizer: left
            (pygame.Rect(self.x + 3800, self.y + 1650, 50, 50), "Refill Hand-Sanitizer"),
            # Refill Hand-Sanitizer: right

            (pygame.Rect(self.x + 7000, self.y + 1050, 50, 50), "Check Temperature"),  # Check Temperature

            (pygame.Rect(self.x + 6150, self.y + 100, 100, 50), "Reset Wifi"),  # Reset Wifi

            (pygame.Rect(self.x + 2100, self.y + 650, 50, 100), "Plug-In Laptops"),  # Plug-In Laptops: top
            (pygame.Rect(self.x + 2100, self.y + 1700, 50, 100), "Plug-In Laptops"),  # Plug-In Laptops: bottom

            (pygame.Rect(self.x + 4300, self.y + 1050, 300, 300), "Wipe down Tables"),  # Wipe down tables: top left
            (pygame.Rect(self.x + 4300, self.y + 1700, 300, 300), "Wipe down Tables"),  # Wipe down tables: bottom left
            (pygame.Rect(self.x + 6500, self.y + 1050, 300, 300), "Wipe down Tables"),  # Wipe down tables: top right
            (pygame.Rect(self.x + 6500, self.y + 1750, 300, 300), "Wipe down Tables"),  # Wipe down tables: bottom right

            (pygame.Rect(self.x + 400, self.y + 1100, 400, 50), "Clean Windows"),  # Clean Windows: left top left
            (pygame.Rect(self.x + 900, self.y + 1100, 400, 50), "Clean Windows"),  # Clean Windows: left top right
            (pygame.Rect(self.x + 400, self.y + 1300, 400, 50), "Clean Windows"),  # Clean Windows: left bottom left
            (pygame.Rect(self.x + 900, self.y + 1300, 400, 50), "Clean Windows"),  # Clean Windows: left bottom right
            (pygame.Rect(self.x + 2350, self.y + 1100, 300, 50), "Clean Windows"),  # Clean Windows: right top left
            (pygame.Rect(self.x + 2750, self.y + 1100, 300, 50), "Clean Windows"),  # Clean Windows: right top right
            (pygame.Rect(self.x + 2350, self.y + 1300, 300, 50), "Clean Windows"),  # Clean Windows: right bottom left
            (pygame.Rect(self.x + 2750, self.y + 1300, 300, 50), "Clean Windows"),  # Clean Windows: right bottom right

            (pygame.Rect(self.x + 6700, self.y + 850, 150, 50), "Nominate For Awards"),  # Nominate for Awards

            (pygame.Rect(self.x + 2300, self.y + 1000, 50, 50), "Collect Trash"),  # Collect Trash: classroom1
            (pygame.Rect(self.x + 2300, self.y + 1400, 50, 50), "Collect Trash"),  # Collect Trash: classroom2
            (pygame.Rect(self.x + 3700, self.y + 1550, 50, 50), "Collect Trash"),  # Collect Trash: bathroom
            (pygame.Rect(self.x + 4350, self.y + 750, 50, 50), "Collect Trash"),  # Collect Trash: breakroom
            (pygame.Rect(self.x + 4150, self.y + 2000, 50, 50), "Collect Trash"),  # Collect Trash: left lobby
            (pygame.Rect(self.x + 6900, self.y + 2000, 50, 50), "Collect Trash"),  # Collect Trash: right lobby
            (pygame.Rect(self.x + 7100, self.y + 850, 50, 50), "Collect Trash"),  # Collect Trash: outside kitchen
            (pygame.Rect(self.x + 6650, self.y + 750, 50, 50), "Collect Trash"),  # Collect Trash: outside kitchen

            (pygame.Rect(self.x + 2450, self.y + 1500, 500, 500), "Do Flashcards"),  # Do Flashcards

            # Sabotages

            (pygame.Rect(self.x + 600, self.y + 1700, 50, 100), "Left A/C top"),  # Left A/C: top
            (pygame.Rect(self.x + 900, self.y + 1850, 100, 50), "Left A/C bottom"),  # Left A/C: bottom
            (pygame.Rect(self.x + 600, self.y + 1700, 50, 100), "Right A/C top"),  # Right A/C: top
            (pygame.Rect(self.x + 600, self.y + 1700, 50, 100), "Right A/C bottom"),  # Right A/C: bottom

            (pygame.Rect(self.x + 3400, self.y + 700, 150, 50), "Lights"),  # Lights

            (pygame.Rect(self.x + 5000, self.y + 150, 50, 100), "Relaunch Zoom"),  # Relaunch Zoom

            (pygame.Rect(self.x + 7050, self.y + 450, 50, 100), "Remove Spoiled Food"),  # Remove Spoiled Food
            (pygame.Rect(self.x + 6400, self.y + 450, 50, 100), "Remove Spoiled Food"),  # Remove Spoiled Food
        ]

    @property
    def get_vent_rects(self):
        return [
            (pygame.Rect(self.x + 170, self.y + 1200, 60, 50), "Left.1"),  # Left system: 1
            (pygame.Rect(self.x + 1795, self.y + 875, 60, 50), "Left.2"),  # Left system: 2
            (pygame.Rect(self.x + 3095, self.y + 1750, 60, 50), "Left.3"),  # Left system: 3
            (pygame.Rect(self.x + 3995, self.y + 425, 60, 50), "Left.4"),  # Left system: 4

            (pygame.Rect(self.x + 5520, self.y + 1950, 60, 50), "Right.1"),  # Right system: 1
            (pygame.Rect(self.x + 6220, self.y + 450, 60, 50), "Right.2"),  # Right system: 2
            (pygame.Rect(self.x + 7195, self.y + 525, 60, 50), "Right.3"),  # Right system: 3
            (pygame.Rect(self.x + 7745, self.y + 1725, 60, 50), "Right.4"),  # Right system: 4
        ]

    def draw_map_image(self, visible_surface: pygame.Surface, shadow_surface: pygame.Surface, draw_lines: bool):
        # Points for shape drawing
        points = []

        unique_points = set()
        for segment in self.get_wall_segments:
            if (('x', segment["a"]["x"]), ('y', segment["a"]["y"])) not in unique_points:
                unique_points.add((('x', segment["a"]["x"]), ('y', segment["a"]["y"])))
            if (('x', segment["b"]["x"]), ('y', segment["b"]["y"])) not in unique_points:
                unique_points.add((('x', segment["b"]["x"]), ('y', segment["b"]["y"])))

        # Find intersection of RAY & SEGMENT
        def get_intersection(ray, segment_instance):
            # RAY in parametric: Point + Delta*t1
            r_px = ray['a']['x']
            r_py = ray['a']['y']
            r_dx = ray['b']['x'] - ray['a']['x']
            r_dy = ray['b']['y'] - ray['a']['y']

            # SEGMENT in parametric: Point + Delta*t2
            s_px = segment_instance['a']['x']
            s_py = segment_instance['a']['y']
            s_dx = segment_instance['b']['x'] - segment_instance['a']['x']
            s_dy = segment_instance['b']['y'] - segment_instance['a']['y']

            # Are they parallel? If so, no intersect
            if r_dx * s_dy == r_dy * s_dx:
                # Unit vectors are the same.
                return None

            # SOLVE FOR t1 & t2
            t2 = (r_dx * (s_py - r_py) + r_dy * (r_px - s_px)) / (s_dx * r_dy - s_dy * r_dx)
            if r_dy == 0:
                t1 = (s_px + s_dx * t2 - r_px) / r_dx
            else:
                t1 = (s_py + s_dy * t2 - r_py) / r_dy

            # Must be within parametric whatevers for RAY/SEGMENT
            if t1 < 0:
                return None
            if t2 < 0 or t2 > 1:
                return None

            # Return the POINT OF INTERSECTION
            return {
                'x': r_px + r_dx * t1,
                'y': r_py + r_dy * t1,
                'param': t1
            }

        #######################################################

        # DRAWING
        def draw(segments):
            # Get all angles
            unique_angles = set()
            for unique_point in unique_points:
                points_dict = dict(unique_point)
                angle = math.atan2(points_dict['y'] - 540, points_dict['x'] - 960)
                unique_angles.update([angle - 0.00001, angle + 0.00001])

            unique_angles = sorted(unique_angles)

            # RAYS IN ALL DIRECTIONS
            for angle in unique_angles:

                # Calculate dx & dy from angle
                dx = math.cos(angle)
                dy = math.sin(angle)

                # Ray from center of screen to player
                ray = {
                    "a": {"x": 960, "y": 540},
                    "b": {"x": 960 + dx, "y": 540 + dy}
                }

                # Find CLOSEST intersection
                closest_intersect = None
                for seg in segments:
                    intersect = get_intersection(ray, seg)
                    if not intersect:
                        continue
                    elif not closest_intersect or intersect["param"] < closest_intersect["param"]:
                        closest_intersect = intersect

                # Intersect angle
                if not closest_intersect:
                    continue
                # Add to list of intersects
                else:
                    points.append((closest_intersect['x'], closest_intersect['y']))

            # DRAW ALL RAYS
            shadow_surface.blit(self.shadow_map_image, (self.x, self.y))
            pygame.draw.polygon(shadow_surface, "#123456", points)

        visible_surface.fill((40, 40, 40))
        visible_surface.blit(self.visible_map_image, (self.x, self.y))
        draw(self.get_wall_segments)
        self.draw_vents(visible_surface)
        self.draw_tasks(visible_surface)
        visible_surface.blit(shadow_surface, (0, 0))

        if draw_lines:
            # Player to corner
            for point in points:
                pygame.draw.line(visible_surface, "#FF00FF", (960, 540), point)

    def draw_collision(self, surface: pygame.Surface):
        # Draw Rects
        # for wall in self.get_wall_rects:
        #     pygame.draw.rect(surface, (0,255,0), wall, 1)

        # Draw segments
        color = "#ff0000"
        for seg in self.get_wall_segments:
            pygame.draw.line(surface, color, (seg["a"]["x"], seg["a"]["y"]), (seg["b"]["x"], seg["b"]["y"]))

    def draw_tasks(self, surface: pygame.Surface):
        for task in self.get_task_rects:
            pygame.draw.rect(surface, (242, 242, 0), task[0], 3)

    def draw_vents(self, surface: pygame.Surface):
        for vent in self.get_vent_rects:
            pygame.draw.rect(surface, (0, 242, 242), vent[0], 3)

    def draw_coordinates(self, surface: pygame.Surface, font: pygame.font):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pos_text = font.render(
            f"X: {round(self.x, 2)}Y: {round(self.y, 3)}" +
            f" ~ X: {round(mouse_x - self.x, 2)}Y: {round(mouse_y - self.y, 3)}",
            True, (255, 0, 0))
        pos_text_rect = pos_text.get_rect()
        pos_text_rect.center = (250, 50)
        surface.blit(pos_text, pos_text_rect)


if __name__ == '__main__':
    import main
