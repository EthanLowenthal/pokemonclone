import sys
if sys.maxsize.bit_length() == 63: print('ONLY RUNS IN 32 BIT PYTHON: SHUTTING DOWN') & quit()
import pygame, time, random, json, requests
try:pass
except:print('A REQIERED PACKAGE IS NOT INSTALLED: SHUTTING DOWN') & quit()
try: import maps, pokemon
except: print('YOU MAY HAVE DELETED IMPORTANT FILES: SHUTTING DOWN') & quit()
from maps import *
from pokemon import *
from pygame.locals import*

optimize = True
pygame.init()

# map = tutorial
map = mid

textlog = []


def button(msg,x,y,w,h,ic,ac,display,sufcoordsx,sufcoordsy, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w+sufcoordsx > mouse[0] > x+sufcoordsx and y+h+sufcoordsy > mouse[1] > y+sufcoordsy:
        pygame.draw.rect(display, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            global intro
            intro = False
            action()
    else:
        pygame.draw.rect(display, ic,(x,y,w,h))
    smallText = pygame.font.SysFont(None, 40)
    textSurf = smallText.render(msg, True, colors['BLACK'])
    textRect = textSurf.get_rect()
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    display.blit(textSurf, textRect)



def displayText(font=None, size=30):

    myfont = pygame.font.SysFont(None, size)
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

    myfont = pygame.font.SysFont(None, 40)
    label = myfont.render('FPS: ' + str(clock.get_fps())[:4], 1, (255, 255, 255), (0, 0, 0))
    label.set_alpha(150)
    display.blit(label, (600, 10))

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

def draw_map(cam_pos):
    for pos2, line in enumerate(map):
        for pos1, wall in enumerate(line):
            if pos1 * 50 > -cam_pos[0] - 50 and pos2 * 50 > -cam_pos[1] - 50:
                if pos1 * 50 < -cam_pos[0] + width and pos2 * 50 < -cam_pos[1] + height:
                    if wall == tiles["WATER"]:
                        if not optimize:
                            world.blit(pygame.image.load('./images/water.jpg'), (pos1 * 50, pos2 * 50))
                        else:
                            pygame.draw.rect(world, colors["BLUE"], ((pos1 * 50, pos2 * 50), (50, 50)))
                    if wall == tiles["LIGHT_GRASS"]:
                        if not optimize:
                            world.blit(pygame.image.load('./images/grass.png'), (pos1 * 50, pos2 * 50))
                        else:
                            pygame.draw.rect(world, colors["LIGHT_GREEN"], ((pos1 * 50, pos2 * 50), (50, 50)))
                    elif wall == tiles["GRASS"] and not optimize:
                        world.blit(pygame.image.load('./images/grass.png'), (pos1 * 50, pos2 * 50))
                    elif wall == tiles["BRICK"]:
                        if not optimize:
                            world.blit(pygame.image.load('./images/thatch.jpg'), (pos1 * 50, pos2 * 50))
                        else:
                            pygame.draw.rect(world, colors["DARK_RED"], ((pos1 * 50, pos2 * 50), (50, 50)))
                    elif wall == tiles["PATH"]:
                        if not optimize:
                            world.blit(pygame.image.load('./images/stone.jpg'), (pos1 * 50, pos2 * 50))
                        else:
                            pygame.draw.rect(world, colors["GREY"], ((pos1 * 50, pos2 * 50), (50, 50)))
                    elif wall == tiles["ICE"]:
                        pygame.draw.rect(world, colors["LIGHT_BLUE"], ((pos1 * 50, pos2 * 50), (50, 50)))



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

def draw_menu():
    pygame.draw.rect(pause_surf, colors['YELLOW'],(0, 0, 350, 500))
    pygame.draw.rect(pause_surf, colors['WHITE'], (10, 10, 330, 480))
    button('Resume', 100, 40, 150, 50, colors['DARK_GREEN'], colors['LIGHT_GREEN'], pause_surf, (width/2)-175, 100, Main)
    button("Quit", 100, 100, 150, 50, colors['DARK_RED'], colors['RED'], pause_surf, (width/2)-175, 100, quit)
    display.blit(pause_surf, ((width/2)-175, 100))

def pause(player):
    overlay.fill(colors['BLACK'])
    pygame.display.set_caption('Ethan\'s Pokemon Clone [PAUSED]')
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    Main()

        player.render(world)
        display.blit(world, camera_pos)
        overlay.fill(colors['BLACK'])
        draw_legend()
        overlay.set_alpha(200)
        display.blit(overlay, (0,0))
        draw_menu()
        pygame.display.flip()

def Main():
    global display, clock, world, intro, camera_pos, last_cam_pos
    pygame.display.set_caption('Ethan\'s Pokemon Clone')
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pause(player)

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

        draw_map(camera_pos)

        player.render(world)
        display.blit(world,camera_pos)

        draw_legend()
        get_pokemon()
        displayText()
        pygame.display.flip()

        last_cam_pos = camera_pos



def game_intro():
    global intro
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.fill(colors['WHITE'])
        largeText = pygame.font.SysFont(None, 115)
        TextSurf = largeText.render('Pokemon Clone', True, colors['BLACK'])
        TextRect = TextSurf.get_rect()
        TextRect.center = ((width / 2), (360))
        display.blit(TextSurf, TextRect)


        button("Start!", 150, 450, 200, 100, colors['DARK_GREEN'], colors['LIGHT_GREEN'], display,0,0, Main)
        button("Quit", 450, 450, 200, 100, colors['DARK_RED'], colors['RED'], display,0,0, quit)

        pygame.display.update()
        clock.tick(15)

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
    global display, clock, world, intro, camera_pos, last_cam_pos, width, height
    display = pygame.display.set_mode((800,800))
    width, height = pygame.display.get_surface().get_size()
    clock = pygame.time.Clock()
    world = pygame.Surface((1000, 1000))
    overlay = pygame.Surface((width, height))
    pause_surf = pygame.Surface((350, 500))
    player = Player()
    camera_pos = (192,192)
    last_cam_pos = camera_pos
    print(width, height)


    intro = True

    game_intro()