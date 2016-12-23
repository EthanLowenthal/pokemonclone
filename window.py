import sys
if sys.maxsize.bit_length() == 63: print('ONLY RUNS IN 32 BIT PYTHON: SHUTTING DOWN') & quit()
import pygame, time, random, json, requests, urllib, cStringIO
try:pass
except:print('A REQIERED PACKAGE IS NOT INSTALLED: SHUTTING DOWN') & quit()
try: import maps, pokemon
except: print('YOU MAY HAVE DELETED IMPORTANT FILES: SHUTTING DOWN') & quit()
from maps import *
from pokemon import *
from pygame.locals import *
from gui import *
from poster.streaminghttp import register_openers
from type_advantages import *

register_openers()

optimize = True
ingame = False
pygame.init()

# map = tutorial
map = mid

textlog = []

colors = {
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "DARK_RED": (102, 0, 0),
    "DARK_GREEN": (0, 102, 0),
    "LIGHT_GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "LIGHT_BLUE": (153, 255, 255),
    "BLACK": (0, 0, 0),
    "GREY": (64, 64, 64),
    "WORLD": (25, 0, 51),
    "YELLOW": (255, 255, 51),
    "PINK": (153, 0, 153),
    "DARK_GREY": (96, 96, 96),
    "ORANGE": (204,102,0),
    "LIGHT_ORANGE": (255,178,102)

}


def displayText(font=None, size=30):

    myfont = pygame.font.SysFont(None, size)
    for pos, text in enumerate(reversed(textlog)):
        if pos <= 6:
            label = myfont.render('['+text[1]+']'+' - '+ text[0]+' ', 1, (255, 255, 255), (0, 0, 0))
            label.set_alpha(150)
            display.blit(label, (0, 800 - (pos * size)))

class Player:
    def __init__(self):
        self.image = pygame.Surface((16,16))
        self.image.fill(colors["WHITE"])
        self.rect = pygame.Rect((50,50),(16,16))
        self.speed = 5
        self.pokemon = []

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

def draw_attacker():
    resp_url = 'http://pokeapi.co/api/v2/pokemon/' + str(player.pokemon[0])
    resp = requests.get(resp_url)
    img_url = json.loads(resp.text)['sprites']['back_default']
    urlopen = urllib.urlopen(img_url).read()
    img = cStringIO.StringIO(urlopen)
    load_img = pygame.image.load(img)
    t_img = pygame.transform.scale(load_img, (300, 300))
    return t_img

def draw_defender(pokemon):
    resp_url = 'http://pokeapi.co/api/v2/pokemon/' + str(pokemon)
    resp = requests.get(resp_url)
    img_url = json.loads(resp.text)['sprites']['front_default']
    urlopen = urllib.urlopen(img_url).read()
    img = cStringIO.StringIO(urlopen)
    load_img = pygame.image.load(img)
    t_img = pygame.transform.scale(load_img, (250, 250))
    return t_img

def displaybattletext(text):
    myfont = pygame.font.SysFont(None, 30)
    label = myfont.render(text, 1, (0, 0, 0))
    return label

def use_move(x):
    global move_used
    move_used = True
    move = x[0]
    player_data = x[1]
    com_data = x[2]
    resp = requests.get(move['move']['url'])
    data = json.loads(resp.text)
    # if random.randint(0, 100) <= data['accuracy']:
    A = 1
    B = player_data['stats'][4]['base_stat']
    C = data['power']
    D = com_data['stats'][3]['base_stat']
    X = 1
    Y = type_adv[player_data['types'][0]['type']['name']][com_data['types'][0]['type']['name']]
    Z = random.randint(217,256)
    if C is None:
        C = 40
    global dmg, label
    label = displaybattletext(player_data['name']+ ' used '+move['move']['name']+'!')
    dmg = ((((2*A+10)/250) * B/D * C + 2) * 1 * Y * Z)/255


