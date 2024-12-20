import pygame
import random
import time
import sys

pygame.init()

class Button:
    def __init__(self , index, text, color ,hover_color ,pos , elevation):
        #attribute
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y = pos[1]
        self.pos = pos
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.index = index
        self.preessed = False

        #top button
        self.top_image = pygame.image.load(f"{text}.png").convert_alpha()
        self.top_rect = self.top_image.get_rect(center = pos)
        self.top_mask = pygame.mask.from_surface(self.top_image)
        self.top_mask.fill()
        
        
        #bottom button
        self.bottom_image = pygame.image.load(f"{text}.png").convert_alpha()
        self.bottom_rect = self.bottom_image.get_rect(center = pos)
        self.bottom_mask = pygame.mask.from_surface(self.bottom_image)
        self.bottom_color = (50,25,25)

        #text
        self.text_surf = my_font.render(text,True,(225, 225, 225))
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        
    def draw(self):
        #top button location
        self.top_rect.y = self.original_y - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center
        
        #draw rect
        screen.blit(self.top_image,self.pos)
        
        #centers and draw text 
        screen.blit(self.text_surf,self.text_rect)

    def hover(self):
        self.top_color = self.hover_color
        self.draw()
        pygame.display.update()

        
    def unhover(self):
        self.top_color = self.color
        self.draw()
        pygame.display.update()

    def click(self,mouse_pos):
        if self.top_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.preessed = True
                self.dynamic_elevation = 0
            else:
                self.dynamic_elevation = self.elevation
                if self.preessed == True:
                    # #------------------------
                    print(self.text,"click")
                    # #------------------------
                    self.preessed = False  
                    simon.test_seq(self.index)
                    #-------------------------
                    # print(self.text,"click")
                    #-------------------------
                 
        else:
            self.dynamic_elevation = self.elevation

        self.draw()
            
class Simon:
    def __init__(self, count,colors, hover_color, texts, poses, cnt):
        self.cnt = cnt
        self.colors = colors
        self.buttons = []
        self.text = texts
        self.count = count
        self.poses = poses
        self.generate = True
        self.collect_input = True
        self.curr_seq = []

        for i in range(0, count):
            self.buttons.append(Button(i, texts[i],colors[i] ,hover_color[i], poses[i], 10))
            
    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.click(mouse_pos)

    def generate_seq(self):
        self.cnt = 0

        memory.append(random.randrange(0,self.count))
        self.play_seq()

        # #-----------------
        print([keybinds[m] for m in memory])
        # #-----------------
        return
    def play_seq(self):
        for button_idx in memory:
            curr_button = self.buttons[button_idx]

            curr_button.hover()
            pygame.display.update()
            time.sleep(0.5)
            curr_button.unhover()
            time.sleep(0.5)

        return
    def play(self):

        if self.generate:
            self.generate_seq()
            self.generate = False

    def test_seq(self, index):
        if memory[self.cnt] == index:
            self.cnt += 1

        elif memory[self.cnt] != index:
            exit()

        if self.cnt >= len(memory):
            self.generate = True

cnt = 0        
memory = []
screen_height = 700
screen_width = 700
colors_list = [[150,0,0],[0,150,0],[0,0,150],[150,150,0],[200,100,50]]
hover_colors = [[225,0,0],[0,225,0],[0,0,225],[225,225,0],[225,100,50]]
locations = [(460,345),(210,200),(405,185),(180,415),(342,455)]
keybinds = ["red","green","blue","yellow","orange"]
my_font = pygame.font.SysFont("impact",30)
screen = pygame.display.set_mode((screen_width, screen_height))
simon = Simon(5, colors_list, hover_colors, keybinds, locations,cnt)
# game = Game(memory, keybinds)

clock = pygame.time.Clock()

run = True
while run:
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:
            run = False
    screen.fill((0,0,0))

    simon.draw()
    pygame.display.update()
    simon.play()
    pygame.display.update()

    clock.tick(60)
pygame.quit()