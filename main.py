import pygame
import random
from player import Player
from asteroid import Asteroid
from exploded_piece import ExplodedPiece
from constants import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
explosion_pieces = pygame.sprite.Group()

player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
all_sprites.add(player)
player_alive = True

asteroid_timer = random.randint(ASTEROID_SPAWN_MIN, ASTEROID_SPAWN_MAX)
total_asteroid_goal = 80
total_asteroids_hit = 0

score = 0
score_font = pygame.font.Font(None, 46)
has_won = False

def setup_game():
    global all_sprites, asteroids, explosion_pieces, player, player_alive, asteroid_timer, score, has_won
    all_sprites = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    explosion_pieces = pygame.sprite.Group()
    
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    all_sprites.add(player)
    player_alive = True
    
    asteroid_timer = random.randint(200, 400)
    
    score = 0
    
    has_won = False

    for _ in range(INITIAL_ASTEROID_COUNT):
        while True:
            x = random.randrange(SCREEN_WIDTH)
            y = random.randrange(SCREEN_HEIGHT)
            if abs(x - player.rect.centerx) > 100 and abs(y - player.rect.centery) > 100:
                break
        asteroid = Asteroid(x, y)
        all_sprites.add(asteroid)
        asteroids.add(asteroid)

coords = []
for _ in range(1000):
    coords.append([random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), 2, 2])

def render_stars():
    for coord in coords:
        coord[1] += 0.5
        if coord[1] > SCREEN_HEIGHT:
            coord[1] = 0
        pygame.draw.rect(screen, random.choice([WHITE, GREY]), coord)

start_font = pygame.font.Font(None, 128)
enter_font = pygame.font.Font(None, 64)
start_text = start_font.render("ASTEROIDS", True, WHITE)
enter_text = enter_font.render("Press SPACE to start!", True, WHITE)

def start_screen():
    screen.fill(BLACK)
    render_stars()
    screen.blit(start_text, ((SCREEN_WIDTH - start_text.get_width()) // 2, (SCREEN_HEIGHT - start_text.get_height()) // 2))
    screen.blit(enter_text, ((SCREEN_WIDTH - enter_text.get_width()) // 2, SCREEN_HEIGHT - (SCREEN_HEIGHT // 3)))

def death_screen():
    screen.fill(BLACK)
    render_stars()
    lose_text = start_font.render("YOU DIED", True, RED)
    instruct_text = enter_font.render("Press Enter To Play Again!", True, WHITE)
    score_text = score_font.render("Score: " + str(score), True, WHITE)
    asteroid_text = score_font.render("Asteroids destroyed: " + str(total_asteroids_hit), True, WHITE)
    screen.blit(lose_text, (SCREEN_WIDTH // 2 - lose_text.get_width() // 2, SCREEN_HEIGHT // 2 - lose_text.get_height() // 2))
    screen.blit(instruct_text, (SCREEN_WIDTH // 2 - instruct_text.get_width() // 2, SCREEN_HEIGHT // 2 + instruct_text.get_height()))
    screen.blit(score_text, (20, 20))
    screen.blit(asteroid_text, (SCREEN_WIDTH - asteroid_text.get_width() - 20, 20))
    
has_started = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE and not has_started:
                has_started = True
                setup_game()
            if event.key == pygame.K_RETURN and (has_won or not player_alive):
                has_started = False
                setup_game()
    
    if not has_started:
        start_screen()
    elif not has_won:
        all_sprites.update()
        player.lasers.update()
        
        if player_alive:
            player_hit = pygame.sprite.spritecollide(player, asteroids, True)
            for hit in player_hit:
                for _ in range(4):
                    piece = ExplodedPiece(player.rect.centerx, player.rect.centery)
                    all_sprites.add(piece)
                    explosion_pieces.add(piece)
                player.kill()
                player_alive = False
                new_asteroids = hit.split()
                for asteroid in new_asteroids:
                    all_sprites.add(asteroid)
                    asteroids.add(asteroid)
                asteroids.remove(hit)
                    
            for laser in player.lasers:
                hits = pygame.sprite.spritecollide(laser, asteroids, True)
                if hits:
                    player.lasers.remove(laser)
                for hit in hits:
                    total_asteroids_hit += 1
                    score += 1000 * (3 - hit.size + 1) + int((abs(hit.speed_x) * abs(hit.speed_y)))
                    if hit.size > 1:
                        new_asteroids = hit.split()
                        for asteroid in new_asteroids:
                            all_sprites.add(asteroid)
                            asteroids.add(asteroid)
                    asteroids.remove(hit)
            
            asteroid_timer -= 1
            if total_asteroids_hit // 4 < total_asteroid_goal // 4 and asteroid_timer <= 0:
                asteroid_timer = random.randint(ASTEROID_SPAWN_MIN, ASTEROID_SPAWN_MAX)
                top_or_left = random.choice([True, False])
                if top_or_left:
                    if random.randint(0, 1) == 0:
                        y = -50
                        x = random.randint(0, SCREEN_WIDTH)
                    else:
                        y = SCREEN_HEIGHT + 50
                        x = random.randint(0, SCREEN_WIDTH)
                else:
                    if random.randint(0, 1) == 0:
                        x = -50
                        y = random.randint(0, SCREEN_HEIGHT)
                    else:
                        x =  SCREEN_WIDTH + 50
                        y = random.randint(0, SCREEN_HEIGHT)
                asteroid = Asteroid(x, y)
                all_sprites.add(asteroid)
                asteroids.add(asteroid)
                
            if total_asteroids_hit >= total_asteroid_goal:
                has_won = True
                
            screen.fill(BLACK)
            render_stars()
            all_sprites.draw(screen)
            player.lasers.draw(screen)
            score_text = score_font.render("Score: " + str(score), True, WHITE)
            screen.blit(score_text, (20, 20))
        else:
            if len(explosion_pieces) > 0:
                screen.fill(BLACK)
                render_stars()
                all_sprites.draw(screen)
                player.lasers.draw(screen)
                pass
            else:
                death_screen()
    elif has_won:
        screen.fill(BLACK)
        render_stars()
        win_text = start_font.render("YOU WIN!", True, WHITE)
        instruct_text = enter_font.render("Press Enter To Play Again!", True, WHITE)
        score_text = enter_font.render("Score: " + str(score), True, WHITE)
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - win_text.get_height() // 2))
        screen.blit(instruct_text, (SCREEN_WIDTH // 2 - instruct_text.get_width() // 2, SCREEN_HEIGHT // 2 + instruct_text.get_height()))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 10))
        
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()