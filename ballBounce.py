import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 612, 612
walls = {}
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

    px, py = point[0], point[1]
    dot = px * sx + py * sy

    return ((px - 2*px*(dot)), (py - 2*py*(dot)))

# Main --------------------------------------------------------------------------------

theta = 0.6
size = 400  # width | height


while True:
    x_center = (WIDTH - ((size)*math.cos(theta)+(size)*math.cos(theta+math.pi/2)))//2
    y_center = (WIDTH - ((size)*math.sin(theta)+(size)*math.sin(theta+math.pi/2)))//2
    walls.update({"0" : Wall((x_center, y_center), ((size)*math.cos(theta) + x_center, (size)*math.sin(theta) + y_center))})
    walls.update({"1" : Wall((x_center, y_center), ((size)*math.cos(theta+math.pi/2) + x_center, (size)*math.sin(theta+math.pi/2) + y_center))})
    walls.update({"2" : Wall((walls.get("0").p_end[0], walls.get("0").p_end[1]), (walls.get("0").p_end[0] + walls.get("1").p_end[0] - x_center, walls.get("0").p_end[1] + walls.get("1").p_end[1] - y_center))})
    walls.update({"3" : Wall((walls.get("1").p_end[0], walls.get("1").p_end[1]), (walls.get("0").p_end[0] + walls.get("1").p_end[0] - x_center, walls.get("0").p_end[1] + walls.get("1").p_end[1] - y_center))})
    dt = 3
    screen.fill("black")
    frameTime = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif event.type ==pygame.MOUSEMOTION:
            theta = pygame.mouse.get_pos()[1] / 100

    pygame.draw.circle(screen, 'red', (x, y), 10)

    for i in range(4):
        i = str(i)
        pygame.draw.line(screen, 'green', walls.get(i).p_start, walls.get(i).p_end, 5)

    pygame.display.update()
    clock.tick(60)