def draw_battle(battle_surf, d, a, moves, player_data, com_data):
    battle_surf.fill(colors['WORLD'])
    pygame.draw.rect(battle_surf, colors['YELLOW'], (10, 10, 380, 480))
    pygame.draw.rect(battle_surf, colors['WHITE'], (20, 20, 360, 210))
    pygame.draw.rect(battle_surf, colors['WHITE'], (20, 240, 360, 60))
    pygame.draw.rect(battle_surf, colors['WHITE'], (20, 310, 360, 170))
    battle_surf.blit(d, (180, -50))
    battle_surf.blit(a, (-10, 10))
    try:
        fake_button(moves[0]['move']['name'], 30, 320, 165, 70, colors['ORANGE'], colors['LIGHT_ORANGE'], battle_surf, 200,
               150, size=35, action=use_move, args=[moves[0], player_data, com_data])
    except:
        fake_button('No Move', 30, 320, 165, 70, colors['GREY'], colors['DARK_GREY'], battle_surf, 200, 150, size=35)
    try:
        fake_button(moves[1]['move']['name'], 30, 395, 165, 70, colors['ORANGE'], colors['LIGHT_ORANGE'], battle_surf, 200,
               150, size=35, action=use_move, args=[moves[1], player_data, com_data])
    except:
        fake_button('No Move', 30, 320, 165, 70, colors['GREY'], colors['DARK_GREY'], battle_surf, 200, 150, size=35)
    try:
        fake_button(moves[2]['move']['name'], 200, 320, 165, 70, colors['ORANGE'], colors['LIGHT_ORANGE'], battle_surf, 200,
               150, size=35, action=use_move, args=[moves[2], player_data, com_data])
    except:
        fake_button('No Move', 30, 320, 165, 70, colors['GREY'], colors['DARK_GREY'], battle_surf, 200, 150, size=35)
    try:
        fake_button(moves[3]['move']['name'], 200, 395, 165, 70, colors['ORANGE'], colors['LIGHT_ORANGE'], battle_surf, 200,
               150, size=35, action=use_move, args=[moves[3], player_data, com_data])
    except:
        fake_button('No Move', 30, 320, 165, 70, colors['GREY'], colors['DARK_GREY'], battle_surf, 200, 150, size=35)

def won(person):
    pass

