import pygame
import sys
import random
pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Just Dodge")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PLAYER_COLOR = (0, 150, 0)
BLOCKS = (200, 0, 0)

player_width = 50
player_height = 10
player_x = (WIDTH - player_width) // 2
player_y = HEIGHT - player_height - 10
player_speed = 6

block_width = 40
block_height = 40
block_speed = 5
block_list = []

ADD_BLOCK_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_BLOCK_EVENT, 800)

score = 0
font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()

def draw_player(x, y):
    pygame.draw.rect(screen, PLAYER_COLOR, (x, y, player_width, player_height))

def draw_block(block):
    pygame.draw.rect(screen, BLOCKS, block)

def display_score(current_score):
    score_surface = font.render("score: " + str(current_score), True, BLACK)
    screen.blit(score_surface, (10, 10))

def game_over():
    game_over_txt = font.render("!GAME OVER! Final Score: " + str(score), True, BLACK)
    screen.blit(game_over_txt, (WIDTH // 2 - game_over_txt.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(4000)
    pygame.quit()    
    sys.exit()


running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == ADD_BLOCK_EVENT:
            block_x = random.randint(0, WIDTH - block_width)
            new_block = pygame.Rect(block_x, 0, block_width, block_height)
            block_list.append(new_block)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_x -= player_speed
        if player_x < 0:
            player_x = 0
    if keys[pygame.K_d]:
        player_x += player_speed
        if player_x > WIDTH - player_width:
            player_x = WIDTH - player_width

    screen.fill(WHITE)

    draw_player(player_x, player_y)

    for block in block_list[:]:
        block.y += block_speed
        draw_block(block)

        if block.y > HEIGHT:
            block_list.remove(block)
            score += 1

        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        if block.colliderect(player_rect):
            game_over()

    if score > 0 and score % 10 == 0:
        block_speed = 3 + score // 10

    display_score(score)
    pygame.display.flip()
        
pygame.quit()