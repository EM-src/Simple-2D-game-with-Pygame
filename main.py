import pygame
from sys import exit
import os
from random import randint

# chnage the current working directory
os.chdir('/Users/manosmarketos/Desktop/Dev/Pygame')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_run_1 = pygame.image.load('graphics/player/playerRun1.png').convert_alpha()
        player_run_2 = pygame.image.load('graphics/player/playerRun2.png').convert_alpha()
        player_run_3 = pygame.image.load('graphics/player/playerRun3.png').convert_alpha()
        player_run_4 = pygame.image.load('graphics/player/playerRun4.png').convert_alpha()
        player_run_5 = pygame.image.load('graphics/player/playerRun5.png').convert_alpha()
        player_jump_1 = pygame.image.load('graphics/player/playerJump1.png').convert_alpha()
        player_jump_2 = pygame.image.load('graphics/player/playerJump2.png').convert_alpha()
        player_jump_3 = pygame.image.load('graphics/player/playerJump3.png').convert_alpha()
        player_jump_4 = pygame.image.load('graphics/player/playerJump4.png').convert_alpha()
        self.player_run = [player_run_1,player_run_2,player_run_3,player_run_4,player_run_5]
        self.player_run_index = 0
        self.player_jump = [player_jump_1,player_jump_2,player_jump_3,player_jump_4]
        self.player_jump_index = 0
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')

        self.image = self.player_run[self.player_run_index]
        self.rect = self.image.get_rect(midbottom = (35,400))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 345:
            self.gravity = -16
            self.jump_sound.play()
            self.jump_sound.set_volume(0.1)
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 345:
            self.rect.bottom = 345

    def animation_state(self):
        if self.rect.bottom < 345:
            self.player_jump_index +=0.2
            if self.player_jump_index >= len(self.player_jump):
                self.player_jump_index = 0
            self.image = self.player_jump[int(self.player_jump_index)]
        else:
            self.player_run_index += 0.1
            if self.player_run_index >= len(self.player_run):
                self.player_run_index = 0
            self.image = self.player_run[int(self.player_run_index)]

    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        car1_surf = pygame.image.load('graphics/cars/car1.png').convert_alpha()
        car2_surf = pygame.image.load('graphics/cars/car2.png').convert_alpha()
        car3_surf = pygame.image.load('graphics/cars/car3.png').convert_alpha()
        car4_surf = pygame.image.load('graphics/cars/car4.png').convert_alpha()
        self.obstacle_rect_list = [car1_surf,car2_surf,car3_surf,car4_surf]
        
        match randint(0,3):
            case 0:
                self.image = self.obstacle_rect_list[0]
                self.rect = self.image.get_rect(midbottom = (randint(900,1100), randint(360,364)))
            case 1:
                self.image = self.obstacle_rect_list[1]
                self.rect = self.image.get_rect(midbottom = (randint(900,1100), randint(360,364)))
            case 2:
                self.image = self.obstacle_rect_list[2]
                self.rect = self.image.get_rect(midbottom = (randint(900,1100), randint(360,364)))
            case 3:
                self.image = self.obstacle_rect_list[3]
                self.rect = self.image.get_rect(midbottom = (randint(900,1100), randint(360,364)))
            case _:
                pass
        
    def update(self):
        self.rect.x -= 5
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = text_font.render(f'Score: {current_time}', False, (188, 19, 254))
    score_rect = text_surf.get_rect(center = (150,150))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle in obstacle_list:
            obstacle.x -= 5
            match obstacle.bottom:
                case 360:
                    screen.blit(car1_surf, obstacle)
                case 361:
                    screen.blit(car2_surf, obstacle)
                case 362:
                    screen.blit(car3_surf, obstacle)
                case 363:
                    screen.blit(car4_surf, obstacle)
                case _:
                    pass

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

def collisions(player, obstacle):
    if obstacle:
        for obstacle_rect in obstacle:
            if player_rect.colliderect(obstacle_rect):
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle, False):
        obstacle.empty()
        return False
    else:
        return True

def player_animation():
    global player_surf, player_jump_index, player_run_index
    if player_rect.bottom < 345:
        player_jump_index += 0.2
        if player_jump_index >= len(player_jump):
            player_jump_index = 0
        player_surf = player_jump[int(player_jump_index)]
    else:
        player_run_index += 0.1
        if player_run_index >= len(player_run):
            player_run_index = 0
        player_surf = player_run[int(player_run_index)]

pygame.init()
screen = pygame.display.set_mode((800,385))

