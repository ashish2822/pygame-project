import pygame, sys
pygame.init()
FONT = pygame.font.SysFont("comicsans",30)
class Button:
    def __init__(self,text,width,height,pos,elevation):

        # self.top_rect.y = self.original_y_pos - self.dynammic_elivation

        self.pressed = False
        self.elevation = elevation
        self.dynamic_elivation = elevation
        self.original_y_pos = pos[1]

        self.top_rect = pygame.Rect(pos,(width,height)) 
        self.top_color = '#475F77'

        self.bottom_rect = pygame.Rect(pos,(width,elevation))
        self.bottom_color = '#354B5E'

        # text
        self.text_surf = FONT.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)


    def draw(self):

        self.top_rect.y = self.original_y_pos - self.dynamic_elivation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elivation
        pygame.draw.rect(WIN,self.bottom_color,self.bottom_rect,border_radius=12)
        pygame.draw.rect(WIN,self.top_color,self.top_rect,border_radius=12)
        WIN.blit(self.text_surf,self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elivation = 0
                self.pressed = True
            else:
                self.dynamic_elivation = self.elevation
                if self.pressed == True:
                    print('click')
                    self.pressed = False
        else:
            self.dynamic_elivation = self.elevation
            self.top_color = '#475F77'


pygame.init()
WIN = pygame.display.set_mode((500,500))
pygame.display.set_caption('Gui Menu')
clock = pygame.time.Clock()
gui_font = pygame.font.Font(None,30)

button1 = Button('click',200,40,(200,250),6)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    WIN.fill('#DCDDD8')
    button1.draw()

    pygame.display.update()
    clock.tick(60)