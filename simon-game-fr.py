import pygame
import random
pygame.init()


class Button:
    def __init__(self ,text ,width ,height ,color ,hover ,pos , elevation):
        #attribute
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y = pos[1]
        self.pos = pos
        self.width = width
        self.height = height
        self.color = color
        self.hover = hover
        self.preessed = False
         
        #top button
        print(pos[0],pos[1]-100)
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = color
        
        #bottom button
        self.bottom_rect = pygame.Rect(pos[0],(pos[1]),width,height)
        self.bottom_color = (50,25,25)
        
        #text
        self.text_surf = my_font.render(text,True,(0, 0, 0))
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        
        
        
    def draw(self):
        #top button location
        self.top_rect.y = self.original_y - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center
        
        #draw rect
        pygame.draw.rect(screen,tuple(self.bottom_color),self.bottom_rect,border_radius=15)
        pygame.draw.rect(screen,tuple(self.top_color),self.top_rect,border_radius=15)
        
        #centers and draw text 
        screen.blit(self.text_surf,self.text_rect)
        mouse_pos = pygame.mouse.get_pos()
        self.click(mouse_pos)
    
    
    def click(self,mouse_pos):
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.hover

            if pygame.mouse.get_pressed()[0]:
                self.preessed = True
                self.dynamic_elevation = 0
                
            else:
                self.dynamic_elevation = self.elevation
                if self.preessed == True:
                    print("click")
                    self.preessed = False
 
        else:
            self.top_color = self.color
            self.dynamic_elevation = self.elevation
                
                
                
                
class Simon:
    def __init__(self ,count ,width ,height ,colors ,hover_color ,texts, poses):
        self.width = width
        self.height = height
        self.colors = colors
        self.buttons = []

        for i in range(0,count):
            self.buttons.append(Button(texts[i], width, height, colors[i] ,hover_color[i] , poses[i], 20))
            
    def draw(self):
        for button in self.buttons:
            button.draw()
            #pygame.draw.rect(border_radius=15)
            #screen.blit(self.dic[i]["text_surf"],self.dic[i]["text_rect"])




screen_height = 700
screen_width = 700
hover_colors = [[150,0,0],[0,150,0],[0,0,150],[150,150,0]]
colors_list = [[225,0,0],[0,225,0],[0,0,225],[225,225,0]]
locations = [(100,100),(100,400),(400,400),(400,100)]
keybinds = ["R","G","B","Y"]
my_font = pygame.font.SysFont("impact",30)
simon = Simon(4 ,200, 200, colors_list, hover_colors, keybinds, locations)
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

run = True
while run:
    
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:
            run = False
    screen.fill((0,0,0))
    simon.draw()
           
    pygame.display.update()
    clock.tick(60)
pygame.quit()            