def battle(pokemon):
    global move_used, label, paused, dmg
    move_used = False
    battle_surf = pygame.Surface((400, 500))
    a = draw_attacker()
    d = draw_defender(pokemon)
    moves = json.loads(requests.get('http://pokeapi.co/api/v2/pokemon/'+ str(player.pokemon[0])).text)['moves']
    player_data = json.loads(requests.get('http://pokeapi.co/api/v2/pokemon/'+str(player.pokemon[0])).text)
    com_data = json.loads(requests.get('http://pokeapi.co/api/v2/pokemon/'+ str(pokemon)).text)
    label = displaybattletext('You encountered a ' + com_data['name'])
    player_hp = player_data['stats'][5]['base_stat']
    com_hp = com_data['stats'][5]['base_stat']
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    paused = True
                    pause(player)
        draw_battle(battle_surf, d, a, moves, player_data, com_data)
        try:
            button(moves[0]['move']['name'], 30, 320, 165, 70, colors['ORANGE'], colors['LIGHT_ORANGE'], battle_surf,
                   200,
                   150, size=35, action=use_move, args=[moves[0], player_data, com_data])
        except:
            button('No Move', 30, 320, 165, 70, colors['GREY'], colors['DARK_GREY'], battle_surf, 200, 150, size=35)
        try:
            button(moves[1]['move']['name'], 30, 395, 165, 70, colors['ORANGE'], colors['LIGHT_ORANGE'], battle_surf,
                   200,
                   150, size=35, action=use_move, args=[moves[1], player_data, com_data])
        except:
            button('No Move', 30, 320, 165, 70, colors['GREY'], colors['DARK_GREY'], battle_surf, 200, 150, size=35)
        try:
            button(moves[2]['move']['name'], 200, 320, 165, 70, colors['ORANGE'], colors['LIGHT_ORANGE'], battle_surf,
                   200,
                   150, size=35, action=use_move, args=[moves[2], player_data, com_data])
        except:
            button('No Move', 30, 320, 165, 70, colors['GREY'], colors['DARK_GREY'], battle_surf, 200, 150, size=35)
        try:
            button(moves[3]['move']['name'], 200, 395, 165, 70, colors['ORANGE'], colors['LIGHT_ORANGE'], battle_surf,
                   200,
                   150, size=35, action=use_move, args=[moves[3], player_data, com_data])
        except:
            button('No Move', 30, 320, 165, 70, colors['GREY'], colors['DARK_GREY'], battle_surf, 200, 150, size=35)
        battle_surf.blit(label, (40, 255))
        display.blit(battle_surf, (200, 150))
        pygame.display.flip()
        if move_used:
            time.sleep(2)
            draw_battle(battle_surf, d, a, moves, player_data, com_data)
            battle_surf.blit(label, (40, 255))
            display.blit(battle_surf, (200, 150))
            pygame.display.flip()
            time.sleep(2)

            com_hp -= dmg
            if com_hp <= 0:
                won(player)
            draw_battle(battle_surf, d, a, moves, player_data, com_data)
            label = displaybattletext('It dealt ' + str(int(dmg)) + ' damage!')
            battle_surf.blit(label, (40, 255))
            display.blit(battle_surf, (200, 150))
            pygame.display.flip()
            time.sleep(2)

            if type_adv[player_data['types'][0]['type']['name']][com_data['types'][0]['type']['name']] == 2.5:
                label = displaybattletext('Its not very effective...')
            if type_adv[player_data['types'][0]['type']['name']][com_data['types'][0]['type']['name']] == 20:
                label = displaybattletext('Its super effective')
            draw_battle(battle_surf, d, a, moves, player_data, com_data)
            battle_surf.blit(label, (40, 255))
            display.blit(battle_surf, (200, 150))
            pygame.display.flip()
            time.sleep(2)

            move = json.loads(requests.get('http://pokeapi.co/api/v2/pokemon/'+ str(pokemon)).text)
            move = move['moves'][random.randint(0,len(move))]
            use_move([move,com_data,com_data,player_data])
            draw_battle(battle_surf, d, a, moves, player_data, com_data)
            battle_surf.blit(label, (40, 255))
            display.blit(battle_surf, (200, 150))
            pygame.display.flip()
            time.sleep(2)

            player_hp -= dmg
            if player_hp <= 0:
                won(com_data)
            draw_battle(battle_surf, d, a, moves, player_data, com_data)
            label = displaybattletext('It dealt ' + str(int(dmg)) + ' damage!')
            battle_surf.blit(label, (40, 255))
            display.blit(battle_surf, (200, 150))
            pygame.display.flip()
            time.sleep(2)

            if type_adv[com_data['types'][0]['type']['name']][player_data['types'][0]['type']['name']] == 2.5:
                label = displaybattletext('Its not very effective...')
            if type_adv[com_data['types'][0]['type']['name']][player_data['types'][0]['type']['name']] == 20:
                label = displaybattletext('Its super effective')
            draw_battle(battle_surf, d, a, moves, player_data, com_data)
            battle_surf.blit(label, (40, 255))
            display.blit(battle_surf, (200, 150))
            pygame.display.flip()
            time.sleep(2)
            move_used = False


def get_pokemon():
    chance = random.randint(1, 1000)
    global pokemon, textlog, last_cam_pos
    if chance >= 1 and camera_pos != last_cam_pos:
        if current_tile == tiles["GRASS"] or current_tile == tiles["LIGHT_GRASS"]:
            pokemon = random.choice(grass_pokemon)
        if current_tile == tiles["WATER"]:
            pokemon = random.choice(water_pokemon)
        else:
            last_cam_pos = camera_pos
            return
        resp = requests.get(pokemon)
        textlog.append(('You encounterd a  ' + json.loads(resp.text)['name'], time.strftime("%I:%M:%S")))
        displayText()
        pygame.display.flip()
        battle(json.loads(resp.text)['id'])

