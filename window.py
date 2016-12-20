import sys
if sys.maxsize.bit_length() == 63: print('ONLY RUNS IN 32 BIT PYTHON: SHUTTING DOWN') & quit()
import pygame, time, random, json, requests
try:pass
except:print('A REQIERED PACKAGE IS NOT INSTALLED: SHUTTING DOWN') & quit()
try: import maps, pokemon
except: print('YOU MAY HAVE DELETED IMPORTANT FILES: SHUTTING DOWN') & quit()
from maps import *
from pokemon import *


pygame.init()
# map = tutorial
map = mid

textlog = []

def displayText(font=None, size=30):

    myfont = pygame.font.SysFont("comicsans", size)
    for pos, text in enumerate(reversed(textlog)):
        if pos <= 6:
            label = myfont.render('['+text[1]+']'+' - '+ text[0]+' ', 1, (255, 255, 255), (0, 0, 0))
            label.set_alpha(150)
            display.blit(label, (0, 800 - (pos * size)))
    pygame.display.flip()

class Player:
    def __init__(self):
        self.image = pygame.Surface((16,16))
        self.image.fill(colors["WHITE"])
        self.rect = pygame.Rect((50,50),(16,16))
        self.speed = 5

    def change_world(self):
        time.sleep(0.7)

        for i in range(0, 250, 2):
            overlay.fill(colors["BLACK"])
            overlay.set_alpha(i)
            display.blit(overlay,(0,0))
            pygame.display.flip()


    def move(self,camera_pos):
        global map

        pos_x,pos_y = camera_pos
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.rect.y -= self.speed
            pos_y += self.speed
        if key[pygame.K_a]:
            self.rect.x -= self.speed
            pos_x += self.speed
        if key[pygame.K_s]:
            self.rect.y += self.speed
            pos_y -= self.speed
        if key[pygame.K_d]:
            self.rect.x += self.speed
            pos_x -= self.speed


        if self.rect.x < 0:
            if map == left or map == up or map == down:
                self.rect.x = 0
            elif map == mid:
                map = left
                self.rect.x = 984
                self.change_world()
            elif map == right:
                map = mid
                self.rect.x = 984
                self.change_world()


        elif self.rect.x > 984:
            if map == right or map == up or map == down:
                self.rect.x = 984
            elif map == mid:
                map = right
                self.rect.x = 0
                self.change_world()
            elif map == left:
                map = mid
                self.rect.x = 0
                self.change_world()

        if self.rect.y < 0:
            self.rect.y = 984
            if map == up or map == left or map == right:
                self.rect.y = 0
                pos_y = camera_pos[1]
            elif map == mid:
                map = up
                self.change_world()
            elif map == down:
                map = mid
                self.change_world()

        elif self.rect.y > 984:
            self.rect.y = 0
            if map == down or map == left or map == right:
                self.rect.y = 984
            elif map == mid:
                map = down
                self.change_world()
            elif map == up:
                map = mid
                self.change_world()

        pos_x, pos_y = -self.rect.x/2 + 150, -self.rect.y/2 + 150
        return (pos_x, pos_y), (self.rect.x, self.rect.y)

    def render(self,display):
        display.blit(self.image,(self.rect.x,self.rect.y))


def draw_legend():
    pygame.draw.rect(display, colors["WHITE"], ((15, 15), (120, 120)))
    pygame.draw.rect(display, colors["LIGHT_BLUE"], ((25, 25), (100, 100)))

    # pygame.draw.rect(display, colors["DARK_RED"], ((32, 32), (25, 25)))
    # pygame.draw.rect(display, colors["DARK_RED"], ((32, 92), (25, 25)))
    # pygame.draw.rect(display, colors["DARK_RED"], ((92, 32), (25, 25)))
    # pygame.draw.rect(display, colors["DARK_RED"], ((92, 92), (25, 25)))

    pygame.draw.rect(display, colors["DARK_RED"], ((32, 62), (25, 25)))  # left
    pygame.draw.rect(display, colors["DARK_RED"], ((62, 32), (25, 25)))  # up
    pygame.draw.rect(display, colors["DARK_RED"], ((62, 62), (25, 25)))  # mid
    pygame.draw.rect(display, colors["DARK_RED"], ((62, 92), (25, 25)))  # down
    pygame.draw.rect(display, colors["DARK_RED"], ((92, 62), (25, 25)))  # right

    if map == up:
        pygame.draw.rect(display, colors["YELLOW"], ((62, 32), (25, 25)))  # up

    elif map == down:
        pygame.draw.rect(display, colors["YELLOW"], ((62, 92), (25, 25)))  # down

    elif map == left:
        pygame.draw.rect(display, colors["YELLOW"], ((32, 62), (25, 25)))  # left

    elif map == right:
        pygame.draw.rect(display, colors["YELLOW"], ((92, 62), (25, 25)))  # right

    elif map == mid:
        pygame.draw.rect(display, colors["YELLOW"], ((62, 62), (25, 25)))  # mid

