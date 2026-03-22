import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 612, 612
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
x, y = (WIDTH//2, HEIGHT//2)
angle = random.random() * 2 * math.pi
v = 2

# Classes --------------------------------------------------------------------------------

class Wall:
    def __init__(self, pStart, pEnd):
        self.p_start = pStart
        self.p_end = pEnd
        self.angle = math.atan2((-1 * (self.p_start[0]- self.p_end[0])), (self.p_start[1] - self.p_end[1]))
        self.normal = (math.cos(theta), math.sin(theta))

    def x(self, y):
        return (y/math.tan(theta))
    
    def y(self, x):
        return (x*math.tan(theta))
    

# Subprogram --------------------------------------------------------------------------------

def reflect(surfaceVector, point):
    sx = surfaceVector[0]
    sy = surfaceVector[1]
    angle = math.atan2(point[1], point[0])

    px, py = math.cos(angle), math.sin(angle)
    dot = px * sx + py * sy

    return (( - py*(dot)), ( - px*(dot)))

# Main --------------------------------------------------------------------------------

theta = 0
size = 400  # width | height
x_center = (WIDTH - ((size)*math.cos(theta)+(size)*math.cos(theta+math.pi/2)))//2
y_center = (WIDTH - ((size)*math.sin(theta)+(size)*math.sin(theta+math.pi/2)))//2

wallTop = Wall((x_center, y_center), ((size)*math.cos(theta) + x_center, (size)*math.sin(theta) + y_center))
wallLeft = Wall((x_center, y_center), ((size)*math.cos(theta+math.pi/2) + x_center, (size)*math.sin(theta+math.pi/2) + y_center))
wallRight = Wall((wallTop.p_end[0], wallTop.p_end[1]), (wallTop.p_end[0] + wallLeft.p_end[0] - x_center, wallTop.p_end[1] + wallLeft.p_end[1] - y_center))
wallBottom = Wall((wallLeft.p_end[0], wallLeft.p_end[1]), (wallLeft.p_end[0] + wallTop.p_end[0] - x_center, wallLeft.p_end[1] + wallTop.p_end[1] - y_center))
while True:
    dt = 0.6
    screen.fill("black")
    frameTime = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass

    nextPos = (x + math.cos(angle)*v*dt, y + math.sin(angle)*v*dt)
    #if theta:
    #    if nextPos[0] > wallRight.x(nextPos[1]):
    #        v[0], v[1] = reflect(wallRight.normal, (math.cos(angle)*v, v))
    #    elif nextPos[0] < wallLeft.x(nextPos[1]):
    #        v[0], v[1] = reflect(wallLeft.normal, (math.cos(angle)*v, v))

    #    elif nextPos[1] > wallTop.y(nextPos[0]):
    #        v[0], v[1] = reflect(wallTop.normal, (math.cos(angle)*v, v))
    #    elif nextPos[1] < wallBottom.y(nextPos[0]):
    #        v[0], v[1] = reflect(wallBottom.normal, (math.cos(angle)*v, v))

    #    else:
    #        y += v*dt
    #        x += math.cos(angle)*v*dt
    #else:
    if 100 > nextPos[0]:
        o, a = reflect(wallLeft.normal, (math.cos(angle)*v, v))
        angle = math.atan(o/ a)
    elif 500 < nextPos[0]:
        o, a = reflect(reflect(wallRight.normal, (math.cos(angle)*v, v)))
        angle = math.atan(o/ a)

    elif 500 < nextPos[1]:
        print(reflect(wallBottom.normal, (math.cos(angle)*v, v)))
        print(wallBottom.normal)
        o, a = reflect(wallBottom.normal, (math.cos(angle)*v, v))
        angle = math.atan(o/ a)
        
        print()
    elif 100 > nextPos[1]:
        o, a = reflect(reflect(wallTop.normal, (math.cos(angle)*v, v)))
        angle = math.atan(o/ a)
    else:
        y += math.sin(angle)*v*dt
        x += math.cos(angle)*v*dt
    pygame.draw.circle(screen, 'red', (x, y), 10)

    pygame.draw.line(screen, 'green', wallTop.p_start, wallTop.p_end, 5)
    pygame.draw.line(screen, 'green', wallLeft.p_start, wallLeft.p_end, 5)
    pygame.draw.line(screen, 'green', wallRight.p_start, wallRight.p_end, 5)
    pygame.draw.line(screen, 'green', wallBottom.p_start, wallBottom.p_end, 5)

    pygame.display.update()
    clock.tick(60)