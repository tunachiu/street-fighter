import pygame
from pygame import mixer

import sys

from Button import *
from config import *
from InputName import *

pygame.init()  # call all the features in pygame package

clock = pygame.time.Clock()
fps = 60

# game window
screen_width = 1200
screen_height = 450
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (210,105,30)
GREEN = (154,205,50)
YELLOW = (255,215,0)

screen = pygame.display.set_mode((screen_width, screen_height))  # set the size the the game window
pygame.display.set_caption('Street Fighter')  # setting the title for the game window
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# background music
mixer.music.load('sounds/background music.mp3')
mixer.music.play(-1)
jump_sound = mixer.Sound('sounds/jump.mp3')
punch_sound = mixer.Sound('sounds/attack/punch.mp3')
kick_sound = mixer.Sound('sounds/attack/kick.mp3')


class GameIntro:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.instruct = False
        self.start = False
        self.play = False
        self.running = True

        self.player1 = ''
        self.player2 = ''

        self.font = pygame.font.Font('COPRGTB.TTF', 60)

        self.intro_background = pygame.image.load("menu/bg.png")

        self.instruct_background = pygame.image.load("menu/Instruction Screen.png")
        self.get_name_background = pygame.image.load("menu/enter_name.png")

    def check_to_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def menu(self):
        intro = True

        play_button = Button(SCREEN_WIDTH/1.4, SCREEN_HEIGHT/4, 250, 70, WHITE, BROWN, 'PLAY', 30)
        instruction_button = Button(SCREEN_WIDTH/1.4, SCREEN_HEIGHT/1.7, 250, 70, WHITE, BROWN, 'INSTRUCTIONS', 25)
        while intro:
            self.check_to_quit()

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
                self.play = True
                self.instruct = False
            if instruction_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
                self.instruct = True
                self.play = False

            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(instruction_button.image, instruction_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def instruction(self):
        play_button = Button(SCREEN_WIDTH/2.5, SCREEN_HEIGHT/1.25, 250, 70, WHITE, BROWN, 'PLAY', 30)
        while self.instruct:
            self.screen.blit(self.instruct_background, (0,0))
            self.screen.blit(play_button.image, play_button.rect)

            self.check_to_quit()

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
                self.play = True
                self.instruct = False
            self.clock.tick(FPS)
            pygame.display.update()

    def enter_name(self):
        next_button = Button(SCREEN_WIDTH/2.3, SCREEN_HEIGHT/5, 200, 60, WHITE, BROWN, 'NEXT', 30)
        while self.play:
            #self.check_to_quit()

            self.screen.blit(self.get_name_background, (0,0))
            self.screen.blit(next_button.image, next_button.rect)

            # Enter name
            name_box_1 = InputBox(270, 80, 100, 40, font_size=32)
            name_box_2 = InputBox(890, 80, 100, 40, font_size=32)
            names = [name_box_1, name_box_2]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                for name in names:
                    name.draw(screen)
            #for name in names:
                #name.draw(self.screen)
            self.player1 = name_box_1.name
            self.player2 = name_box_2.name

            # Start
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if next_button.is_pressed(mouse_pos, mouse_pressed):
                self.start = True
                self.play = False
                self.instruct = False

            self.clock.tick(FPS)
            pygame.display.update()


# load images
# background image

def Game_Start():
    update_time = pygame.time.get_ticks()
    countdown_list = []
    img_index = -1
    sound_index = 0
    for i in range(1, 6):
        img = pygame.image.load(f'start/{i}.png')
        countdown_list.append(img)
    img = countdown_list[0]
    running = True
    bg = pygame.image.load(f'background/0.gif')
    scale = screen_width / bg.get_width()
    print(scale)
    bg = pygame.transform.scale(bg, (bg.get_width() * scale, bg.get_height() * scale))

    while running:
        try:
            screen.blit(bg, (0, 0))
            cooldown = 300
            if pygame.time.get_ticks() - update_time > cooldown:
                update_time = pygame.time.get_ticks() + cooldown
                img = img.set_colorkey([0, 0, 0])
                img_index += 1
                if img_index == len(countdown_list) - 1:
                    running = False
                img = countdown_list[img_index]
                sound = mixer.Sound(f'sounds/intro/{img_index}.mp3')
                sound.play()
            screen.blit(img, (500, 200))
        except FileNotFoundError:
            running = False
        pygame.display.update()


def Game_Over():
    pass


class Background:
    def __init__(self):
        """Set components to manage multiple frames of the background"""
        self.background_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        for i in range(8):
            bg = pygame.image.load(f'background/{i}.gif')
            scale = screen_width / bg.get_width()
            bg = pygame.transform.scale(bg, (bg.get_width() * scale, bg.get_height() * scale))
            self.background_list.append(bg)
        self.background_img = self.background_list[self.frame_index]

    def update(self):
        """Update images for the animation"""
        animation_cooldown = 100
        # handle animation
        # update images
        self.background_img = self.background_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.background_list):
                self.frame_index = 0

    def draw(self):
        """Draw the background"""
        screen.blit(self.background_img, (0, 0))


