import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 512, 512
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
r = [WIDTH//2, HEIGHT//2]
v = [0, 0]
radius = 10
theta = 0

squareTheta = math.pi/2 # under pi/2 and over -pi/2 non inclusive
dt = 0.5

walls = {}

# Classes --------------------------------------------------------------------------------

class wall:
    def __init__(self, start, end):
        self.start = pygame.math.Vector2(start)
        self.end = pygame.math.Vector2(end)
        self.WallVector =  (self.end - self.start)
        self.length = self.WallVector.length()
        self.WallVector = self.WallVector.normalize()
        self.normal = pygame.math.Vector2(-self.WallVector.y, self.WallVector.x).normalize()


# Subprogram -----------------------------------------------------------------------------

def dot(pointX, pointY, vecX, vecY):
    return pointX*vecX + pointY*vecY

def createWalls():
    n = random.randint(3, 20)
    points = []

    for i in range(n):
        r = random.randint(100, WIDTH//2)
        thisPoint = (WIDTH//2 + r*math.cos(squareTheta+2*i*math.pi/n), HEIGHT//2 - r*math.sin(squareTheta+2*i*math.pi/n))
        while thisPoint in points:
            thisPoint = (WIDTH//2 + r*math.cos(squareTheta+2*i*math.pi/n), HEIGHT//2 - r*math.sin(squareTheta+2*i*math.pi/n))
        points.append(thisPoint)

    for i in range(1, len(points)):
        walls.update({i: wall(points[i - 1], points[i])})
    walls.update({len(points): wall(points[-1], points[0])})

    
# Main -----------------------------------------------------------------------------------

createWalls()

while True:
    screen.fill("black")
    frameTime = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            r = (pygame.mouse.get_pos())
            theta = random.uniform(-math.pi, math.pi)
            v = [10*math.cos(theta), -10*math.sin(theta)]

    r = [r[0] + dt*v[0], r[1] + dt*v[1]]

    pygame.draw.circle(screen, 'white', r, radius)

    for i in walls:
        currentWall = walls.get(i)

        pygame.draw.line(screen, "white", currentWall.start, currentWall.end)

        vectorToBall = pygame.math.Vector2(r)-currentWall.start
        projection = max(0, min(dot(vectorToBall.x, vectorToBall.y, currentWall.WallVector.x, currentWall.WallVector.y), currentWall.length)) # clamping, did that for cool graphic representation earlier in the project, otherwise useless if it all works.
        contact = currentWall.start + currentWall.WallVector * projection # projection is how far up the wall the contact is. Hence start + direction*distance = contact.

        distance = (r - contact).length()

        # credits to Zanzlanz; not my code --------------------------------------------------------
        if distance < radius:
            magVNormal = dot(v[0], v[1], currentWall.normal.x, currentWall.normal.y)
            magVTangent = dot(v[0], v[1], currentWall.WallVector.x, currentWall.WallVector.y)

            v[0] = -(magVNormal * currentWall.normal.x) + (magVTangent * currentWall.normal.y)
            v[1] = -(magVNormal * currentWall.normal.y) + (magVTangent * -currentWall.normal.x)
        # credits to Zanzlanz; not my code --------------------------------------------------------
        # Check out Zanzlanz's yt channel @zanzlanz

    pygame.display.update()
    clock.tick(60)

# Added features: 
#  - Removed redundant code
#  - Handle velocitties, walls and positions using vectors
#  - random wall addition upon mouse clicking