def resume_game():
    global paused
    pause_surf.set_alpha(0)
    paused = False

def pause_menu():
    pause_surf.set_alpha(255)
    pygame.draw.rect(pause_surf, colors['YELLOW'],(0, 0, 350, 500))
    pygame.draw.rect(pause_surf, colors['WHITE'], (10, 10, 330, 480))
    myfont = pygame.font.SysFont(None, 60)
    label = myfont.render('Paused', 1, (0, 0, 0))
    pause_surf.blit(label, (100, 30))
    button('Resume', 100, 100, 150, 50, colors['DARK_GREEN'], colors['LIGHT_GREEN'], pause_surf, (width/2)-175, 100, resume_game)
    button("Quit", 100, 160, 150, 50, colors['DARK_RED'], colors['RED'], pause_surf, (width/2)-175, 100, quit)
    button("Home", 100, 220, 150, 50, colors['DARK_GREEN'], colors['LIGHT_GREEN'], pause_surf, (width / 2) - 175, 100, game_intro)
    button("Settings", 100, 280, 150, 50, colors['DARK_GREEN'], colors['LIGHT_GREEN'], pause_surf, (width / 2) - 175, 100, settings)
    display.blit(pause_surf, ((width/2)-175, 100))

def settings_menu(check):
    pygame.draw.rect(pause_surf, colors['YELLOW'], (0, 0, 350, 500))
    pygame.draw.rect(pause_surf, colors['WHITE'], (10, 10, 330, 480))
    myfont = pygame.font.SysFont(None, 60)
    label = myfont.render('Settings', 1, (0, 0, 0))
    pause_surf.blit(label, (85, 30))
    check.render_checkbox()
    if ingame:
        button("Save", 240, 440, 100, 50, colors['DARK_GREEN'], colors['LIGHT_GREEN'], pause_surf, (width / 2) - 175, 100, pause, args=player)
    else:
        button("Save", 240, 440, 100, 50, colors['DARK_GREEN'], colors['LIGHT_GREEN'], pause_surf, (width / 2) - 175, 100, game_intro)
    display.blit(pause_surf, ((width / 2) - 175, 100))


def pause(player):
    paused = True
    overlay.fill(colors['BLACK'])
    pygame.display.set_caption('Ethan\'s Pokemon Clone [PAUSED]')
    while paused:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    resume_game()
        player.render(world)
        display.blit(world, camera_pos)
        overlay.fill(colors['BLACK'])
        draw_legend()
        overlay.set_alpha(200)
        display.blit(overlay, (0,0))
        pause_menu()
        pygame.display.flip()

def Main():
    global display, clock, world, intro, camera_pos, last_cam_pos
    pygame.display.set_caption('Ethan\'s Pokemon Clone')
    # if not ingame:
    #     game_intro()
    while ingame:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    global paused
                    paused = True
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
        button("", width - 65, height - 65, 50, 50, colors['WHITE'], colors['WHITE'], display, 0, 0, settings)
        display.blit(pygame.image.load('./images/settings.png'), (width - 65, height - 65))
        pygame.display.flip()

        last_cam_pos = camera_pos


def settings():
    overlay.fill(colors['BLACK'])
    pygame.display.set_caption('Ethan\'s Pokemon Clone [PAUSED]')
    check = Checkbox(pause_surf, 30, 100, color=colors['WHITE'], caption="Faster Graphics", outline_color=colors['BLACK'],
                     text_offset=(100, 1), surf_offset=((width / 2) - 175, 100), font_size=30)
    if optimize:
        check.click = True
        check.active = True
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            check.update_checkbox(event)
        if ingame:
            player.render(world)
            display.blit(world, camera_pos)
            overlay.fill(colors['BLACK'])
            draw_legend()
        else:
            draw_intro()
        overlay.set_alpha(200)
        display.blit(overlay, (0, 0))
        settings_menu(check)
        pygame.display.flip()
        global optimize
        if check.is_checked():
            optimize = True
        else:
            optimize = False