# fighter class
class Fighter:
    def __init__(self, x, y, name, img_scale):
        self.name = name
        self.max_hp = 200
        self.hp = 200
        self.alive = True
        self.action = 'idle'
        self.scale = img_scale  # scale to adjust the size of the character image
        img = pygame.image.load(f'char_img/{self.name}/{self.action}.gif')
        self.image = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
        self.frame_index = 0
        self.x = x
        self.y = y
        shot_image = pygame.image.load(f'char_img/{self.name}/power_shot.png')
        self.shot_image = pygame.transform.scale(shot_image, (shot_image.get_width() / 2, shot_image.get_height() / 2))
        self.speed = 10
        self.jump = False
        self.in_air = False
        self.flip = False
        self.direction = 1
        self.update_time = pygame.time.get_ticks()
        self.vel_y = 0
        self.special_power = Power_Shoot(self.x, self.y, self.shot_image, self.name, self.direction)
        #self.health_bar = HealthBar(self.name, self.max_hp)

    def move(self, move_left, move_right):  # method for moving left and right
        """Method for character movement left, right"""
        if self.name == 'Guile':
            if move_left and self.x >= 0:  # check move and set boundary so the image won't move outside the screen
                self.x -= self.speed
                self.flip = True
                self.direction = -1
            if move_right and self.x <= screen_width - self.image.get_width() - self.speed:
                self.x += self.speed
                self.flip = False
                self.direction = 1
        if self.name == 'Ryu':
            if move_left and self.x >= 0:  # check move and set boundary so the image won't move outside the screen
                self.x -= self.speed
                self.flip = False
                self.direction = -1
            if move_right and self.x <= screen_width - self.image.get_width() - self.speed:
                self.x += self.speed
                self.flip = True
                self.direction = 1

    def jumping(self):
        """Method for jump"""
        jump_step = 0
        GRAVITY = 0.3
        if first_fighter.jump and self.in_air == False:
            self.action = 'jump'
            self.draw()
            jump_sound.play()
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 20:
            self.vel_y = 20
        jump_step += self.vel_y

        # check collision with floor
        if self.y + jump_step > 250:
            jump_step = 250 - self.y
            self.in_air = False
        # update rectangle position
        self.y += jump_step
        self.special_power.y = self.y

    def draw(self):  # draw the character
        """Draw the fighter"""
        img = pygame.image.load(f'char_img/{self.name}/{self.action}.gif')
        self.image = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.x, self.y))

    def attack(self):
        if self.action == 'punch':
            punch_sound.play()
            self.draw()
        if self.action == 'kick':
            kick_sound.play()
            self.draw()
        if self.action == 'special_power':
            self.special_power.sound.play()
            self.draw()
        if power_shot:
            self.special_power.shoot()
            self.special_power.hp_substract()

        if pygame.time.get_ticks() - self.update_time > 600:
            self.update_time = pygame.time.get_ticks()
            self.action = 'idle'
            self.draw()

    def hp_check(self):
        if self.hp == 0:
            self.alive = False


class Power_Shoot:
    """Create special power object and shooting"""
    def __init__(self, x, y, shot_image, name, direction):
        self.shot_image = shot_image
        self.name = name
        self.sound = self.special_sound = mixer.Sound(f'sounds/attack/power {self.name}.mp3')
        self.x = x
        self.y = y
        self.x_vel = 20
        self.direction = direction
        self.flip = False

    def shoot(self):
        if self.name == 'Guile':
            if self.direction == 1:
                self.flip = False
            if self.direction == -1:
                self.flip = True
        else:
            if self.direction == 1:
                self.flip = True
            if self.direction == -1:
                self.flip = False
        self.x += self.x_vel * self.direction
        screen.blit(pygame.transform.flip(self.shot_image, self.flip, False), (self.x, self.y))

    def hp_substract(self):
        if self.name == 'Ryu':
            if abs(self.x - second_fighter.x) <= 10 and abs(self.y - second_fighter.y) < 80:
                second_fighter.hp -= 15

        else:
            if abs(self.x - first_fighter.x) <= 10 and abs(self.y - first_fighter.y) < 80:
                first_fighter.hp -= 15

