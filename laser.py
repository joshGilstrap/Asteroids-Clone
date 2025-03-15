import pygame
import math
from constants import *

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((5, 5), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (2, 2), 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, -1).rotate(-angle) * 10
    
    def update(self):
        self.position += self.velocity
        self.rect.center = (int(self.position.x), int(self.position.y))
        
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.kill()