def starterpokemon():
    global x
    x = True
    display.fill(colors['WHITE'])
    pygame.draw.rect(display, colors['YELLOW'], (0, 0, width, height))
    pygame.draw.rect(display, colors['WHITE'], (10, 10, width - 20, height - 20))
    myfont = pygame.font.SysFont(None, 90)
    label = myfont.render('Choose your starter', 1, (0, 0, 0))
    label1 = myfont.render('pokemon!', 1, (0, 0, 0))
    def b():
        player.pokemon.append(1)
        global x
        x = False
    def c():
        player.pokemon.append(4)
        global x
        x = False
    def s():
        player.pokemon.append(7)
        global x
        x = False

    b_img = pygame.image.load(cStringIO.StringIO(urllib.urlopen(json.loads(requests.get('http://pokeapi.co/api/v2/pokemon/1').text)['sprites']['front_default']).read()))
    c_img = pygame.image.load(cStringIO.StringIO(urllib.urlopen(json.loads(requests.get('http://pokeapi.co/api/v2/pokemon/4').text)['sprites']['front_default']).read()))
    s_img = pygame.image.load(cStringIO.StringIO(urllib.urlopen(json.loads(requests.get('http://pokeapi.co/api/v2/pokemon/7').text)['sprites']['front_default']).read()))
    while x:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        display.blit(label, (100, 75))
        display.blit(label1, (270, 150))
        button("", 266, 290, 266, 300, colors['WHITE'], colors['WHITE'], display, 0, 0, s)
        button("", 10, 290, 256, 300, colors['WHITE'], colors['WHITE'], display, 0, 0, b)
        button("", 532, 290, 256, 300, colors['WHITE'], colors['WHITE'], display, 0, 0, c)
        display.blit(pygame.transform.scale(s_img, (500, 500)), (150, 200))
        display.blit(pygame.transform.scale(b_img, (500, 500)), (-100, 200))
        display.blit(pygame.transform.scale(c_img, (500, 500)), (400, 200))
        pygame.display.flip()


def StartGame():
    global ingame
    ingame = True
    if player.pokemon == []:
        starterpokemon()
    Main()


def draw_intro():
        display.fill((51,0,25))
        largeText = pygame.font.SysFont(None, 115)
        smallText = pygame.font.SysFont(None, 75)
        title = largeText.render('`', True, colors['BLACK'])
        display.blit(title, (250,217))
        title = largeText.render('Pokemon Clone', True, colors['BLACK'])
        titlerect = title.get_rect()
        titlerect.center = ((width / 2), (260))
        display.blit(title, titlerect)
        credits = smallText.render('By Ethan', True, colors['BLACK'])
        creditsrect = credits.get_rect()
        creditsrect.center = ((width / 2), (360))
        display.blit(credits, creditsrect)
        global ingame
        button("Start!", 150, 450, 200, 100, colors['LIGHT_GREEN'], colors['DARK_GREEN'], display,0,0, StartGame)
        button("Quit", 450, 450, 200, 100, colors['RED'], colors['DARK_RED'], display,0,0, quit)
        button("", width - 65, height - 65, 50, 50, colors['WHITE'], colors['WHITE'], display, 0, 0, settings)

        display.blit(pygame.image.load('./images/settings.png'), (width - 65, height - 65))


def game_intro():
    pygame.display.set_caption('Ethan\'s Pokemon Clone')
    global intro, ingame
    ingame = False
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        draw_intro()
        pygame.display.flip()


if __name__ in "__main__":
    global colors, tiles
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