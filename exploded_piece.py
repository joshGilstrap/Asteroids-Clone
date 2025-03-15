import pygame
import random
from constants import *

class ExplodedPiece(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        size = random.randint(10, 15)
        self.original_image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image, WHITE, [(size // 2, 0), (0, size), (size, size)])
        self.rect = self.original_image.get_rect(center=(x, y))
        self.image = self.original_image
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-3, 3), random.uniform(-3, 3))
        self.lifetime = 180;
        self.angle = 0
        self.rotation_speed = 6
    
    def update(self):
        self.angle += self.rotation_speed
        self.angle %= 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        
        self.position += self.velocity
        self.rect.center = (int(self.position.x), int(self.position.y))
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()