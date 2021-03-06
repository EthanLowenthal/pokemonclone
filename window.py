import sys
if sys.maxsize.bit_length() == 63: print('ONLY RUNS IN 32 BIT PYTHON: SHUTTING DOWN') & quit()
import pygame, time, random, json, requests, urllib, cStringIO, math
try:pass
except:print('A REQIERED PACKAGE IS NOT INSTALLED: SHUTTING DOWN') & quit()
try: import maps, pokemon
except: print('YOU MAY HAVE DELETED IMPORTANT FILES: SHUTTING DOWN') & quit()
from maps import *
from pokemon import *
from pygame.locals import *
from gui import *
from poster.streaminghttp import register_openers
from pokemon_data import *

register_openers()

global current_pokemon
optimize = True
ingame = False
current_pokemon = 0
pygame.init()

# map = tutorial
map = mid

textlog = []

colors = {
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "DARK_RED": (102, 0, 0),
    "DARK_GREEN": (0, 102, 0),
    "GREEN": (0, 120, 0),
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

items = {
    'potion':20,
    'max-potion':1000,
    'super-potion':50
}


inventory = {
    'poke-ball':10,
    'potion':5,
    'max-potion':1,
    'super-potion':0
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
    global current_pokemon
    resp_url = 'http://pokeapi.co/api/v2/pokemon/' + str(player.pokemon[current_pokemon][0])
    resp = requests.get(resp_url)
    img_url = json.loads(resp.text)['sprites']['back_default']
    urlopen = urllib.urlopen(img_url).read()
    img = cStringIO.StringIO(urlopen)
    load_img = pygame.image.load(img)
    t_img = pygame.transform.scale(load_img, (250, 250))
    return t_img

def draw_defender(pokemon):
    resp_url = 'http://pokeapi.co/api/v2/pokemon/' + str(pokemon)
    resp = requests.get(resp_url)
    img_url = json.loads(resp.text).get('sprites')
    urlopen = urllib.urlopen(img_url['front_default']).read()
    img = cStringIO.StringIO(urlopen)
    load_img = pygame.image.load(img)
    t_img = pygame.transform.scale(load_img, (200, 200))
    return t_img

def displaybattletext(text):
    myfont = pygame.font.SysFont(None, 30)
    label = myfont.render(text, 1, (0, 0, 0))
    return label

def use_move(x):
    global move_used, escape_times
    escape_times = 0
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


def use_pokeball():
    global d, pokemon, com_data
    inventory['poke-ball'] -= 1
    total_hp = com_data['stats'][5]['base_stat']
    bonusstatus = 0
    rate = random.randint(100,255)
    catch_rate = max((3 * total_hp - 2 * com_hp) * rate / (3 * total_hp), 1) + bonusstatus
    if random.randint(0,100) > catch_rate:
        player.pokemon.append([com_data['id'], False])
        resp_url = item_url['poke-ball']
        resp = requests.get(resp_url)
        img_url = json.loads(resp.text)['sprites']['default']
        urlopen = urllib.urlopen(img_url).read()
        img = cStringIO.StringIO(urlopen)
        load_img = pygame.image.load(img)
        t_img = pygame.transform.scale(load_img, (150, 150))
        d = t_img
        draw_battle(battle_surf, d, a, moves, player_data, com_data, 'menu')
        button('Attack', 30, 320, 165, 70, colors['ORANGE'], colors['LIGHT_ORANGE'], battle_surf, 200, 150, size=35)
        button('Run', 30, 395, 165, 70, colors['ORANGE'], colors['LIGHT_ORANGE'], battle_surf, 200, 150, size=35)
        button('Items', 200, 320, 165, 70, colors['ORANGE'], colors['LIGHT_ORANGE'], battle_surf, 200, 150, size=35)
        button('Pokemon', 200, 395, 165, 70, colors['ORANGE'], colors['LIGHT_ORANGE'], battle_surf, 200, 150, size=35)
        label = displaybattletext('You captured '+com_data['name'])
        battle_surf.blit(label, (40, 255))
        overlay.set_alpha(100)
        display.blit(overlay, (0, 0))
        display.blit(battle_surf, (200, 150))
        pygame.display.flip()
        time.sleep(2)
        Main()


def use_potion(potion):
    global player_hp
    player_hp += items[potion]
    inventory[potion] -= 1
    if player_hp > player_data['stats'][5]['base_stat']:
        player_hp = player_data['stats'][5]['base_stat']
    return player_hp

def use_item(item):
    global label, player_hp
    time.sleep(1)
    if item == 'poke-ball':
        use_pokeball()
    elif item == 'potion':
        player_hp = use_potion('potion')

    elif item == 'max-potion':
        player_hp = use_potion('max-potion')

    elif item == 'super-potion':
        player_hp = use_potion('super-potion')

    label = displaybattletext('You used a ' + item)
    battle(pokemon)


def display_items(battle_surf):
    global pokemon_img
    battle_surf.fill(colors['WORLD'])
    pygame.draw.rect(battle_surf, colors['YELLOW'], (10, 10, 380, 480))
    pygame.draw.rect(battle_surf, colors['WHITE'], (20, 20, 360, 460))
    for pos, item in enumerate(inventory):
        if inventory[item] > 0:
            if inventory[item] == 'poke-ball':
                if len(player.pokemon) < 6:
                    button(str(item)+' ('+str(inventory[item])+')', 30, 75 * pos + 30, 340, 70, colors['GREEN'], colors['LIGHT_GREEN'], battle_surf,200, 150, action=use_item, size=35, args=item)
                else:
                    button(str(item) + ' (0)', 30, 75 * pos + 30, 340, 70, colors['RED'], colors['DARK_RED'],battle_surf, 200, 150)
            else:
                button(str(item) + ' (' + str(inventory[item]) + ')', 30, 75 * pos + 30, 340, 70, colors['GREEN'],colors['LIGHT_GREEN'], battle_surf, 200, 150, action=use_item, size=35, args=item)

        else:
            button(str(item) + ' (0)', 30, 75 * pos + 30, 340, 70, colors['RED'],colors['DARK_RED'], battle_surf, 200, 150)
    for i in range(-(len(inventory)-6)):
        button('No Item', 30, 75 * (i + len(inventory)) + 30, 340, 70, colors['GREY'], colors['DARK_GREY'], battle_surf,200, 150, size=35)


def draw_battle(battle_surf, d, a, moves, player_data, com_data, __mode__):
    global player_hp, com_hp
    battle_surf.fill(colors['WORLD'])
    pygame.draw.rect(battle_surf, colors['YELLOW'], (10, 10, 380, 480))
    pygame.draw.rect(battle_surf, colors['WHITE'], (20, 20, 360, 210))
    pygame.draw.rect(battle_surf, colors['WHITE'], (20, 240, 360, 60))
    pygame.draw.rect(battle_surf, colors['WHITE'], (20, 310, 360, 170))
    battle_surf.blit(d, (180, 0))
    battle_surf.blit(a, (-10, 10))
    myfont = pygame.font.SysFont(None, 30)
    label = myfont.render('COM', 1, (0, 0, 0))
    battle_surf.blit(label, (40, 30))
    pygame.draw.rect(battle_surf, colors['RED'], (50, 50, 150, 8))
    pygame.draw.rect(battle_surf, colors['LIGHT_GREEN'], (50, 50, (com_hp / com_data['stats'][5]['base_stat']) * 150, 8))
    label = myfont.render('PLAYER', 1, (0, 0, 0))
    battle_surf.blit(label, (220, 190))
    pygame.draw.rect(battle_surf, colors['RED'], (220, 210, 150, 8))
    pygame.draw.rect(battle_surf, colors['LIGHT_GREEN'], (220, 210, (player_hp / player_data['stats'][5]['base_stat']) * 150, 8))
    if __mode__ == 'attack':
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
    if person == 'player':
        draw_battle(battle_surf, d, a, moves, player_data, com_data, 'attack')
        label = displaybattletext(com_data['name'] + ' fainted!')
        battle_surf.blit(label, (40, 255))
        overlay.set_alpha(100)
        display.blit(overlay, (0, 0))
        display.blit(battle_surf, (200, 150))
        pygame.display.flip()
        time.sleep(2)
        Main()
    if person == 'com':
        player.pokemon[current_pokemon] = [player.pokemon[current_pokemon][0], True]
        for poke in player.pokemon:
            if poke[1]:
                display_pokemon(battle_surf)
        else:
            draw_battle(battle_surf, d, a, moves, player_data, com_data, 'attack')
            label = displaybattletext(player_data['name'] + ' fainted!')
            battle_surf.blit(label, (40, 255))
            overlay.set_alpha(100)
            display.blit(overlay, (0, 0))
            display.blit(battle_surf, (200, 150))
            pygame.display.flip()
            time.sleep(2)
            Main()

def change_pokemon(num):
    global current_pokemon
    current_pokemon = num
    init_battle(pokemon, mode='menu')

def display_pokemon(battle_surf):
    global pokemon_img
    battle_surf.fill(colors['WORLD'])
    pygame.draw.rect(battle_surf, colors['YELLOW'], (10, 10, 380, 480))
    pygame.draw.rect(battle_surf, colors['WHITE'], (20, 20, 360, 460))
    for pos in range(6):
        try:
            img = pokemon_img[pos]
            try:
                if player.pokemon[pos][1] is True:
                    button(img[1]['name'], 30, 75 * pos + 30, 340, 70, colors['DARK_RED'], colors['RED'], battle_surf,200, 150, size=35)
                else:
                    button(img[1]['name'], 30, 75 * pos + 30, 340, 70, colors['GREEN'], colors['LIGHT_GREEN'], battle_surf,200, 150, action=change_pokemon, size=35, args=pos)
            except: pass
            battle_surf.blit(img[0], (20, 75 * pos + 30 - 20))
        except:
            button('No Pokemon', 30, 75 * pos + 30, 340, 70, colors['GREY'], colors['DARK_GREY'], battle_surf,200, 150, size=35)

def change_mode(x):
    time.sleep(1)
    battle(x[0]['id'], __mode__=x[1])

def battle(pokemon, __mode__='menu'):
    global move_used, label, dmg, player_hp, com_hp, escape_times, pokemon_img, battle_surf, d, a, moves, player_data, com_data
    while True:
        overlay.set_alpha(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pause(player)
        draw_battle(battle_surf, d, a, moves, player_data, com_data,__mode__)
        if __mode__ == 'menu':
            button('Attack', 30, 320, 165, 70, colors['ORANGE'], colors['LIGHT_ORANGE'], battle_surf,200,150, size=35, action=change_mode, args=(com_data, 'attack'))
            button('Run', 30, 395, 165, 70, colors['ORANGE'], colors['LIGHT_ORANGE'], battle_surf,200,150, size=35, action=change_mode, args=(com_data, 'run'))
            button('Items', 200, 320, 165, 70, colors['ORANGE'], colors['LIGHT_ORANGE'], battle_surf,200,150, size=35, action=change_mode, args=(com_data, 'items'))
            button('Pokemon', 200, 395, 165, 70, colors['ORANGE'], colors['LIGHT_ORANGE'], battle_surf,200,150, size=35, action=change_mode, args=(com_data, 'pokemon'))
        elif __mode__ == 'attack':
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
        elif __mode__ == 'items':
            display_items(battle_surf)
        elif __mode__ =='run':
            escape_times += 1
            player_speed = player_data['stats'][0]['base_stat']
            com_speed = (com_data['stats'][0]['base_stat']/4)%256
            chance = ((player_speed * 32)/com_speed) + 30 * escape_times
            roll = random.randint(0,255)
            if roll > chance or chance > 255:
                label = displaybattletext('You ran away!')
                battle_surf.blit(label, (40, 255))
                overlay.set_alpha(100)
                display.blit(overlay, (0, 0))
                display.blit(battle_surf, (200, 150))
                pygame.display.flip()
                time.sleep(2)
                Main()
            label = displaybattletext('You couldn\'t run away...')
            time.sleep(1)
            __mode__ = 'menu'
        elif __mode__ == 'pokemon':
            display_pokemon(battle_surf)
        if __mode__ == 'menu':
            battle_surf.blit(label, (40, 255))
        overlay.set_alpha(100)
        display.blit(overlay, (0, 0))
        display.blit(battle_surf, (200, 150))
        pygame.display.flip()
        if move_used:
            time.sleep(2)
            draw_battle(battle_surf, d, a, moves, player_data, com_data, __mode__)
            battle_surf.blit(label, (40, 255))
            overlay.set_alpha(100)
            display.blit(overlay, (0, 0))
            display.blit(battle_surf, (200, 150))
            pygame.display.flip()
            time.sleep(2)

            com_hp -= dmg
            if com_hp <= 0:
                won('player')
            draw_battle(battle_surf, d, a, moves, player_data, com_data, __mode__)
            label = displaybattletext('It dealt ' + str(int(dmg)) + ' damage!')
            battle_surf.blit(label, (40, 255))
            overlay.set_alpha(100)
            display.blit(overlay, (0, 0))
            display.blit(battle_surf, (200, 150))
            pygame.display.flip()
            time.sleep(2)

            if type_adv[player_data['types'][0]['type']['name']][com_data['types'][0]['type']['name']] == 2.5:
                label = displaybattletext('Its not very effective...')
            if type_adv[player_data['types'][0]['type']['name']][com_data['types'][0]['type']['name']] == 20:
                label = displaybattletext('Its super effective')
            draw_battle(battle_surf, d, a, moves, player_data, com_data, __mode__)
            battle_surf.blit(label, (40, 255))
            overlay.set_alpha(100)
            display.blit(overlay, (0, 0))
            display.blit(battle_surf, (200, 150))
            pygame.display.flip()
            time.sleep(2)

            move = json.loads(requests.get('http://pokeapi.co/api/v2/pokemon/'+ str(pokemon)).text)
            move = move['moves'][random.randint(0,len(move))]
            use_move([move,com_data,com_data,player_data])
            draw_battle(battle_surf, d, a, moves, player_data, com_data, __mode__)
            battle_surf.blit(label, (40, 255))
            overlay.set_alpha(100)
            display.blit(overlay, (0, 0))
            display.blit(battle_surf, (200, 150))
            pygame.display.flip()
            time.sleep(2)

            player_hp -= dmg
            if player_hp <= 0:
                won('com')
            draw_battle(battle_surf, d, a, moves, player_data, com_data, __mode__)
            label = displaybattletext('It dealt ' + str(int(dmg)) + ' damage!')
            battle_surf.blit(label, (40, 255))
            overlay.set_alpha(100)
            display.blit(overlay, (0, 0))
            display.blit(battle_surf, (200, 150))
            pygame.display.flip()
            time.sleep(2)

            if type_adv[com_data['types'][0]['type']['name']][player_data['types'][0]['type']['name']] == 2.5:
                label = displaybattletext('Its not very effective...')
            if type_adv[com_data['types'][0]['type']['name']][player_data['types'][0]['type']['name']] == 20:
                label = displaybattletext('Its super effective')
            draw_battle(battle_surf, d, a, moves, player_data, com_data, __mode__)
            battle_surf.blit(label, (40, 255))
            overlay.set_alpha(100)
            display.blit(overlay, (0, 0))
            display.blit(battle_surf, (200, 150))
            pygame.display.flip()
            time.sleep(2)
            move_used = False
            __mode__ = 'menu'


def init_battle(pokemon, mode='menu'):
    global move_used, label, dmg, player_hp, com_hp, escape_times, pokemon_img, battle_surf, d, a, moves, player_data, com_data
    pokemon_img = []
    for i, poke in enumerate(player.pokemon):
        if i <= 5:
            img_url = json.loads(requests.get('http://pokeapi.co/api/v2/pokemon/' + str(poke[0])).text)
            urlopen = urllib.urlopen(img_url['sprites']['front_default']).read()
            img = cStringIO.StringIO(urlopen)
            load_img = pygame.image.load(img)
            t_img = pygame.transform.scale(load_img, (95, 95))
            pokemon_img.append((t_img, img_url))
    escape_times = 0
    overlay.fill(colors['BLACK'])
    move_used = False
    battle_surf = pygame.Surface((400, 500))
    a = draw_attacker()
    d = draw_defender(pokemon)
    moves = json.loads(requests.get('http://pokeapi.co/api/v2/pokemon/' + str(player.pokemon[current_pokemon][0])).text)[
        'moves']
    player_data = json.loads(
        requests.get('http://pokeapi.co/api/v2/pokemon/' + str(player.pokemon[current_pokemon][0])).text)
    com_data = json.loads(requests.get('http://pokeapi.co/api/v2/pokemon/' + str(pokemon)).text)
    label = displaybattletext('You encountered a ' + com_data['name'])
    player_hp = player_data['stats'][5]['base_stat']
    com_hp = com_data['stats'][5]['base_stat']
    battle(pokemon, __mode__=mode)

def get_pokemon():
    chance = random.randint(1, 1000)
    global pokemon, textlog, last_cam_pos
    if chance >= 998 and camera_pos != last_cam_pos:
        if current_tile == tiles["GRASS"] or current_tile == tiles["LIGHT_GRASS"]:
            pokemon = random.choice(grass_pokemon)
            resp = requests.get(pokemon)
            textlog.append(('You encounterd a  ' + json.loads(resp.text)['name'], time.strftime("%I:%M:%S")))
            displayText()
            init_battle(json.loads(resp.text)['id'])
        elif current_tile == tiles["WATER"]:
            pokemon = random.choice(water_pokemon)
            resp = requests.get(pokemon)
            textlog.append(('You encounterd a  ' + json.loads(resp.text)['name'], time.strftime("%I:%M:%S")))
            displayText()
            pygame.display.flip()
            init_battle(json.loads(resp.text)['id'])
        else:
            last_cam_pos = camera_pos

def resume_game():
    global p
    p = False
    pause(player, paused=False)

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


def pause(player, paused=True):
    global p
    p = paused
    overlay.fill(colors['BLACK'])
    pygame.display.set_caption('Ethan\'s Pokemon Clone [PAUSED]')
    while True:
        if p:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        p = False
                        resume_game()
            player.render(world)
            display.blit(world, camera_pos)
            overlay.fill(colors['BLACK'])
            draw_legend()
            overlay.set_alpha(200)
            display.blit(overlay, (0,0))
            pause_menu()
            pygame.display.flip()
        else:
            return

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
        player.pokemon.append([1, False])
        global x
        x = False
    def c():
        player.pokemon.append([4, False])
        global x
        x = False
    def s():
        player.pokemon.append([7, False])
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
    # player.pokemon.append([23, False])
    # player.pokemon.append([432, False])
    # player.pokemon.append([12, False])
    camera_pos = (192,192)
    last_cam_pos = camera_pos


    intro = True

    game_intro()