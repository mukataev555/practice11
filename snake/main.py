import pygame
import random
import time

pygame.init()


WIDTH, HEIGHT = 600, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake: Mukataev Alibek")


WHITE = (255,255,255)
GREEN= (0,255,0)
RED = (255, 0, 0)
YELLOW = (255,255,0)
BLACK = (0, 0, 0)

SNAKE_BLOCK = 20
font_style = pygame.font.SysFont("Times New Roman", 25)

pygame.mixer.music.load("background.mp3") 
pygame.mixer.music.play(-1) 
pygame.mixer.music.set_volume(0.5)

def show_score(score, level):
    value = font_style.render(f"Score: {score}  Level: {level}", True, WHITE)
    SCREEN.blit(value, [10, 10])

def generate_food(snake_body):
    while True:
        x = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 20.0) * 20.0
        y = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 20.0) * 20.0
        if [x, y] not in snake_body:
            weight = 5 if random.randint(1, 10) > 8 else 1
            spawn_time = pygame.time.get_ticks() 
            return x, y, weight, spawn_time

def game_loop():
    game_over = False
    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_c, y1_c = 0, 0
    snake_body = []
    length_of_snake = 1
    
    score = 0
    level = 1
    speed = 10
    food_timer = 5000 #перемещается через 5 секунд еда

    food_x, food_y, food_weight, food_spawn_time = generate_food(snake_body)
    clock = pygame.time.Clock()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_c == 0:
                    x1_c, y1_c = -SNAKE_BLOCK, 0
                elif event.key == pygame.K_RIGHT and x1_c == 0:
                    x1_c, y1_c = SNAKE_BLOCK, 0
                elif event.key == pygame.K_UP and y1_c == 0:
                    y1_c, x1_c = -SNAKE_BLOCK, 0
                elif event.key == pygame.K_DOWN and y1_c == 0:
                    y1_c, x1_c = SNAKE_BLOCK, 0

        #границы
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_over = True

        x1 += x1_c
        y1 += y1_c
        SCREEN.fill(BLACK)

        #через время еда исчезает
        current_time = pygame.time.get_ticks()
        if current_time - food_spawn_time > food_timer:
            food_x, food_y, food_weight, food_spawn_time = generate_food(snake_body)

        food_color = YELLOW if food_weight == 5 else RED
        pygame.draw.rect(SCREEN, food_color, [food_x, food_y, SNAKE_BLOCK, SNAKE_BLOCK])

        # Логика змейки
        snake_head = [x1, y1]
        snake_body.append(snake_head)
        if len(snake_body) > length_of_snake:
            del snake_body[0]

        for segment in snake_body[:-1]:
            if segment == snake_head:
                game_over = True

        for segment in snake_body:
            pygame.draw.rect(SCREEN, GREEN, [segment[0], segment[1], SNAKE_BLOCK, SNAKE_BLOCK])

        if x1 == food_x and y1 == food_y:
            score += food_weight
            length_of_snake += 1
            if score // 5 >= level:
                level += 1
                speed += 2
            food_x, food_y, food_weight, food_spawn_time = generate_food(snake_body)

        show_score(score, level)
        pygame.display.update()
        clock.tick(speed)

    pygame.quit()

game_loop()