# Sets the title of the Pygame window (icon could be updated too)
pygame.display.set_caption('Pygame Traffic')

# Clock Object to control frame rate
clock = pygame.time.Clock()

# Game state control
game_active = True
start_time = 0
score = 0

player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle = pygame.sprite.Group()

music = pygame.mixer.Sound('audio/music.wav')
music.play(loops = -1)
music.set_volume(0.2)

text_font = pygame.font.Font('pixel_font/Pixel_font.ttf', 35)

# Defining the images that will be used as assets in the screen display
sky_surf = pygame.image.load('graphics/Pygame_sky.png').convert()
ground_surf = pygame.image.load('graphics/Pygame_road.png').convert()

text_surf = text_font.render('Lixouri Vice', False, (188, 19, 254))
text_rect = text_surf.get_rect(center = (650,150))

game_over_text = 'Game Over'
instructions = 'Press \'Enter\' to restart'
game_over_surf = text_font.render(f'{game_over_text}', False, (188, 19, 254))
instructions_surf = text_font.render(f'{instructions}', False, (188, 19, 254))
game_over_rect = game_over_surf.get_rect(center = (400,100))
instructions_rect = instructions_surf.get_rect(center = (400,260))

# Obstacles
car1_surf = pygame.image.load('graphics/cars/car1.png').convert_alpha()
car2_surf = pygame.image.load('graphics/cars/car2.png').convert_alpha()
car3_surf = pygame.image.load('graphics/cars/car3.png').convert_alpha()
car4_surf = pygame.image.load('graphics/cars/car4.png').convert_alpha()
obstacle_rect_list = []

# player_surf = pygame.image.load('graphics/player/player.png').convert_alpha()
player_run_1 = pygame.image.load('graphics/player/playerRun1.png').convert_alpha()
player_run_2 = pygame.image.load('graphics/player/playerRun2.png').convert_alpha()
player_run_3 = pygame.image.load('graphics/player/playerRun3.png').convert_alpha()
player_run_4 = pygame.image.load('graphics/player/playerRun4.png').convert_alpha()
player_run_5 = pygame.image.load('graphics/player/playerRun5.png').convert_alpha()
player_run_index = 0
player_run = [player_run_1,player_run_2,player_run_3,player_run_4,player_run_5]

player_jump_1 = pygame.image.load('graphics/player/playerJump1.png').convert_alpha()
player_jump_2 = pygame.image.load('graphics/player/playerJump2.png').convert_alpha()
player_jump_3 = pygame.image.load('graphics/player/playerJump3.png').convert_alpha()
player_jump_4 = pygame.image.load('graphics/player/playerJump4.png').convert_alpha()
player_jump_index = 0
player_jump = [player_jump_1,player_jump_2,player_jump_3,player_jump_4]

player_surf = player_run[player_run_index]
player_rect = player_surf.get_rect(midbottom = (35,345))
scaled_player = pygame.transform.scale2x(player_surf)
# Introducing player gravity which is essentially a counter that will increase with each game loop soit gives the impression of gravity
player_gravity = 0

# Timer
obstacle_timer = pygame.USEREVENT +1
pygame.time.set_timer(obstacle_timer, 1400)

# This loop will run for as long as it breaks from the inside. The entire game will run from this loop and
# all elements will be placed in the loop
while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

# Implementing the jump using space bar, and also allowing the player to perform a jump only if he is already touching the ground
        if game_active:            
            if event.type == obstacle_timer:
                obstacle.add(Obstacle())
        else:
            if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                obstacle_rect_list.clear()
                game_active = True
                start_time = pygame.time.get_ticks()
    
    if game_active:
        screen.blit(sky_surf,(0,0))
        screen.blit(ground_surf,(0,320))
        pygame.draw.rect(screen, "Pink", text_rect)
        screen.blit(text_surf,text_rect)
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle.draw(screen)
        obstacle.update()

        # Collison
        game_active = collision_sprite()

    else:
        screen.fill("Black")
        screen.blit(game_over_surf, game_over_rect)
        screen.blit(scaled_player, (370,120))
        score_message_surf = text_font.render(f'You lasted for {score} seconds...', False, (188, 19, 254))
        score_message_rect = score_message_surf.get_rect(center = (400,220))
        screen.blit(score_message_surf, score_message_rect)
        screen.blit(instructions_surf, instructions_rect)

    # Updates the display surface
    pygame.display.update()
    # Ceiling for frame rate. Not higher frame rate than 60 per second
    clock.tick(60)