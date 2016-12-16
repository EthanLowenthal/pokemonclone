import pygame
pygame.init()


map = [
[2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,2,2,0,1,2,2,2,2,0,0,0,0,0,0,0],
[0,0,0,0,0,2,1,1,1,1,1,1,2,2,0,0,0,0,0,0],
[0,0,0,0,2,2,1,1,1,1,1,2,2,2,0,0,0,0,0,0],
[0,0,0,0,2,2,1,1,1,1,2,2,2,0,0,0,0,0,0,0],
[0,0,0,0,2,2,0,1,1,2,2,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,2,1,3,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,3,1,2,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]

class Player:
    def __init__(self):
        self.image = pygame.Surface((16,16))
        self.image.fill(colors["WHITE"])
        self.rect = pygame.Rect((50,50),(16,16))


    def move(self,camera_pos):
        pos_x,pos_y = camera_pos
        #
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.rect.y -= 8
            pos_y += 8
        if key[pygame.K_a]:
            self.rect.x -= 8
            pos_x += 8
        if key[pygame.K_s]:
            self.rect.y += 8
            pos_y -= 8
        if key[pygame.K_d]:
            self.rect.x += 8
            pos_x -= 8
        #
        if self.rect.x < 0:
            self.rect.x = 0
            pos_x = camera_pos[0]
        elif self.rect.x > 984:
            self.rect.x = 984
            pos_x = camera_pos[0]
        if self.rect.y < 0:
            self.rect.y = 0
            pos_y = camera_pos[1]
        elif self.rect.y > 984:
            self.rect.y = 984
            pos_y = camera_pos[1]

        return (pos_x,pos_y)

    def render(self,display):
        display.blit(self.image,(self.rect.x,self.rect.y))



def Main(display,clock):
    world = pygame.Surface((1000,1000))
    world.fill(colors["BLACK"])
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
        #
        camera_pos = player.move(camera_pos)
        #
        display.fill(colors["WHITE"])
        world.fill(colors["BLACK"])

        for pos2, line in enumerate(map):
            for pos1, wall in enumerate(line):
                if wall == 1:
                    pygame.draw.rect(world, colors["BLUE"], ((pos1 * 50, pos2 * 50), (50, 50)))
                if wall == 2:
                    pygame.draw.rect(world, colors["GREEN"], ((pos1 * 50, pos2 * 50), (50, 50)))
                if wall == 3:
                    pygame.draw.rect(world, colors["RED"], ((pos1 * 50, pos2 * 50), (50, 50)))


        player.render(world)
        display.blit(world,camera_pos)

        pygame.display.flip()

if __name__ in "__main__":
    display = pygame.display.set_mode((800,800))
    pygame.display.set_caption("Scrolling Camera")
    clock = pygame.time.Clock()

    global colors
    colors = {
    "WHITE":(255,255,255),
    "RED"  :(255,0,0),
    "GREEN":(0,102,0),
    "BLUE" :(0,0,255),
    "BLACK":(0,0,0)
    }
    Main(display,clock)