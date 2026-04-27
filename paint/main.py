import pygame, sys, math
from pygame.locals import *

pygame.init()

# Настройки экрана
fps = 120
timer = pygame.time.Clock()
WIDTH = 1000 
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pro Paint by Mukataev Alibek07')

active_size = 3
active_color = (0, 0, 0)
active_shape = 0  
painting = []

drawing = False
start_pos = (0, 0)
current_pos = (0, 0)

run = True

def get_points(shape, start, end):
    x1, y1 = start
    x2, y2 = end
    w, h = x2 - x1, y2 - y1
    if shape == 2: return [(x1 + w // 2, y1), (x1, y2), (x2, y2)]
    elif shape == 3:
        side = abs(w)
        alt = int(side * (math.sqrt(3) / 2))
        direction = 1 if h > 0 else -1
        return [(x1 + w // 2, y1), (x1 + w // 2 - side // 2, y1 + alt * direction), (x1 + w // 2 + side // 2, y1 + alt * direction)]
    elif shape == 4: return [(x1 + w // 2, y1), (x2, y1 + h // 2), (x1 + w // 2, y2), (x1, y1 + h // 2)]
    return []

def draw_objects(paints):
    for p in paints:
        color, start, end, thickness, shape = p
        if shape == 5: 
            pygame.draw.circle(screen, 'white', start, thickness * 5)
        else:
            rect = pygame.Rect(start, (end[0] - start[0], end[1] - start[1]))
            rect.normalize()
            if shape == 0: pygame.draw.ellipse(screen, color, rect, thickness)
            elif shape == 1: pygame.draw.rect(screen, color, rect, thickness)
            else:
                pts = get_points(shape, start, end)
                if pts: pygame.draw.polygon(screen, color, pts, thickness)

def draw_menu(color, size, shape):
    pygame.draw.rect(screen, 'gray', [0, 0, WIDTH, 70])
    pygame.draw.line(screen, 'black', (0, 70), (WIDTH, 70), 3)
    
    # Толщина
    t_btns = [pygame.draw.rect(screen, 'black', [10 + i*50, 15, 45, 45]) for i in range(3)]
    for i, t in enumerate([1, 3, 5]):
        pygame.draw.line(screen, 'white', (15 + i*50, 37), (50 + i*50, 37), t)
    curr_t = {1:0, 3:1, 5:2}.get(size, 1)
    pygame.draw.rect(screen, 'green', [10 + curr_t*50, 15, 45, 45], 3)

    # Фигуры + Ластик
    sh_btns = []
    for i in range(6):
        btn = pygame.draw.rect(screen, 'black', [180 + i*55, 15, 45, 45])
        sh_btns.append(btn)
        if shape == i: pygame.draw.rect(screen, 'green', [180 + i*55, 15, 45, 45], 3)

    # Иконки
    pygame.draw.circle(screen, 'white', (202, 37), 12, 1)
    pygame.draw.rect(screen, 'white', [243, 23, 28, 28], 1)
    pygame.draw.polygon(screen, 'white', [(307, 23), (292, 52), (322, 52)], 1)
    pygame.draw.polygon(screen, 'white', [(362, 23), (347, 48), (377, 48)], 1)
    pygame.draw.polygon(screen, 'white', [(417, 20), (432, 37), (417, 54), (402, 37)], 1)
    # Иконка ластика
    pygame.draw.rect(screen, (255, 255, 255), [465, 25, 30, 25])
    pygame.draw.rect(screen, 'white', [465, 25, 30, 10])

    # Цвета
    rgbs = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (0, 0, 0), (255, 255, 255), (255, 255, 0)]
    c_rects = [pygame.draw.rect(screen, c, [WIDTH - 210 + i*32, 22, 25, 25]) for i, c in enumerate(rgbs)]

    return t_btns, sh_btns, c_rects, rgbs

while run:
    timer.tick(fps)
    screen.fill('white')
    draw_objects(painting)

    mouse_pos = pygame.mouse.get_pos()

    if drawing:
        if active_shape == 5:
            # Ластик работает в реальном времени: добавляем точки постоянно
            painting.append(('white', mouse_pos, mouse_pos, active_size, 5))
        else:
            # Для фигур рисуем временный контур
            r = pygame.Rect(start_pos, (mouse_pos[0]-start_pos[0], mouse_pos[1]-start_pos[1]))
            r.normalize()
            if active_shape == 0: pygame.draw.ellipse(screen, active_color, r, active_size)
            elif active_shape == 1: pygame.draw.rect(screen, active_color, r, active_size)
            else:
                pts = get_points(active_shape, start_pos, mouse_pos)
                if pts: pygame.draw.polygon(screen, active_color, pts, active_size)

    t_b, s_b, c_r, rgbs = draw_menu(active_color, active_size, active_shape)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False
        if event.type == MOUSEBUTTONDOWN:
            if event.pos[1] < 70:
                for i, b in enumerate(t_b):
                    if b.collidepoint(event.pos): active_size = [1, 3, 5][i]
                for i, b in enumerate(s_b):
                    if b.collidepoint(event.pos): active_shape = i
                for i, r_c in enumerate(c_r):
                    if r_c.collidepoint(event.pos): active_color = rgbs[i]
            else:
                drawing = True
                start_pos = event.pos
        
        if event.type == MOUSEBUTTONUP:
            if drawing:
                if active_shape != 5: # Сохраняем фигуру только при отпускании
                    painting.append((active_color, start_pos, event.pos, active_size, active_shape))
                drawing = False

    pygame.display.flip()
pygame.quit()