import pygame, math
from pprint import pprint

class Map(object):
    def __init__(self, visible_map_image, shadow_map_image):
        self.x, self.y = 0, 0
        self.visible_map_image = visible_map_image
        self.shadow_map_image = shadow_map_image
        self.width = self.visible_map_image.get_rect().width
        self.height = self.visible_map_image.get_rect().height
        self.x_velocity = 8
        self.y_velocity = 8

        self.viewport = pygame.Rect(210, 0, 1500, 1080)

    @property
    def get_wall_rects(self):
        return (
            pygame.Rect(self.x + 50, self.y + 300, 5250, 50), # Outside: classrooms top wall [4:6]
            pygame.Rect(self.x + 50, self.y + 350, 50, 1750), # Outside: classrooms left wall 
            pygame.Rect(self.x + 50, self.y + 2100, 8100, 50), # Outside: classrooms bottom wall 
            pygame.Rect(self.x + 4950, self.y + 50, 1450, 50), # Outside: offices top wall
            pygame.Rect(self.x + 4950, self.y + 100, 50, 300), # Outside: offices left wall [6:8]
            pygame.Rect(self.x + 6350, self.y + 100, 50, 700), # Outside: offices right wall [8]
            pygame.Rect(self.x + 6400, self.y + 400, 1750, 50), # Outside: kitchen top wall
            pygame.Rect(self.x + 8100, self.y + 450, 50, 1650), # Outside: student door wall
            
            pygame.Rect(self.x + 5400, self.y + 300, 500, 50), # BCCA: top office middle wall [9:11]
            pygame.Rect(self.x + 6000, self.y + 300, 350, 50), # BCCA: top office right wall [11:13]
            pygame.Rect(self.x + 4950, self.y + 500, 50, 300), # BCCA: left office left wall [13:15]
            pygame.Rect(self.x + 4900, self.y + 800, 700, 50), # BCCA: left office bottom wall [15:17]
            pygame.Rect(self.x + 5000, self.y + 550, 600, 50), # BCCA: left office top wall [17:19]
            pygame.Rect(self.x + 5500, self.y + 600, 50, 200), # BCCA: left office right wall
            pygame.Rect(self.x + 5700, self.y + 550, 650, 50), # BCCA: right office top wall [19:21]
            pygame.Rect(self.x + 5750, self.y + 600, 50, 200), # BCCA: right office right wall

            pygame.Rect(self.x + 4650, self.y + 350, 50, 450), # BCCA: breakroom right wall [21]
            pygame.Rect(self.x + 4300, self.y + 800, 450, 50), # BCCA: breakroom bottom right wall [21:23]
            pygame.Rect(self.x + 4150, self.y + 800, 50, 50), # BCCA: breakroom bottom left wall [23:25]
            pygame.Rect(self.x + 4100, self.y + 350, 50, 750), # BCCA: breakroom left wall [25:27]

            pygame.Rect(self.x + 4350, self.y + 1100, 200, 200), # BCCA: lobby top left block [27:29]
            pygame.Rect(self.x + 4350, self.y + 1750, 200, 200), # BCCA: lobby bottom left block [29:31]
            pygame.Rect(self.x + 6550, self.y + 1100, 200, 200), # BCCA: lobby top right block [31:33]
            pygame.Rect(self.x + 6550, self.y + 1800, 200, 200), # BCCA: lobby bottom right block [33:35]
            pygame.Rect(self.x + 5650, self.y + 1200, 700, 50), # BCCA: lobby top right wall [35:37]
            pygame.Rect(self.x + 4750, self.y + 1200, 700, 50), # BCCA: lobby top left wall [37:39]
            pygame.Rect(self.x + 4750, self.y + 1250, 50, 150), # BCCA: lobby left top wall [39:41]
            pygame.Rect(self.x + 4750, self.y + 1600, 50, 150), # BCCA: lobby left bottom wall [41:43]
            pygame.Rect(self.x + 4750, self.y + 1750, 700, 50), # BCCA: lobby bottom left wall [43:45]
            pygame.Rect(self.x + 5650, self.y + 1750, 700, 50), # BCCA: lobby bottom right wall [45:47]
            pygame.Rect(self.x + 6300, self.y + 1250, 50, 150), # BCCA: lobby right top wall [47:49]
            pygame.Rect(self.x + 6300, self.y + 1600, 50, 150), # BCCA: lobby right bottom wall [49:51]

            pygame.Rect(self.x + 3800, self.y + 1050, 300, 50), # BCCA: supply bottom right wall [51:53]
            pygame.Rect(self.x + 3600, self.y + 600, 50, 450), # BCCA: supply middle wall [53:55]
            pygame.Rect(self.x + 3350, self.y + 750, 250, 50), # BCCA: supply middle left wall

            pygame.Rect(self.x + 3150, self.y + 1100, 50, 50), # BCCA: hallway top door stud [55:57]
            pygame.Rect(self.x + 3150, self.y + 1300, 50, 50), # BCCA: hallway bottom door stud [57:59]

            pygame.Rect(self.x + 3300, self.y + 350, 50, 700), # BCCA: classroom1 right wall [59]
            pygame.Rect(self.x + 2250, self.y + 1050, 1450, 50), # BCCA: classroom1 bottom right wall [60:62]
            pygame.Rect(self.x + 2500, self.y + 500, 400, 400), # BCCA: classroom1 block [62:64]
            pygame.Rect(self.x + 1900, self.y + 1050, 250, 50), # BCCA: classroom1 bottom left wall [64:66]
            pygame.Rect(self.x + 2050, self.y + 350, 50, 100), # BCCA: classroom1 left top wall [66:68]
            pygame.Rect(self.x + 2050, self.y + 550, 50, 500), # BCCA: classroom1 left bottom wall [68:70]

            pygame.Rect(self.x + 1500, self.y + 1050, 250, 50), # BCCA: breakoutroom1 bottom left wall [70:72]
            pygame.Rect(self.x + 1750, self.y + 350, 150, 400), # BCCA: breakoutroom1 table [72:74]
            pygame.Rect(self.x + 1550, self.y + 350, 50, 100), # BCCA: breakoutroom1 left top wall [74:76]
            pygame.Rect(self.x + 1550, self.y + 550, 50, 500), # BCCA: breakoutroom1 left bottom wall [76:78]

            pygame.Rect(self.x + 1100, self.y + 600, 200, 200), # BCCA: classroom3 right block [78:80]
            pygame.Rect(self.x + 600, self.y + 600, 200, 200), # BCCA: classroom3 left block [80:82]
            pygame.Rect(self.x + 300, self.y + 900, 50, 150), # BCCA: classroom3 middle wall [82]
            pygame.Rect(self.x + 300, self.y + 1050, 1100, 50), # BCCA: classroom3 bottom left wall [83:85]
            pygame.Rect(self.x + 250, self.y + 850, 100, 50), # BCCA: classroom3 middle right wall [85:87]
            pygame.Rect(self.x + 100, self.y + 850, 50, 50), # BCCA: classroom3 middle left wall [87:89]

            pygame.Rect(self.x + 300, self.y + 1350, 1100, 50), # BCCA: classroom4 top left wall [89:91]
            pygame.Rect(self.x + 300, self.y + 1400, 50, 150), # BCCA: classroom4 middle wall [91]
            pygame.Rect(self.x + 250, self.y + 1550, 100, 50), # BCCA: classroom4 middle right wall [92:94]
            pygame.Rect(self.x + 100, self.y + 1550, 50, 50), # BCCA: classroom4 middle left wall [94:96]
            pygame.Rect(self.x + 550, self.y + 1600, 200, 50), # BCCA: classroom4 center top wall [96:98]
            pygame.Rect(self.x + 550, self.y + 1650, 50, 250), # BCCA: classroom4 center left wall [98]
            pygame.Rect(self.x + 550, self.y + 1900, 500, 50), # BCCA: classroom4 center bottom wall [99]
            pygame.Rect(self.x + 1050, self.y + 1800, 50, 150), # BCCA: classroom4 center right wall [100:102]

            pygame.Rect(self.x + 1500, self.y + 1350, 250, 50), # BCCA: breakoutroom2 top left wall [102:104]
            pygame.Rect(self.x + 1900, self.y + 1350, 250, 50), # BCCA: breakoutroom2 top right wall [104:106]
            pygame.Rect(self.x + 1550, self.y + 1400, 50, 500), # BCCA: breakoutroom2 left top wall [106:108]
            pygame.Rect(self.x + 1550, self.y + 2000, 50, 100), # BCCA: breakoutroom2 left bottom wall [108:110]
            pygame.Rect(self.x + 1750, self.y + 1500, 150, 450), # BCCA: breakoutroom2 table [110:112]
            pygame.Rect(self.x + 2050, self.y + 1400, 50, 500), # BCCA: breakoutroom2 right top wall [112:114]
            pygame.Rect(self.x + 2050, self.y + 2000, 50, 100), # BCCA: breakoutroom2 right bottom wall [114:116]

            pygame.Rect(self.x + 2250, self.y + 1350, 1350, 50), # BCCA: classroom2 top right wall [116:118]
            pygame.Rect(self.x + 2500, self.y + 1550, 400, 400), # BCCA: classroom2 block [118:120]
            pygame.Rect(self.x + 3300, self.y + 1400, 50, 700), # BCCA: classroom2 right wall [120]

            pygame.Rect(self.x + 3550, self.y + 1400, 50, 50), # BCCA: bathroom top left door stud [121:123]
            pygame.Rect(self.x + 3550, self.y + 1550, 50, 50), # BCCA: bathroom bottom left door stud [123:125]
            pygame.Rect(self.x + 3850, self.y + 1400, 50, 50), # BCCA: bathroom top right door stud [125:127]
            pygame.Rect(self.x + 3850, self.y + 1550, 50, 50), # BCCA: bathroom bottom right door stud [237:129]
            pygame.Rect(self.x + 3550, self.y + 1600, 350, 50), # BCCA: bathroom top middle wall [129]
            pygame.Rect(self.x + 3700, self.y + 1650, 50, 450), # BCCA: bathroom middle wall [130]
            pygame.Rect(self.x + 3850, self.y + 1350, 300, 50), # BCCA: bathroom top right wall [131]
            pygame.Rect(self.x + 4100, self.y + 1400, 50, 700), # BCCA: bathroom right wall [132]

            pygame.Rect(self.x + 7100, self.y + 450, 50, 350), # BCCA: kitchen right wall [133]
            pygame.Rect(self.x + 5700, self.y + 800, 1200, 50), # BCCA: kitchen bottom left wall [134:136]
            pygame.Rect(self.x + 7000, self.y + 800, 250, 50), # BCCA: kitchen bottom right wall [136:138]
            
            pygame.Rect(self.x + 7350, self.y + 800, 750, 50), # BCCA: meeting room bottom wall [138:140]
            pygame.Rect(self.x + 7450, self.y + 650, 50, 150), # BCCA: meeting room middle wall [140:142]

            pygame.Rect(self.x + 6950, self.y + 1100, 700, 50), # BCCA: incubator top left wall [142]
            pygame.Rect(self.x + 7850, self.y + 1100, 250, 1000), # BCCA: incubator top right wall [143]
            pygame.Rect(self.x + 6950, self.y + 1150, 50, 400), # BCCA: incubator left top wall [144:146]
            pygame.Rect(self.x + 6950, self.y + 1650, 50, 450), # BCCA: incubator left bottom wall [146:148]
            pygame.Rect(self.x + 7650, self.y + 1200, 50, 50), # BCCA: incubator top entrance left wall [148:150]
            pygame.Rect(self.x + 7800, self.y + 1200, 50, 50), # BCCA: incubator top entrance right wall [150:152]
            pygame.Rect(self.x + 7000, self.y + 1450, 100, 50), # BCCA: incubator top room bottom left wall [152:154]
            pygame.Rect(self.x + 7200, self.y + 1450, 100, 50), # BCCA: incubator top room bottom right wall [154:156]
            pygame.Rect(self.x + 7250, self.y + 1400, 50, 50), # BCCA: incubator top room middle wall
            pygame.Rect(self.x + 7250, self.y + 1350, 200, 50), # BCCA: incubator top room middle top wall [156:158]
            pygame.Rect(self.x + 7550, self.y + 1350, 50, 50), # BCCA: incubator top room bottom right wall [158:160]
            pygame.Rect(self.x + 7600, self.y + 1150, 50, 250), # BCCA: incubator top room right wall [160]
            pygame.Rect(self.x + 7000, self.y + 1700, 100, 50), # BCCA: incubator bottom room top left wall [161:163]
            pygame.Rect(self.x + 7200, self.y + 1700, 100, 50), # BCCA: incubator bottom room top right wall [163:165]
            pygame.Rect(self.x + 7250, self.y + 1750, 50, 50), # BCCA: incubator bottom room middle wall
            pygame.Rect(self.x + 7250, self.y + 1800, 600, 50), # BCCA: incubator bottom room top right wall [165:]
        )

    @property
    def get_wall_segments(self):
        # topleft-topright, topright-bottomright, bottomright-bottomleft, bottomleft-topleft
        segments = (
            # Viewport: top
            {'a': {'x': 210, 'y': 0}, 'b': {'x': 1709, 'y': 0}}, 
            # Viewport: right
            {'a': {'x': 1709, 'y': 0}, 'b': {'x': 1709, 'y': 1079}},  
            # Viewport: bottom
            {'a': {'x': 210, 'y': 1079}, 'b': {'x': 1709, 'y': 1079}},  
            # Viewport: left
            {'a': {'x': 210, 'y': 1079}, 'b': {'x': 210, 'y': 0}},  

            # Outside: classrooms top wall
            {'a': {'x': self.x + 5000, 'y': self.y + 300}, 'b': {'x': self.x + 5300, 'y': self.y + 350}}, 
            {'a': {'x': self.x + 100, 'y': self.y + 350}, 'b': {'x': self.x + 5300, 'y': self.y + 300}}, 
            # Outside: offices left wall
            {'a': {'x': self.x + 4950, 'y': self.y + 350}, 'b': {'x': self.x + 5000, 'y': self.y + 400}}, 
            {'a': {'x': self.x + 4950, 'y': self.y + 400}, 'b': {'x': self.x + 5000, 'y': self.y + 100}}, 
            # Outside: offices right wall 
            {'a': {'x': self.x + 6350, 'y': self.y + 100}, 'b': {'x': self.x + 6400, 'y': self.y + 800}}, 


            # BCCA: top office middle wall
            {'a': {'x': self.x + 5400, 'y': self.y + 300}, 'b': {'x': self.x + 5900, 'y': self.y + 350}}, 
            {'a': {'x': self.x + 5400, 'y': self.y + 350}, 'b': {'x': self.x + 5900, 'y': self.y + 300}}, 
            # BCCA: top office right wall
            {'a': {'x': self.x + 6000, 'y': self.y + 300}, 'b': {'x': self.x + 6350, 'y': self.y + 350}}, 
            {'a': {'x': self.x + 6000, 'y': self.y + 350}, 'b': {'x': self.x + 6350, 'y': self.y + 300}}, 
            # BCCA: left office left wall
            {'a': {'x': self.x + 4950, 'y': self.y + 500}, 'b': {'x': self.x + 5000, 'y': self.y + 550}},  
            {'a': {'x': self.x + 4950, 'y': self.y + 800}, 'b': {'x': self.x + 5000, 'y': self.y + 500}}, 
            # BCCA: left office bottom wall
            {'a': {'x': self.x + 4900, 'y': self.y + 800}, 'b': {'x': self.x + 5600, 'y': self.y + 850}}, 
            {'a': {'x': self.x + 4900, 'y': self.y + 850}, 'b': {'x': self.x + 5600, 'y': self.y + 800}}, 
            # BCCA: left office top wall
            {'a': {'x': self.x + 5000, 'y': self.y + 550}, 'b': {'x': self.x + 5600, 'y': self.y + 600}}, 
            {'a': {'x': self.x + 5550, 'y': self.y + 600}, 'b': {'x': self.x + 5600, 'y': self.y + 550}}, 
            # BCCA: right office top wall
            {'a': {'x': self.x + 5700, 'y': self.y + 550}, 'b': {'x': self.x + 5750, 'y': self.y + 600}}, 
            {'a': {'x': self.x + 5700, 'y': self.y + 600}, 'b': {'x': self.x + 6350, 'y': self.y + 550}}, 


            # BCCA: breakroom right wall
            {'a': {'x': self.x + 4675, 'y': self.y + 800}, 'b': {'x': self.x + 4675, 'y': self.y + 350}}, 
            # BCCA: breakroom bottom right wall
            {'a': {'x': self.x + 4300, 'y': self.y + 800}, 'b': {'x': self.x + 4750, 'y': self.y + 850}}, 
            {'a': {'x': self.x + 4300, 'y': self.y + 850}, 'b': {'x': self.x + 4750, 'y': self.y + 800}}, 
            # BCCA: breakroom bottom left wall
            {'a': {'x': self.x + 4150, 'y': self.y + 800}, 'b': {'x': self.x + 4200, 'y': self.y + 850}}, 
            {'a': {'x': self.x + 4150, 'y': self.y + 850}, 'b': {'x': self.x + 4200, 'y': self.y + 800}},
            # BCCA: breakroom left wall
            {'a': {'x': self.x + 4100, 'y': self.y + 350}, 'b': {'x': self.x + 4150, 'y': self.y + 1100}}, 


            # BCCA: lobby top left block
            {'a': {'x': self.x + 4350, 'y': self.y + 1100}, 'b': {'x': self.x + 4550, 'y': self.y + 1300}}, 
            {'a': {'x': self.x + 4350, 'y': self.y + 1300}, 'b': {'x': self.x + 4550, 'y': self.y + 1100}}, 
            # BCCA: lobby bottom left block
            {'a': {'x': self.x + 4350, 'y': self.y + 1750}, 'b': {'x': self.x + 4550, 'y': self.y + 1950}}, 
            {'a': {'x': self.x + 4350, 'y': self.y + 1950}, 'b': {'x': self.x + 4550, 'y': self.y + 1750}}, 
            # BCCA: lobby top right block
            {'a': {'x': self.x + 6550, 'y': self.y + 1100}, 'b': {'x': self.x + 6750, 'y': self.y + 1300}}, 
            {'a': {'x': self.x + 6550, 'y': self.y + 1300}, 'b': {'x': self.x + 6750, 'y': self.y + 1100}}, 
            # BCCA: lobby bottom right block
            {'a': {'x': self.x + 6550, 'y': self.y + 1800}, 'b': {'x': self.x + 6750, 'y': self.y + 2000}}, 
            {'a': {'x': self.x + 6550, 'y': self.y + 2000}, 'b': {'x': self.x + 6750, 'y': self.y + 1800}}, 
            # BCCA: lobby top right wall
            {'a': {'x': self.x + 5650, 'y': self.y + 1200}, 'b': {'x': self.x + 6300, 'y': self.y + 1250}}, 
            {'a': {'x': self.x + 5650, 'y': self.y + 1250}, 'b': {'x': self.x + 6350, 'y': self.y + 1200}}, 
            # BCCA: lobby top left wall
            {'a': {'x': self.x + 4750, 'y': self.y + 1200}, 'b': {'x': self.x + 5450, 'y': self.y + 1250}}, 
            {'a': {'x': self.x + 4800, 'y': self.y + 1250}, 'b': {'x': self.x + 5450, 'y': self.y + 1200}}, 
            # BCCA: lobby left top wall
            {'a': {'x': self.x + 4750, 'y': self.y + 1200}, 'b': {'x': self.x + 4800, 'y': self.y + 1400}},
            {'a': {'x': self.x + 4750, 'y': self.y + 1400}, 'b': {'x': self.x + 4800, 'y': self.y + 1250}},
            # BCCA: lobby left bottom wall
            {'a': {'x': self.x + 4750, 'y': self.y + 1600}, 'b': {'x': self.x + 4800, 'y': self.y + 1750}}, 
            {'a': {'x': self.x + 4750, 'y': self.y + 1800}, 'b': {'x': self.x + 4800, 'y': self.y + 1600}}, 
            # BCCA: lobby bottom left wall
            {'a': {'x': self.x + 4800, 'y': self.y + 1750}, 'b': {'x': self.x + 5450, 'y': self.y + 1800}}, 
            {'a': {'x': self.x + 4750, 'y': self.y + 1800}, 'b': {'x': self.x + 5450, 'y': self.y + 1750}}, 
            # BCCA: lobby bottom right wall
            {'a': {'x': self.x + 5650, 'y': self.y + 1750}, 'b': {'x': self.x + 6350, 'y': self.y + 1800}}, 
            {'a': {'x': self.x + 5650, 'y': self.y + 1800}, 'b': {'x': self.x + 6300, 'y': self.y + 1750}}, 
            # BCCA: lobby right top wall
            {'a': {'x': self.x + 6300, 'y': self.y + 1250}, 'b': {'x': self.x + 6350, 'y': self.y + 1400}}, 
            {'a': {'x': self.x + 6300, 'y': self.y + 1400}, 'b': {'x': self.x + 6350, 'y': self.y + 1200}}, 
            # BCCA: lobby right bottom wall
            {'a': {'x': self.x + 6300, 'y': self.y + 1600}, 'b': {'x': self.x + 6350, 'y': self.y + 1800}}, 
            {'a': {'x': self.x + 6300, 'y': self.y + 1750}, 'b': {'x': self.x + 6350, 'y': self.y + 1600}}, 


            # BCCA: supply bottom right wall
            {'a': {'x': self.x + 3800, 'y': self.y + 1050}, 'b': {'x': self.x + 4150, 'y': self.y + 1100}}, 
            {'a': {'x': self.x + 3800, 'y': self.y + 1100}, 'b': {'x': self.x + 4100, 'y': self.y + 1050}}, 
            # BCCA: supply middle wall
            {'a': {'x': self.x + 3600, 'y': self.y + 600}, 'b': {'x': self.x + 3650, 'y': self.y + 1050}}, 
            {'a': {'x': self.x + 3600, 'y': self.y + 750}, 'b': {'x': self.x + 3650, 'y': self.y + 600}}, 


            # BCCA: hallway top door stud
            {'a': {'x': self.x + 3150, 'y': self.y + 1100}, 'b': {'x': self.x + 3200, 'y': self.y + 1150}}, 
            {'a': {'x': self.x + 3150, 'y': self.y + 1150}, 'b': {'x': self.x + 3200, 'y': self.y + 1100}}, 
            # BCCA: hallway bottom door stud
            {'a': {'x': self.x + 3150, 'y': self.y + 1300}, 'b': {'x': self.x + 3200, 'y': self.y + 1350}}, 
            {'a': {'x': self.x + 3150, 'y': self.y + 1350}, 'b': {'x': self.x + 3200, 'y': self.y + 1300}}, 


            # BCCA: classroom1 right wall
            {'a': {'x': self.x + 3300, 'y': self.y + 350}, 'b': {'x': self.x + 3350, 'y': self.y + 1050}},
            # BCCA: classroom1 bottom right wall
            {'a': {'x': self.x + 2250, 'y': self.y + 1050}, 'b': {'x': self.x + 3700, 'y': self.y + 1100}}, 
            {'a': {'x': self.x + 2250, 'y': self.y + 1100}, 'b': {'x': self.x + 3700, 'y': self.y + 1050}}, 
            # BCCA: classroom1 block
            {'a': {'x': self.x + 2500, 'y': self.y + 500}, 'b': {'x': self.x + 2900, 'y': self.y + 900}}, 
            {'a': {'x': self.x + 2500, 'y': self.y + 900}, 'b': {'x': self.x + 2900, 'y': self.y + 500}}, 
            # BCCA: classroom1 bottom left wall
            {'a': {'x': self.x + 1900, 'y': self.y + 1050}, 'b': {'x': self.x + 2150, 'y': self.y + 1100}}, 
            {'a': {'x': self.x + 1900, 'y': self.y + 1100}, 'b': {'x': self.x + 2150, 'y': self.y + 1050}}, 
            # BCCA: classroom1 left top wall
            {'a': {'x': self.x + 2050, 'y': self.y + 350}, 'b': {'x': self.x + 2100, 'y': self.y + 450}}, 
            {'a': {'x': self.x + 2050, 'y': self.y + 450}, 'b': {'x': self.x + 2100, 'y': self.y + 350}}, 
            # BCCA: classroom1 left bottom wall
            {'a': {'x': self.x + 2050, 'y': self.y + 550}, 'b': {'x': self.x + 2100, 'y': self.y + 1050}}, 
            {'a': {'x': self.x + 2050, 'y': self.y + 1050}, 'b': {'x': self.x + 2100, 'y': self.y + 550}}, 


            # BCCA: breakoutroom1 bottom left wall
            {'a': {'x': self.x + 1500, 'y': self.y + 1050}, 'b': {'x': self.x + 1750, 'y': self.y + 1100}}, 
            {'a': {'x': self.x + 1500, 'y': self.y + 1100}, 'b': {'x': self.x + 1750, 'y': self.y + 1050}}, 
            # BCCA: breakoutroom1 table
            {'a': {'x': self.x + 1750, 'y': self.y + 350}, 'b': {'x': self.x + 1900, 'y': self.y + 750}}, 
            {'a': {'x': self.x + 1750, 'y': self.y + 750}, 'b': {'x': self.x + 1900, 'y': self.y + 350}}, 
            # BCCA: breakoutroom1 left top wall
            {'a': {'x': self.x + 1550, 'y': self.y + 350}, 'b': {'x': self.x + 1600, 'y': self.y + 450}}, 
            {'a': {'x': self.x + 1550, 'y': self.y + 450}, 'b': {'x': self.x + 1600, 'y': self.y + 350}}, 
            # BCCA: breakoutroom1 left bottom wall
            {'a': {'x': self.x + 1550, 'y': self.y + 550}, 'b': {'x': self.x + 1600, 'y': self.y + 1050}}, 
            {'a': {'x': self.x + 1550, 'y': self.y + 1050}, 'b': {'x': self.x + 1600, 'y': self.y + 550}}, 


            # BCCA: classroom3 right block
            {'a': {'x': self.x + 1100, 'y': self.y + 600}, 'b': {'x': self.x + 1300, 'y': self.y + 800}}, 
            {'a': {'x': self.x + 1100, 'y': self.y + 800}, 'b': {'x': self.x + 1300, 'y': self.y + 600}}, 
            # BCCA: classroom3 left block
            {'a': {'x': self.x + 600, 'y': self.y + 600}, 'b': {'x': self.x + 800, 'y': self.y + 800}}, 
            {'a': {'x': self.x + 600, 'y': self.y + 800}, 'b': {'x': self.x + 800, 'y': self.y + 600}}, 
            # BCCA: classroom3 middle wall
            {'a': {'x': self.x + 300, 'y': self.y + 900}, 'b': {'x': self.x + 350, 'y': self.y + 1050}}, 
            # BCCA: classroom3 bottom left wall
            {'a': {'x': self.x + 350, 'y': self.y + 1050}, 'b': {'x': self.x + 1400, 'y': self.y + 1100}}, 
            {'a': {'x': self.x + 300, 'y': self.y + 1100}, 'b': {'x': self.x + 1400, 'y': self.y + 1050}}, 
            # BCCA: classroom3 middle right wall
            {'a': {'x': self.x + 250, 'y': self.y + 850}, 'b': {'x': self.x + 300, 'y': self.y + 900}}, 
            {'a': {'x': self.x + 250, 'y': self.y + 900}, 'b': {'x': self.x + 350, 'y': self.y + 850}}, 
            # BCCA: classroom3 middle left wall
            {'a': {'x': self.x + 100, 'y': self.y + 850}, 'b': {'x': self.x + 150, 'y': self.y + 900}}, 
            {'a': {'x': self.x + 100, 'y': self.y + 900}, 'b': {'x': self.x + 150, 'y': self.y + 850}}, 


            # BCCA: classroom4 top left wall
            {'a': {'x': self.x + 300, 'y': self.y + 1350}, 'b': {'x': self.x + 1400, 'y': self.y + 1400}}, 
            {'a': {'x': self.x + 350, 'y': self.y + 1400}, 'b': {'x': self.x + 1400, 'y': self.y + 1350}}, 
            # BCCA: classroom4 middle wall
            {'a': {'x': self.x + 300, 'y': self.y + 1550}, 'b': {'x': self.x + 350, 'y': self.y + 1400}},  
            # BCCA: classroom4 middle right wall
            {'a': {'x': self.x + 250, 'y': self.y + 1550}, 'b': {'x': self.x + 350, 'y': self.y + 1600}}, 
            {'a': {'x': self.x + 250, 'y': self.y + 1600}, 'b': {'x': self.x + 300, 'y': self.y + 1550}}, 
            # BCCA: classroom4 middle left wall
            {'a': {'x': self.x + 100, 'y': self.y + 1550}, 'b': {'x': self.x + 150, 'y': self.y + 1600}}, 
            {'a': {'x': self.x + 100, 'y': self.y + 1600}, 'b': {'x': self.x + 150, 'y': self.y + 1550}}, 
            # BCCA: classroom4 center top wall
            {'a': {'x': self.x + 550, 'y': self.y + 1600}, 'b': {'x': self.x + 750, 'y': self.y + 1650}}, 
            {'a': {'x': self.x + 600, 'y': self.y + 1650}, 'b': {'x': self.x + 750, 'y': self.y + 1600}}, 
            # BCCA: classroom4 center left wall
            {'a': {'x': self.x + 550, 'y': self.y + 1950}, 'b': {'x': self.x + 600, 'y': self.y + 1650}}, 
            # BCCA: classroom4 center bottom wall 
            {'a': {'x': self.x + 550, 'y': self.y + 1950}, 'b': {'x': self.x + 1050, 'y': self.y + 1900}}, 
            # BCCA: classroom4 center right wall
            {'a': {'x': self.x + 1050, 'y': self.y + 1800}, 'b': {'x': self.x + 1100, 'y': self.y + 1950}},
            {'a': {'x': self.x + 1050, 'y': self.y + 1900}, 'b': {'x': self.x + 1100, 'y': self.y + 1800}},


            # BCCA: breakoutroom2 top left wall
            {'a': {'x': self.x + 1500, 'y': self.y + 1350}, 'b': {'x': self.x + 1750, 'y': self.y + 1400}}, 
            {'a': {'x': self.x + 1500, 'y': self.y + 1400}, 'b': {'x': self.x + 1750, 'y': self.y + 1350}}, 
            # BCCA: breakoutroom2 top right wall
            {'a': {'x': self.x + 1900, 'y': self.y + 1350}, 'b': {'x': self.x + 2150, 'y': self.y + 1400}}, 
            {'a': {'x': self.x + 1900, 'y': self.y + 1400}, 'b': {'x': self.x + 2150, 'y': self.y + 1350}},
            # BCCA: breakoutroom2 left top wall
            {'a': {'x': self.x + 1550, 'y': self.y + 1400}, 'b': {'x': self.x + 1600, 'y': self.y + 1900}}, 
            {'a': {'x': self.x + 1550, 'y': self.y + 1900}, 'b': {'x': self.x + 1600, 'y': self.y + 1400}}, 
            # BCCA: breakoutroom2 left bottom wall
            {'a': {'x': self.x + 1550, 'y': self.y + 2000}, 'b': {'x': self.x + 1600, 'y': self.y + 2100}}, 
            {'a': {'x': self.x + 1550, 'y': self.y + 2100}, 'b': {'x': self.x + 1600, 'y': self.y + 2000}}, 
            # BCCA: breakoutroom2 table
            {'a': {'x': self.x + 1750, 'y': self.y + 1500}, 'b': {'x': self.x + 1900, 'y': self.y + 1950}}, 
            {'a': {'x': self.x + 1750, 'y': self.y + 1950}, 'b': {'x': self.x + 1900, 'y': self.y + 1500}}, 
            # BCCA: breakoutroom2 right top wall
            {'a': {'x': self.x + 2050, 'y': self.y + 1400}, 'b': {'x': self.x + 2100, 'y': self.y + 1900}}, 
            {'a': {'x': self.x + 2050, 'y': self.y + 1900}, 'b': {'x': self.x + 2100, 'y': self.y + 1400}}, 
            # BCCA: breakoutroom2 right bottom wall
            {'a': {'x': self.x + 2050, 'y': self.y + 2000}, 'b': {'x': self.x + 2100, 'y': self.y + 2100}}, 
            {'a': {'x': self.x + 2050, 'y': self.y + 2100}, 'b': {'x': self.x + 2100, 'y': self.y + 2000}}, 


            # BCCA: classroom2 top right wall
            {'a': {'x': self.x + 2250, 'y': self.y + 1350}, 'b': {'x': self.x + 3550, 'y': self.y + 1400}}, 
            {'a': {'x': self.x + 2250, 'y': self.y + 1400}, 'b': {'x': self.x + 3600, 'y': self.y + 1350}}, 
            # BCCA: classroom2 block
            {'a': {'x': self.x + 2500, 'y': self.y + 1550}, 'b': {'x': self.x + 2900, 'y': self.y + 1950}}, 
            {'a': {'x': self.x + 2500, 'y': self.y + 1950}, 'b': {'x': self.x + 2900, 'y': self.y + 1550}}, 
            # BCCA: classroom2 right wall
            {'a': {'x': self.x + 3300, 'y': self.y + 1400}, 'b': {'x': self.x + 3350, 'y': self.y + 2100}}, 


            # BCCA: bathroom top left door stud 
            {'a': {'x': self.x + 3550, 'y': self.y + 1400}, 'b': {'x': self.x + 3600, 'y': self.y + 1450}}, 
            {'a': {'x': self.x + 3550, 'y': self.y + 1450}, 'b': {'x': self.x + 3600, 'y': self.y + 1350}}, 
            # BCCA: bathroom bottom left door stud
            {'a': {'x': self.x + 3550, 'y': self.y + 1550}, 'b': {'x': self.x + 3600, 'y': self.y + 1600}}, 
            {'a': {'x': self.x + 3550, 'y': self.y + 1650}, 'b': {'x': self.x + 3600, 'y': self.y + 1550}}, 
            # BCCA: bathroom top right door stud
            {'a': {'x': self.x + 3850, 'y': self.y + 1350}, 'b': {'x': self.x + 3900, 'y': self.y + 1450}}, 
            {'a': {'x': self.x + 3850, 'y': self.y + 1450}, 'b': {'x': self.x + 3900, 'y': self.y + 1400}}, 
            # BCCA: bathroom bottom right door stud
            {'a': {'x': self.x + 3850, 'y': self.y + 1550}, 'b': {'x': self.x + 3900, 'y': self.y + 1650}}, 
            {'a': {'x': self.x + 3850, 'y': self.y + 1600}, 'b': {'x': self.x + 3900, 'y': self.y + 1550}}, 
            # BCCA: bathroom top middle wall
            {'a': {'x': self.x + 3600, 'y': self.y + 1600}, 'b': {'x': self.x + 3900, 'y': self.y + 1650}}, 
            # BCCA: bathroom middle wall
            {'a': {'x': self.x + 3700, 'y': self.y + 1650}, 'b': {'x': self.x + 3750, 'y': self.y + 2100}}, 
            # BCCA: bathroom top right wall
            {'a': {'x': self.x + 3900, 'y': self.y + 1400}, 'b': {'x': self.x + 4150, 'y': self.y + 1350}}, 
            # BCCA: bathroom right wall
            {'a': {'x': self.x + 4100, 'y': self.y + 2100}, 'b': {'x': self.x + 4150, 'y': self.y + 1350}}, 


            # BCCA: kitchen right wall
            {'a': {'x': self.x + 7100, 'y': self.y + 450}, 'b': {'x': self.x + 7150, 'y': self.y + 800}}, 
            # BCCA: kitchen bottom left wall
            {'a': {'x': self.x + 5700, 'y': self.y + 800}, 'b': {'x': self.x + 6900, 'y': self.y + 850}}, 
            {'a': {'x': self.x + 5700, 'y': self.y + 850}, 'b': {'x': self.x + 6900, 'y': self.y + 800}}, 
            # BCCA: kitchen bottom right wall
            {'a': {'x': self.x + 7000, 'y': self.y + 800}, 'b': {'x': self.x + 7250, 'y': self.y + 850}}, 
            {'a': {'x': self.x + 7000, 'y': self.y + 850}, 'b': {'x': self.x + 7250, 'y': self.y + 800}}, 


            # BCCA: meeting room bottom wall
            {'a': {'x': self.x + 7350, 'y': self.y + 800}, 'b': {'x': self.x + 8100, 'y': self.y + 850}}, 
            {'a': {'x': self.x + 7350, 'y': self.y + 850}, 'b': {'x': self.x + 8100, 'y': self.y + 800}}, 
            # BCCA: meeting room middle wall
            {'a': {'x': self.x + 7450, 'y': self.y + 650}, 'b': {'x': self.x + 7500, 'y': self.y + 800}}, 
            {'a': {'x': self.x + 7450, 'y': self.y + 800}, 'b': {'x': self.x + 7500, 'y': self.y + 650}}, 


            # BCCA: incubator top left wall
            {'a': {'x': self.x + 6999, 'y': self.y + 1149}, 'b': {'x': self.x + 7650, 'y': self.y + 1100}}, 
            # BCCA: incubator top right wall 
            {'a': {'x': self.x + 7850, 'y': self.y + 1100}, 'b': {'x': self.x + 7900, 'y': self.y + 2150}}, 
            # BCCA: incubator left top wall
            {'a': {'x': self.x + 6950, 'y': self.y + 1100}, 'b': {'x': self.x + 7000, 'y': self.y + 1550}}, 
            {'a': {'x': self.x + 6950, 'y': self.y + 1550}, 'b': {'x': self.x + 6999, 'y': self.y + 1149}}, 
            # BCCA: incubator left bottom wall
            {'a': {'x': self.x + 6950, 'y': self.y + 1650}, 'b': {'x': self.x + 7000, 'y': self.y + 2100}}, 
            {'a': {'x': self.x + 6950, 'y': self.y + 2100}, 'b': {'x': self.x + 7000, 'y': self.y + 1650}},
            # BCCA: incubator top entrance left wall
            {'a': {'x': self.x + 7650, 'y': self.y + 1200}, 'b': {'x': self.x + 7700, 'y': self.y + 1250}}, 
            {'a': {'x': self.x + 7650, 'y': self.y + 1250}, 'b': {'x': self.x + 7700, 'y': self.y + 1200}}, 
            # BCCA: incubator top entrance right wall
            {'a': {'x': self.x + 7800, 'y': self.y + 1200}, 'b': {'x': self.x + 7850, 'y': self.y + 1250}}, 
            {'a': {'x': self.x + 7800, 'y': self.y + 1250}, 'b': {'x': self.x + 7850, 'y': self.y + 1200}}, 
            # BCCA: incubator top room bottom left wall
            {'a': {'x': self.x + 7000, 'y': self.y + 1450}, 'b': {'x': self.x + 7100, 'y': self.y + 1500}}, 
            {'a': {'x': self.x + 7000, 'y': self.y + 1500}, 'b': {'x': self.x + 7100, 'y': self.y + 1450}}, 
            # BCCA: incubator top room bottom right wall
            {'a': {'x': self.x + 7200, 'y': self.y + 1450}, 'b': {'x': self.x + 7300, 'y': self.y + 1500}}, 
            {'a': {'x': self.x + 7200, 'y': self.y + 1500}, 'b': {'x': self.x + 7300, 'y': self.y + 1400}},
            # BCCA: incubator top room middle top wall
            {'a': {'x': self.x + 7250, 'y': self.y + 1350}, 'b': {'x': self.x + 7450, 'y': self.y + 1400}}, 
            {'a': {'x': self.x + 7300, 'y': self.y + 1400}, 'b': {'x': self.x + 7450, 'y': self.y + 1350}}, 
            # BCCA: incubator top room bottom right wall
            {'a': {'x': self.x + 7550, 'y': self.y + 1350}, 'b': {'x': self.x + 7650, 'y': self.y + 1400}}, 
            {'a': {'x': self.x + 7550, 'y': self.y + 1400}, 'b': {'x': self.x + 7600, 'y': self.y + 1350}}, 
            # BCCA: incubator top room right wall
            {'a': {'x': self.x + 7600, 'y': self.y + 1350}, 'b': {'x': self.x + 7650, 'y': self.y + 1100}}, 
            # BCCA: incubator bottom room top left wall
            {'a': {'x': self.x + 7000, 'y': self.y + 1700}, 'b': {'x': self.x + 7100, 'y': self.y + 1750}}, 
            {'a': {'x': self.x + 7000, 'y': self.y + 1750}, 'b': {'x': self.x + 7100, 'y': self.y + 1700}}, 
            # BCCA: incubator bottom room top right wall
            {'a': {'x': self.x + 7200, 'y': self.y + 1700}, 'b': {'x': self.x + 7300, 'y': self.y + 1800}}, 
            {'a': {'x': self.x + 7200, 'y': self.y + 1750}, 'b': {'x': self.x + 7300, 'y': self.y + 1700}}, 
            # BCCA: incubator bottom room top right wall
            {'a': {'x': self.x + 7300, 'y': self.y + 1800}, 'b': {'x': self.x + 7850, 'y': self.y + 1850}}, 
            {'a': {'x': self.x + 7250, 'y': self.y + 1850}, 'b': {'x': self.x + 7850, 'y': self.y + 1800}}, 
        )
        return [segment for segment in segments if self.viewport.collidepoint(tuple(segment['a'].values())) or self.viewport.collidepoint(tuple(segment['b'].values()))]

    @property
    def get_task_rects(self):
        return [
            (pygame.Rect(self.x + 2450, self.y + 450, 500, 500), "Check Inbox"), # Check Inbox

            (pygame.Rect(self.x + 3600, self.y + 1650, 50, 50), "Refil Hand-Sanitizer"), # Refil Hand-Sanitizer: left
            (pygame.Rect(self.x + 3800, self.y + 1650, 50, 50), "Refil Hand-Sanitizer"), # Refil Hand-Sanitizer: right

            (pygame.Rect(self.x + 7000, self.y + 1050, 50, 50), "Check Temperature"), # Check Temperature

            (pygame.Rect(self.x + 6150, self.y + 100, 100, 50), "Reset Wifi"), # Reset Wifi

            (pygame.Rect(self.x + 2100, self.y + 650, 50, 100), "Plug-In Laptops"), # Plug-In Laptops: top
            (pygame.Rect(self.x + 2100, self.y + 1700, 50, 100), "Plug-In Laptops"), # Plug-In Laptops: bottom

            (pygame.Rect(self.x + 4300, self.y + 1050, 300, 300), "Wipe down Tables"), # Wipe down tables: top left
            (pygame.Rect(self.x + 4300, self.y + 1700, 300, 300), "Wipe down Tables"), # Wipe down tables: bottom left
            (pygame.Rect(self.x + 6500, self.y + 1050, 300, 300), "Wipe down Tables"), # Wipe down tables: top right
            (pygame.Rect(self.x + 6500, self.y + 1750, 300, 300), "Wipe down Tables"), # Wipe down tables: bottom right
            
            (pygame.Rect(self.x + 400, self.y + 1100, 400, 50), "Clean Windows"), # Clean Windows: left top left
            (pygame.Rect(self.x + 900, self.y + 1100, 400, 50), "Clean Windows"), # Clean Windows: left top right
            (pygame.Rect(self.x + 400, self.y + 1300, 400, 50), "Clean Windows"), # Clean Windows: left bottom left
            (pygame.Rect(self.x + 900, self.y + 1300, 400, 50), "Clean Windows"), # Clean Windows: left bottom right
            (pygame.Rect(self.x + 2350, self.y + 1100, 300, 50), "Clean Windows"), # Clean Windows: right top left
            (pygame.Rect(self.x + 2750, self.y + 1100, 300, 50), "Clean Windows"), # Clean Windows: right top right
            (pygame.Rect(self.x + 2350, self.y + 1300, 300, 50), "Clean Windows"), # Clean Windows: right bottom left
            (pygame.Rect(self.x + 2750, self.y + 1300, 300, 50), "Clean Windows"), # Clean Windows: right bottom right

            (pygame.Rect(self.x + 6700, self.y + 850, 150, 50), "Nominate For Awards"), # Nominate for Awards

            (pygame.Rect(self.x + 2300, self.y + 1000, 50, 50), "Collect Trash"), # Collect Trash: classroom1
            (pygame.Rect(self.x + 2300, self.y + 1400, 50, 50), "Collect Trash"), # Collect Trash: classroom2
            (pygame.Rect(self.x + 3700, self.y + 1550, 50, 50), "Collect Trash"), # Collect Trash: bathroom
            (pygame.Rect(self.x + 4350, self.y + 750, 50, 50), "Collect Trash"), # Collect Trash: breakroom
            (pygame.Rect(self.x + 4150, self.y + 2000, 50, 50), "Collect Trash"), # Collect Trash: left lobby
            (pygame.Rect(self.x + 6900, self.y + 2000, 50, 50), "Collect Trash"), # Collect Trash: right lobby
            (pygame.Rect(self.x + 7100, self.y + 850, 50, 50), "Collect Trash"), # Collect Trash: outside kitchen
            (pygame.Rect(self.x + 6650, self.y + 750, 50, 50), "Collect Trash"), # Collect Trash: outside kitchen

            (pygame.Rect(self.x + 2450, self.y + 1500, 500, 500), "Do Flashcards"), # Do Flashcards

            # Sabotages

            (pygame.Rect(self.x + 600, self.y + 1700, 50, 100), "Left A/C top"), # Left A/C: top
            (pygame.Rect(self.x + 900, self.y + 1850, 100, 50), "Left A/C bottom"), # Left A/C: bottom
            (pygame.Rect(self.x + 600, self.y + 1700, 50, 100), "Right A/C top"), # Right A/C: top
            (pygame.Rect(self.x + 600, self.y + 1700, 50, 100), "Right A/C bottom"), # Right A/C: bottom

            (pygame.Rect(self.x + 3400, self.y + 700, 150, 50), "Lights"), # Lights

            (pygame.Rect(self.x + 5000, self.y + 150, 50, 100), "Relaunch Zoom"), # Relaunch Zoom

            (pygame.Rect(self.x + 7050, self.y + 450, 50, 100), "Remove Spoiled Food"), # Remove Spoiled Food
            (pygame.Rect(self.x + 6400, self.y + 450, 50, 100), "Remove Spoiled Food"), # Remove Spoiled Food
        ]

    @property
    def get_vent_rects(self):
        return [
            (pygame.Rect(self.x + 170, self.y + 1200, 60, 50), "Left.1"), # Left system: 1
            (pygame.Rect(self.x + 1795, self.y + 875, 60, 50), "Left.2"), # Left system: 2
            (pygame.Rect(self.x + 3095, self.y + 1750, 60, 50), "Left.3"), # Left system: 3
            (pygame.Rect(self.x + 3995, self.y + 425, 60, 50), "Left.4"), # Left system: 4

            (pygame.Rect(self.x + 5520, self.y + 1950, 60, 50), "Right.1"), # Right system: 1
            (pygame.Rect(self.x + 6220, self.y + 450, 60, 50), "Right.2"), # Right system: 2
            (pygame.Rect(self.x + 7195, self.y + 525, 60, 50), "Right.3"), # Right system: 3
            (pygame.Rect(self.x + 7745, self.y + 1725, 60, 50), "Right.4"), # Right system: 4
        ]

    def draw_map_image(self, visible_surface, shadow_surface, do_ray_casting):
        if do_ray_casting:
            uniquePoints = set()
            for segment in self.get_wall_segments:
                if tuple(segment["a"].items()) not in uniquePoints:
                    uniquePoints.add(tuple(segment["a"].items()))
                if tuple(segment["b"].items()) not in uniquePoints:
                    uniquePoints.add(tuple(segment["b"].items()))
            
            # Find intersection of RAY & SEGMENT
            def getIntersection(ray, segment):
                # RAY in parametric: Point + Delta*T1
                r_px = ray['a']['x']
                r_py = ray['a']['y']
                r_dx = ray['b']['x'] - ray['a']['x']
                r_dy = ray['b']['y'] - ray['a']['y']

                # SEGMENT in parametric: Point + Delta*T2
                s_px = segment['a']['x']
                s_py = segment['a']['y']
                s_dx = segment['b']['x'] - segment['a']['x']
                s_dy = segment['b']['y'] - segment['a']['y']

                # Are they parallel? If so, no intersect
                if r_dx * s_dy == r_dy * s_dx:
                    # Unit vectors are the same.
                    return None

                # SOLVE FOR T1 & T2
                T2 = (r_dx * (s_py - r_py) + r_dy * (r_px - s_px)) / (s_dx * r_dy - s_dy * r_dx)
                if r_dy == 0:
                    T1 = (s_px + s_dx * T2 - r_px) / r_dx
                else:
                    T1 = (s_py + s_dy * T2 - r_py) / r_dy

                # Must be within parametic whatevers for RAY/SEGMENT
                if T1 < 0: return None
                if T2 < 0 or T2 > 1: return None

                # Return the POINT OF INTERSECTION
                return {
                    'x': r_px + r_dx * T1,
                    'y': r_py + r_dy * T1,
                    'param': T1
                }

            #######################################################

            # DRAWING
            def draw(segments):
                # Get all angles
                uniqueAngles = set()
                for uniquePoint in uniquePoints:
                    points_dict = dict(uniquePoint)
                    angle = math.atan2(points_dict['y'] - 540, points_dict['x'] - 960)
                    uniqueAngles.update([angle-0.00001, angle+0.00001])

                uniqueAngles = sorted(uniqueAngles)

                # RAYS IN ALL DIRECTIONS
                points = []
                for angle in uniqueAngles:

                    # Calculate dx & dy from angle
                    dx = math.cos(angle)
                    dy = math.sin(angle)

                    # Ray from center of screen to player
                    ray = {
                        "a":{"x": 960, "y": 540},
                        "b":{"x": 960 + dx, "y": 540 + dy}
                    }

                    # Find CLOSEST intersection
                    closestIntersect = None
                    for segment in segments:
                        intersect = getIntersection(ray,segment)
                        if not intersect: continue
                        elif not closestIntersect or intersect["param"] < closestIntersect["param"]:
                            closestIntersect = intersect

                    # Intersect angle
                    if not closestIntersect: continue
                    # Add to list of intersects
                    else:
                        points.append((closestIntersect['x'], closestIntersect['y']))

                # DRAW ALL RAYS
                # # print("\n", points, "\n")
                shadow_surface.blit(self.shadow_map_image, (self.x, self.y))
                pygame.draw.polygon(shadow_surface, "#123456", points)
            
            visible_surface.fill((40,40,40))
            visible_surface.blit(self.visible_map_image, (self.x, self.y))
            draw(self.get_wall_segments)
            self.draw_vents(visible_surface)
            self.draw_tasks(visible_surface)
            visible_surface.blit(shadow_surface, (0, 0))
        else:
            visible_surface.fill((40,40,40))
            visible_surface.blit(self.visible_map_image, (self.x, self.y))
    
    def draw_collision(self, surface):
        # Draw Rects
        # for wall in self.get_wall_rects:
        #     pygame.draw.rect(surface, (0,255,0), wall, 1)

        # Draw segments
            color = "#ff0000"
            for seg in self.get_wall_segments:
            	pygame.draw.line(surface, color, (seg["a"]["x"], seg["a"]["y"]), (seg["b"]["x"], seg["b"]["y"]), 3)

    def draw_tasks(self, surface):
        for task in self.get_task_rects:
            pygame.draw.rect(surface, (242,242,0), task[0], 3)
    
    def draw_vents(self, surface):
        for vent in self.get_vent_rects:
            pygame.draw.rect(surface, (0,242,242), vent[0], 3)

    def draw_coords(self, surface, font):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pos_text = font.render(f"X: {round(self.x, 2)}Y: {round(self.y, 3)} ~ X: {round(mouse_x - self.x, 2)}Y: {round(mouse_y - self.y, 3)}", True, (255,0,0))
        pos_textRect = pos_text.get_rect()
        pos_textRect.center = (250, 50)
        surface.blit(pos_text, pos_textRect)

if __name__ == "__main__":
    import main