'''
class HealthBar:
    def __init__(self, char_name, max_hp):
        self.char_name = char_name
        if self.char_name == 'Guile':
            self.x = 217
            self.y = 65
        else:
            self.x = 795
            self.y = 63
        self.max_hp = max_hp
        self.length = 195  # Độ dài energy bar
        #self.image = pygame.image.load(f"char_img/{self.char_name}/hp bar.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 0.7, self.image.get_height() * 0.7))

    def draw(self, hp):
        if self.char_name == 'Guile':
            screen.blit(self.image, (200, 10))
        else:
            screen.blit(self.image, (700, 10))
        if hp > self.max_hp * 0.5:
            pygame.draw.rect(screen, GREEN, (self.x, self.y, int(hp * self.length/self.max_hp), 20))
        elif hp > self.max_hp * 0.2:
            pygame.draw.rect(screen, YELLOW, (self.x, self.y, int(hp * self.length/self.max_hp), 20))
        else:
            pygame.draw.rect(screen, RED, (self.x, self.y, int(hp * self.length/self.max_hp), 20))
'''

# game variables
background_img = Background()
second_fighter = Fighter(250, 250, 'Guile', 0.8)
first_fighter = Fighter(950, 250, 'Ryu', 0.7)
move_left = False
move_right = False
power_count = 100
run = True
power_shot = False

g = GameIntro()
g.menu()

g.instruction()
g.enter_name()
first_fighter_name = g.player1
second_fighter_name = g.player2

#Game_Start()
while run:  # the run loop
    clock.tick(fps)  # set up the same speed of display for any animation in the game

    # draw background
    background_img.update()
    background_img.draw()

    # draw fighters:
    first_fighter.draw()
    #first_fighter.health_bar.draw(first_fighter.hp)
    first_fighter.hp_check()
    # first_fighter.test()
    second_fighter.draw()
    #second_fighter.health_bar.draw(second_fighter.hp)
    second_fighter.hp_check()

    for event in pygame.event.get():
        """Exit game input"""
        if event.type == pygame.QUIT:
            run = False

        """Character left/right movement input/ Hold pressed key"""
        if event.type == pygame.KEYDOWN:  # check for key presses
            if event.key == pygame.K_b:  # input key is B
                move_left = True
            if event.key == pygame.K_f:  # input key is F
                move_right = True
            if event.key == pygame.K_SPACE:
                first_fighter.jump = True
            if event.key == pygame.K_p:  # punch
                first_fighter.action = 'punch'
                if abs(first_fighter.x - second_fighter.x) < 90 and abs(first_fighter.y - second_fighter.y) < 80:
                    second_fighter.hp -= 10
            if event.key == pygame.K_k:  # kick
                first_fighter.action = 'kick'
                if abs(first_fighter.x - second_fighter.x) < 90 and abs(first_fighter.y - second_fighter.y) < 80:
                    second_fighter.hp -= 10
            if event.key == pygame.K_s:  # special power
                power_count -= 1
                first_fighter.special_power.x = first_fighter.x
                first_fighter.special_power.y = first_fighter.y
                first_fighter.special_power.direction = first_fighter.direction
                if power_count >= 0 and first_fighter.hp >= first_fighter.max_hp * 0.2:
                    power_shot = True
                    first_fighter.action = 'special_power'

        if event.type == pygame.KEYUP:  # check for key releases
            if event.key == pygame.K_b:  # key B released
                move_left = False
            if event.key == pygame.K_f:  # key F is released
                move_right = False

    # if first_fighter.alive:
    first_fighter.move(move_left, move_right)
    first_fighter.attack()
    first_fighter.jumping()

    if first_fighter.hp <= 0 or second_fighter.hp <= 0:
        Game_Over()
    print(second_fighter.hp)

    pygame.display.update()  # to update all added images
pygame.quit()
