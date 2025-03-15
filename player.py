import pygame
from constants import *
from laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image, WHITE, [(15, 0), (0, 30), (30, 30)])
        pygame.draw.polygon(self.original_image, DARK_GREY, [(15, 5), (5, 25), (25, 25)])
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = 0.1
        self.max_speed = 5
        self.rotation_speed = 3
        self.angle = 0
        self.friction = 0.98
        
        self.lasers = pygame.sprite.Group()
        self._can_shoot = False
    
    def update(self):
        keys = pygame.key.get_pressed()
        self.fire(keys)
        self.rotate(keys)
        self.accelerate(keys)
        self.move()
        self.check_bounds()
    
    def rotate(self, keys):
        if keys[pygame.K_LEFT]:
            self.angle += self.rotation_speed
        if keys[pygame.K_RIGHT]:
            self.angle -= self.rotation_speed
        
        self.angle %= 360
        
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def accelerate(self, keys):
        if keys[pygame.K_UP]:
            acceleration_vector = pygame.Vector2(0, -self.acceleration).rotate(-self.angle)
            self.velocity += acceleration_vector
            if self.velocity.length() > self.max_speed:
                self.velocity.scale_to_length(self.max_speed)
        
        if keys[pygame.K_DOWN]:
            acceleration_vector = pygame.Vector2(0, self.acceleration / 2).rotate(-self.angle)
            self.velocity += acceleration_vector
            if self.velocity.length() > self.max_speed:
                self.velocity.scale_to_length(self.max_speed)
        
        self.velocity *= self.friction
    
    def move(self):
        self.position += self.velocity
        self.rect.center = (int(self.position.x), int(self.position.y))
    
    def check_bounds(self):
        if self.rect.left > SCREEN_WIDTH:
            self.position.x = 0
            self.rect.center = (int(self.position.x), int(self.position.y))
        elif self.rect.right < 0:
            self.position.x = SCREEN_WIDTH
            self.rect.center = (int(self.position.x), int(self.position.y))
        
        if self.rect.top > SCREEN_HEIGHT:
            self.position.y = 0
            self.rect.center = (int(self.position.x), int(self.position.y))
        elif self.rect.bottom < 0:
            self.position.y = SCREEN_HEIGHT
            self.rect.center = (int(self.position.x), int(self.position.y))
            
    def fire(self, keys):
        if keys[pygame.K_SPACE] and self._can_shoot:
            offset = pygame.Vector2(0, -15).rotate(-self.angle)
            position = self.position + offset
            self.lasers.add(Laser(position.x, position.y, self.angle))
            self._can_shoot = False
        elif not keys[pygame.K_SPACE]:
            self._can_shoot = True
