import pygame
import random
import time
import sys

pygame.init()

"---------------start menu---------------"
class Start_menu:
    def __init__(self, text, color, hover_color, pos, sound_effect):
        "attribute"
        self.pos = pos
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.sound_effect = sound_effect
        self.player = Player()
        self.button = Button(10, self.text, self.color, self.hover_color, self.pos, 1, self.sound_effect, self.player.surf, )
        self.draw()
        
    def draw(self):
        self.player.update()
        check_press, index = self.button.click(self.player.rect, self.player.mask)
        
        if check_press:
            global screen_state, memory    
            screen_state = "game"
            memory = []

class Button:
    def __init__(self, index, text, color, hover_color, pos, elevation, sound_effect, image_surf, press_callback=None):
        "attribute"
        #self.elevation = elevation
        #self.dynamic_elevation = elevation
        #self.original_y = pos[1]
        self.pos = pos
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.index = index
        self.preessed = False
        self.bright = False
        self.image_surf = image_surf
        self.sound = pygame.mixer.Sound(f"C:/Users/User/tsur/code/school-project/audio/{sound_effect}.mp3")
        self.press_callback = press_callback
        

        "top button"
        self.top_image = pygame.image.load(f"C:/Users/User/tsur/code/school-project/images/{text}").convert_alpha()
        #self.top_rect = self.top_image.get_rect(center = pos)
        self.top_mask = pygame.mask.from_surface(self.top_image)
        
        "hover button"
        self.bright_surf = self.top_mask.to_surface()
        self.bright_surf.set_colorkey((0,0,0))
        self.surf_w, self.surf_h = self.bright_surf.get_size()    
        
        for x in range(self.surf_w):
            for y in range(self.surf_h):
                color = self.top_image.get_at((x,y))
                if color != (0,0,0,0):
                    self.bright_surf.set_at((x,y),(max(0,color[0]-50),max(0,color[1]-50),max(0,color[2]-50)))

        "text"
        #self.text_surf = my_font.render(text,True,(225, 225, 225))
        #self.text_rect = self.text_surf.get_rect(center = self.top_image)
        
    def draw(self):
        #top button location
        #self.top_rect.y = self.original_y - self.dynamic_elevation
        #self.text_rect.center = self.top_rect.center
        
        "draw masks"
        mouse_pos = pygame.mouse.get_pos()
        if self.bright == True:
            screen.blit(self.bright_surf,self.pos)
        else:     
            screen.blit(self.top_image,self.pos)
        screen.blit(self.image_surf,(mouse_pos))
        
    "darker color for button"
    def hover(self):
        self.bright = True
        self.draw()
        pygame.display.update()
    
    "undo dark color"
    def unhover(self):
        self.bright = False
        self.draw()
        pygame.display.update()

    "checks for hovers and clicks" 
    def click(self, mouse_rect, mouse_mask):
        self.mouse_rect = mouse_rect
        self.mouse_mask = mouse_mask
        offset_x = self.pos[0] - mouse_rect.left
        offset_y = self.pos[1] - mouse_rect.top
        was_pressed = False

        if mouse_mask.overlap(self.top_mask,(offset_x, offset_y)):
            #----------------
            #print(self.text)
            #----------------
            
            if pygame.mouse.get_pressed()[0]:
                self.preessed = True
                self.bright = True
                #self.dynamic_elevation = 0
            else:
                #self.dynamic_elevation = self.elevation
                if self.preessed == True:
                    
                    #------------------------
                    #print(self.text,"click")
                    #------------------------
                    self.preessed = False  
                    self.bright = False
                    was_pressed = True
                    
                 
        else:
            #self.dynamic_elevation = self.elevation
            self.bright = False
        self.draw()
        
        return was_pressed, self.index

"---------------mouse---------------"
class Player:
    def __init__(self):
        self.surf = pygame.Surface((5,5))
        self.surf.fill((225,255,255))
        self.mask = pygame.mask.from_surface(self.surf)
        
        self.update()
    
    "updates mouse pos"
    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.rect = self.surf.get_rect(center = self.mouse_pos)