def draw_map():
    for pos2, line in enumerate(map):
        for pos1, wall in enumerate(line):
            if wall == tiles["WATER"]:
                pygame.draw.rect(world, colors["BLUE"], ((pos1 * 50, pos2 * 50), (50, 50)))
            if wall == tiles["LIGHT_GRASS"]:
                pygame.draw.rect(world, colors["LIGHT_GREEN"], ((pos1 * 50, pos2 * 50), (50, 50)))
            if wall == tiles["BRICK"]:
                pygame.draw.rect(world, colors["DARK_RED"], ((pos1 * 50, pos2 * 50), (50, 50)))
            if wall == tiles["PATH"]:
                pygame.draw.rect(world, colors["GREY"], ((pos1 * 50, pos2 * 50), (50, 50)))
            if wall == tiles["ICE"]:
                pygame.draw.rect(world, colors["LIGHT_BLUE"], ((pos1 * 50, pos2 * 50), (50, 50)))


def fight():
    pass

def get_pokemon():
    chance = random.randint(1, 1000)
    global pokemon, textlog, last_cam_pos
    if chance >= 998 and camera_pos != last_cam_pos:
        if current_tile == tiles["GRASS"]:
            pokemon = random.choice(grass_pokemon)
        if current_tile == tiles["WATER"]:
            pokemon = random.choice(water_pokemon)
        else:
            last_cam_pos = camera_pos
            return
        resp = requests.get(pokemon)
        textlog.append(('You encounterd a  ' + json.loads(resp.text)['name'], time.strftime("%I:%M:%S")))
        last_cam_pos = camera_pos


def Main(display,clock, world):
    for x in range(10):
        pygame.draw.rect(world,colors["BLUE"],((x * 100,x * 100),(20,20)))

    player = Player()
    global camera_pos
    camera_pos = (192,192)
    global last_cam_pos
    last_cam_pos = camera_pos

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        camera_pos, player_pos = player.move(camera_pos)

        display.fill(colors["WORLD"])
        world.fill(colors["DARK_GREEN"])

        global current_tile
        current_tile = map[int(player_pos[1]/50)][int(player_pos[0]/50)]
        if current_tile == tiles["PATH"]:
            player.speed = 5
        elif current_tile == tiles["WATER"]:
            player.speed = 1
        else:
            player.speed = 3

        draw_map()

        player.render(world)
        display.blit(world,camera_pos)

        draw_legend()
        get_pokemon()
        displayText()

        pygame.display.flip()


if __name__ in "__main__":
    global colors, tiles
    colors = {
        "WHITE": (255, 255, 255),
        "RED": (255, 0, 0),
        "DARK_RED": (102, 0, 0),
        "DARK_GREEN": (0, 102, 0),
        "LIGHT_GREEN": (0, 170, 0),
        "BLUE": (0, 0, 255),
        "LIGHT_BLUE": (153, 255, 255),
        "BLACK": (0, 0, 0),
        "GREY": (64, 64, 64),
        "WORLD": (25, 0, 51),
        "YELLOW": (255, 255, 51),
        "PINK": (153, 0, 153)

    }

    tiles = {
        "GRASS":0,
        "WATER":1,
        "LIGHT_GRASS":2,
        "BRICK":3,
        "PATH":4,
        "ICE":5,
    }
    display = pygame.display.set_mode((800,800))
    clock = pygame.time.Clock()
    world = pygame.Surface((1000, 1000))
    overlay = pygame.Surface((800, 800))


    Main(display,clock,world)