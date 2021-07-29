import pygame
import math
import os
from settings import PATH_A, PATH_B

ENEMY_HP_W = 40
ENEMY_HP_H = 4

RED = (255, 0, 0)
GREEN = (0, 255, 0)


pygame.init()
ENEMY_IMAGE = pygame.image.load(os.path.join("images", "enemy.png"))



class Enemy:
    
    def __init__(self, path_choice):
        self.width = 40
        self.height = 50
        self.image = pygame.transform.scale(ENEMY_IMAGE, (self.width, self.height))
        self.health = 5
        self.max_health = 10
        
        # path choice A or B
        self.path_choice = path_choice
        if self.path_choice % 2 == 1:
            self.path = PATH_A
        else :
            self.path = PATH_B        
        
        self.path_pos = 0
        self.move_count = 0
        self.stride = 1
        self.x, self.y = self.path[0]
        
    def draw(self, win):
        # draw enemy
        win.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))
        # draw enemy health bar
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        """
        Draw health bar on an enemy
        :param win: window
        :return: None
        """        
        pygame.draw.rect(win, RED, [self.x - self.width // 2, self.y - self.height // 2, ENEMY_HP_W , ENEMY_HP_H])
        pygame.draw.rect(win, GREEN, [self.x - self.width // 2, self.y - self.height // 2, ENEMY_HP_W * (self.health / self.max_health), ENEMY_HP_H])        

    def move(self):
        """
        Enemy move toward path points every frame
        :return: None
        """
        ax, ay = self.path[self.path_pos]
        bx, by = self.path[self.path_pos + 1]
        distance_ab = math.sqrt((bx-ax)**2 + (by-ay)**2)
        max_count = int (distance_ab / self.stride) 

        if self.move_count < max_count:
            unit_vector_x = (bx - ax) / distance_ab
            unit_vector_y = (by - ay) / distance_ab
            delta_x = unit_vector_x * self.stride
            delta_y = unit_vector_y * self.stride

            # update the coordinate and the counter
            self.x += delta_x
            self.y += delta_y
            self.move_count += 1
        # next path position    
        else: 
            self.path_pos += 1
            self.move_count = 0
            
class EnemyGroup:
    def __init__(self):
        self.gen_count = 0
        self.gen_period = 120   # (unit: frame)
        self.reserved_members = []
        self.expedition = []  # don't change this line until you do the EX.3 
        self.path_flag = 0

    def campaign(self):
        """
        Send an enemy to go on an expedition once 120 frame
        :return: None
        """
        
        #  compaign one enemy per 120 frames
        self.gen_count += 1
        if (self.gen_count % self.gen_period == 0) and (self.reserved_members != []):
            self.expedition.append(self.reserved_members.pop())
            
        

    def generate(self, num):
        """
        Generate the enemies in this wave
        :param num: enemy number
        :return: None
        """
        # campaign and change another path
        self.path_flag += 1
        for i in range (num):
            self.reserved_members.append(Enemy(self.path_flag))
        

    def get(self):
        """
        Get the enemy list
        """
        return self.expedition

    def is_empty(self):
        """
        Return whether the enemy is empty (so that we can move on to next wave)
        """
        return False if self.reserved_members else True

    def retreat(self, enemy):
        """
        Remove the enemy from the expedition
        :param enemy: class Enemy()
        :return: None
        """
        self.expedition.remove(enemy)





