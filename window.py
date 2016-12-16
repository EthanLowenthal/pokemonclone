import pygame, time
from maps import *

pygame.init()

map = mid


class Player:
    def __init__(self):
        self.image = pygame.Surface((16,16))
        self.image.fill(colors["WHITE"])
        self.rect = pygame.Rect((50,50),(16,16))
        self.speed = 5

    def change_world(self):
        display.fill(colors["BLACK"])
        world.fill(colors["BLACK"])
        pygame.display.flip()
        time.sleep(0.7)

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
            if map == left:
                self.rect.x = 0
            elif map == mid or map == up or map == down:
                map = left
                self.rect.x = 984
            elif map == right:
                map = mid
                self.rect.x = 984
            self.change_world()


        elif self.rect.x > 984:
            if map == right:
                self.rect.x = 984
            elif map == mid or map == up or map == down:
                map = right
                self.rect.x = 0
            elif map == left:
                map = mid
                self.rect.x = 0
            self.change_world()

        if self.rect.y < 0:
            self.rect.y = 984
            if map == up:
                self.rect.y = 0
                pos_y = camera_pos[1]
            elif map == mid or map == left or map == right:
                map = up
            elif map == down:
                map = mid
            self.change_world()

        elif self.rect.y > 984:

            global map
            self.rect.y = 0
            if map == down:
                self.rect.y = 984
            elif map == mid or map == left or map == right:
                map = down
            elif map == up:
                map = mid
            self.change_world()

        pos_x, pos_y = -self.rect.x + 400, -self.rect.y + 400
        return (pos_x, pos_y)

    def render(self,display):
        display.blit(self.image,(self.rect.x,self.rect.y))



def Main(display,clock, world):
    for x in range(10):
        pygame.draw.rect(world,colors["BLUE"],((x * 100,x * 100),(20,20)))
    #
    player = Player()
    camera_pos = (192,192)
    #
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        camera_pos = player.move(camera_pos)

        display.fill(colors["WORLD"])
        world.fill(colors["DARK_GREEN"])

        for pos2, line in enumerate(map):
            for pos1, wall in enumerate(line):
                if wall == 1:
                    pygame.draw.rect(world, colors["BLUE"], ((pos1 * 50, pos2 * 50), (50, 50)))
                if wall == 2:
                    pygame.draw.rect(world, colors["LIGHT_GREEN"], ((pos1 * 50, pos2 * 50), (50, 50)))
                if wall == 3:
                    pygame.draw.rect(world, colors["DARK_RED"], ((pos1 * 50, pos2 * 50), (50, 50)))
                if wall == 4:
                    pygame.draw.rect(world, colors["GREY"], ((pos1 * 50, pos2 * 50), (50, 50)))
                if wall == 5:
                    pygame.draw.rect(world, colors["LIGHT_BLUE"], ((pos1 * 50, pos2 * 50), (50, 50)))

        def draw_map():
            pygame.draw.rect(display, colors["WHITE"], ((15, 15), (120, 120)))
            pygame.draw.rect(display, colors["LIGHT_BLUE"], ((25, 25), (100, 100)))

            # pygame.draw.rect(display, colors["DARK_RED"], ((32, 32), (25, 25)))
            # pygame.draw.rect(display, colors["DARK_RED"], ((32, 92), (25, 25)))
            # pygame.draw.rect(display, colors["DARK_RED"], ((92, 32), (25, 25)))
            # pygame.draw.rect(display, colors["DARK_RED"], ((92, 92), (25, 25)))


            pygame.draw.rect(display, colors["DARK_RED"], ((32, 62), (25, 25))) #left
            pygame.draw.rect(display, colors["DARK_RED"], ((62, 32), (25, 25))) #up
            pygame.draw.rect(display, colors["DARK_RED"], ((62, 62), (25, 25))) #mid
            pygame.draw.rect(display, colors["DARK_RED"], ((62, 92), (25, 25))) #down
            pygame.draw.rect(display, colors["DARK_RED"], ((92, 62), (25, 25))) #right

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


        player.render(world)
        display.blit(world,camera_pos)

        draw_map()


        pygame.display.flip()

if __name__ in "__main__":
    global colors
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
        "YELLOW": (255, 255, 51)

    }
    display = pygame.display.set_mode((800,800))
    clock = pygame.time.Clock()
    world = pygame.Surface((1000,1000))


    Main(display,clock,world)