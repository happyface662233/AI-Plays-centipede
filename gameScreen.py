import sys
import pygame
from random import randint
from math import trunc
import SnakeEnemy
from time import sleep
from settings import *
from player import player
import threading
# print(dir(SnakeEnemy))
pygame.init()

print('HEIGHT ', height, 'WIDTH ', width)
win = pygame.display.set_mode((size))

pygame.display.set_caption("AI Leans Centipede")


def moveSnake(s):
    while s.dead == False and end == False:
        s.move()
        sleep(sleepForSnake)


def notInEmpty(empty, x, y):
    for e in empty:
        if e[0] == x and e[1] == y:
            return True
    return False


def makeGrid(empty: list) -> list:
    points = []

    for x in range(tilesWide):
        for y in range(trunc(tilesHeight*(2/3))):
            c = randint(0, 4)
            if c == 0 and notInEmpty(empty, x, y) == False:
                points.append([x, y])
    return points


def generatePath(x: int, y: int) -> list:  # x and y tile not coord
    path = []
    # print(tilesHeight-(trunc(tilesHeight/3)))
    while y < tilesHeight-(trunc(tilesHeight/3)):
        choice = randint(0, 2)
        c2 = randint(0, 100)
        # print('looping', choice)
        if choice == 0 and x != tilesWide:
            # print('if 1')
            x += 1
            path.append([x, y])
        elif choice == 1 and x != 0:
            x -= 1
            # print('if 2')
            path.append([x, y])
        elif choice == 2 and y != tilesHeight:
            y += 1
            # print('if 3')
            path.append([x, y])
        if c2 < divertThresh:
            # print('divert')
            path += generatePath(x, y)

    return path


path1 = generatePath(0, 0)
path2 = generatePath(trunc(tilesWide/2), 0)
# print(path2)
snakes = [SnakeEnemy.snakeEnemy(trunc(tilesWide/2), 0, 10)]
path3 = generatePath(tilesWide, 0)
empty = path1+path2+path3
# print(len(path3))
grid = makeGrid(empty)
running = True
p = player(25, 24)
p.shoot()
t = threading.Thread(target=moveSnake, args=[snakes[0]])
t.start()
snakes[0].grid = grid


while running:
    clock.tick(FPS)
    win.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            end = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                p.moveUp()
                # print('pressed')
            elif event.key == pygame.K_s:
                p.moveDown()
            elif event.key == pygame.K_a:
                p.moveLeft()
            elif event.key == pygame.K_d:
                p.moveRight()
            elif event.key == pygame.K_SPACE:
                p.shoot()
            break
    for space in grid:
        # print(space[0]*(width/tilesWide))
        pygame.draw.rect(win, (0, 0, 255), pygame.Rect(
            space[0]*(width/tilesWide), space[1]*(height/tilesHeight), width/tilesWide, height/tilesHeight))
    # s.move(grid)
    # s.move([])
    for s in snakes:
        win = s.show(win)
    win = p.show(win)

    win, ns = p.update(win, snakes, grid)

    if ns != []:
        print(ns)
        for s in ns:
            s.grid = grid
            snakes.append(s)
            t = threading.Thread(target=moveSnake, args=[s])
            t.start()
    # pygame.draw.rect(win, (0, 0, 255), pygame.Rect(
    #     1*(s.width/s.tilesWide), 1*(s.height/s.tilesHeight), s.width/s.tilesWide, s.height/s.tilesHeight))

    # print(s.x,s.y)
    pygame.display.flip()
    #print(1*(s.width/s.tilesWide), 1*(s.height/s.tilesHeight))
    new = []
    for i, s in enumerate(snakes):
        if s.dead == False:
            new.append(s)
    snakes = new


pygame.quit()
