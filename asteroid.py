import pygame
import random
from constants import *

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, size=3):
        super().__init__()
        
        self.size = size
        self.radius = size * 10
        
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.image, DARK_BROWN, (self.radius, self.radius), self.radius - 3)
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
        self.speed_x = random.uniform(-ASTEROID_SPEED, ASTEROID_SPEED)
        self.speed_y = random.uniform(-ASTEROID_SPEED, ASTEROID_SPEED)
    
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        if self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
            self.x = self.rect.x
        elif self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
            self.x = self.rect.x
        if self.rect.top > SCREEN_WIDTH:
            self.rect.bottom = 0
            self.y = self.rect.y
        elif self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT
            self.y = self.rect.y
    
    def split(self):
        if self.size > 1:
            new_size = self.size - 1
            return [Asteroid(self.rect.centerx, self.rect.centery, new_size),
                    Asteroid(self.rect.centerx, self.rect.centery, new_size)]
        else:
            return []