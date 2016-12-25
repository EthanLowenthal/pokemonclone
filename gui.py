import pygame
from window import colors

class Checkbox:
    def __init__(self, surface, x, y, color=(230, 230, 230), caption="", outline_color=(0, 0, 0),
                 check_color=(0, 0, 0), font_size=22, font_color=(0, 0, 0), text_offset=(28, 1), surf_offset=(0,0)):
        self.surface = surface
        self.surf_offset = surf_offset
        self.x = x
        self.y = y
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fs = font_size
        self.fc = font_color
        self.to = text_offset
        # checkbox object
        self.checkbox_obj = pygame.Rect(self.x, self.y, 12, 12)
        self.checkbox_outline = self.checkbox_obj.copy()
        # variables to test the different states of the checkbox
        self.checked = False
        self.active = False
        self.unchecked = True
        self.click = False

    def _draw_button_text(self):
        self.font = pygame.font.Font(None, self.fs)
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + 12 / 2 - w / 2 + self.to[0], self.y + 12 / 2 - h / 2 + self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render_checkbox(self):
        if self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
            pygame.draw.circle(self.surface, self.cc, (self.x + 6, self.y + 6), 4)

        elif self.unchecked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
        self._draw_button_text()

    def _update(self, event_object):
        x, y = event_object.pos
        # self.x, self.y, 12, 12
        px, py, w, h = self.checkbox_obj  # getting check box dimensions
        if px < x - self.surf_offset[0] < px + w and px < x - self.surf_offset[0] < px + w:
            self.active = True
        else:
            self.active = False

    def _mouse_up(self):
            if self.active and not self.checked and self.click:
                    self.checked = True
            elif self.checked:
                self.checked = False
                self.unchecked = True

            if self.click is True and self.active is False:
                if self.checked:
                    self.checked = True
                if self.unchecked:
                    self.unchecked = True
                self.active = False

    def update_checkbox(self, event_object):
        if event_object.type == pygame.MOUSEBUTTONDOWN:
            self.click = True
            # self._mouse_down()
        if event_object.type == pygame.MOUSEBUTTONUP:
            self._mouse_up()
        if event_object.type == pygame.MOUSEMOTION:
            self._update(event_object)

    def is_checked(self):
        if self.checked is True:
            return True
        else:
            return False

    def is_unchecked(self):
        if self.checked is False:
            return True
        else:
            return False

def button(title,x,y,width,height,inactive_color,active_color,display,sufcoordsx=0,sufcoordsy=0, action=None, size=40, args=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+width+sufcoordsx > mouse[0] > x+sufcoordsx and y+height+sufcoordsy > mouse[1] > y+sufcoordsy:
        pygame.draw.rect(display, active_color,(x,y,width,height))
        if click[0] == 1 and action != None:
            global intro
            intro = False
            if args is not None:
                action(args)
            else:
                action()
    else:
        pygame.draw.rect(display, inactive_color,(x,y,width,height))
    smallText = pygame.font.SysFont(None, size)
    textSurf = smallText.render(title, True, colors['BLACK'])
    textRect = textSurf.get_rect()
    textRect.center = ((x+(width/2)), (y+(height/2)))
    display.blit(textSurf, textRect)


# while True:
#     button('TEST', 100, 100, 100, 300, (0,102,0),(0,153,0),screen, action=myFunction)
def fake_button(msg,x,y,w,h,ic,ac,display,sufcoordsx,sufcoordsy, action=None, size=40, args=None):
    pygame.draw.rect(display, ic, (x, y, w, h))
    smallText = pygame.font.SysFont(None, size)
    textSurf = smallText.render(msg, True, colors['BLACK'])
    textRect = textSurf.get_rect()
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    display.blit(textSurf, textRect)