"---------------main game---------------"
class Simon:
    def __init__(self, count,colors, hover_color, texts, poses, cnt, sound_effects):
        self.cnt = cnt
        self.colors = colors
        self.level = 0
        self.buttons = []
        self.text = texts
        self.count = count
        self.poses = poses
        self.sound_effects = sound_effects
        self.player = Player()
        self.generate = True
        self.collect_input = True
        self.curr_seq = []

        for i in range(0, count):
            self.buttons.append(Button(i, texts[i],colors[i] ,hover_color[i], poses[i], 10, sound_effects[i], self.player.surf))
            

    "draws"
    def draw(self):
        self.player.update()
        for button in self.buttons:
            self.check_press, self.index = button.click(self.player.rect,self.player.mask)
            if self.check_press:
                self.test_seq(self.index) 
        self.display_score()
    def diff(self):
        if self.level < 5:
            return 500
        elif self.level < 10:
            return 250
        elif self.level < 15:
            return 200
        elif self.level < 20:
            return 125
        elif self.level < 25:
            return 100

    "generate sequens"
    def generate_seq(self):
        self.cnt = 0
        memory.append(random.randrange(0,self.count))
        self.play_seq()
        
        #-----------------
        print([keybinds[m] for m in memory])
        #-----------------
        return

    "plays sequens"
    def play_seq(self):
        self.speed =  self.diff()
        for button_idx in memory:
            curr_button = self.buttons[button_idx]
            curr_button.hover()
            curr_button.sound.play(0,self.speed)
            pygame.display.update()
            time.sleep(0.25)
            curr_button.unhover()
            time.sleep(0.25)
        return
    
    def play(self):
        if self.generate:
            self.generate_seq()
            self.generate = False

    "checks if sequens is correct"
    def test_seq(self, index):
        if memory[self.cnt] == index:
            self.cnt += 1

        elif memory[self.cnt] != index:
            global screen_state
            screen_state = "fail"

        if self.cnt >= len(memory):
            self.generate = True
            self.level += 1

    def display_score(self):
        text_score = my_font.render(f"SCORE: {self.level}", True, (225,225,225))
        screen.blit(text_score, (half_screen_width-20,half_screen_height+50))

"---------------main attributes---------------"
screen_state = "start"
cnt = 0        
memory = []
screen_height = 700
screen_width = 1200
half_screen_height = screen_height/2
half_screen_width = screen_width/2
background = pygame.image.load(f"C:/Users/User/tsur/code/school-project/images/background.png")
background = pygame.transform.scale(background, (screen_width, screen_height))
screen = pygame.display.set_mode((screen_width, screen_height))  
colors_list = [[150,0,0],[0,150,0],[0,0,150],[150,150,0],[200,100,50]]
hover_colors = [[225,0,0],[0,225,0],[0,0,225],[225,225,0],[225,100,50]]
locations = [(half_screen_width+80,half_screen_height),(half_screen_width-180,half_screen_height-120),(half_screen_width,half_screen_height-115),(half_screen_width-210,half_screen_height+50),(half_screen_width-80,half_screen_height+145)]
sounds = ["sound1","sound2","sound3","sound4","sound5"]
keybinds = ["red.png","green.png","blue.png","yellow.png","orange.png"]
my_font = pygame.font.SysFont("impact",30)
start_button = ["start_button.png", (200,200,200), (150,150,150), (half_screen_width/2, half_screen_height/2), "start"]
fail_button = ["game_over.png", (200,200,200), (150,150,150), (half_screen_width/2, half_screen_height/2), "start"]
start_menu = Start_menu(start_button[0], start_button[1], start_button[2], start_button[3], start_button[4])
end_screen = Start_menu(fail_button[0], fail_button[1], fail_button[2], fail_button[3], fail_button[4])
simon = Simon(5, colors_list, hover_colors, keybinds, locations,cnt,sounds)
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

"---------------main loop---------------"
run = True
while run:
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:
            run = False
    screen.fill((0,0,0))
    screen.blit(background, (0, 0))
    if screen_state == "start":
        start_menu.draw()
        pygame.display.update()
    elif screen_state == "fail":
        end_screen.draw()
        pygame.display.update()        
    elif screen_state == "game":
        simon.draw()
        pygame.display.update()
        simon.play()
        pygame.display.update()

    clock.tick(60)
pygame.quit()