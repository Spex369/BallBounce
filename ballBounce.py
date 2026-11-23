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
ball = False

squareTheta = math.pi/2 # under pi/2 and over -pi/2 non inclusive
halfDiagSquare = 250

dt = 0.5

p1 = (WIDTH//2 + halfDiagSquare*math.cos(squareTheta), HEIGHT//2 - halfDiagSquare*math.sin(squareTheta))
p2 = (WIDTH//2 + halfDiagSquare*math.cos(squareTheta+math.pi/2), HEIGHT//2 - halfDiagSquare*math.sin(squareTheta+math.pi/2))
p3 = (WIDTH//2 + halfDiagSquare*math.cos(squareTheta+math.pi), HEIGHT//2 - halfDiagSquare*math.sin(squareTheta+math.pi))
p4 = (WIDTH//2 + halfDiagSquare*math.cos(squareTheta+3*math.pi/2), HEIGHT//2 - halfDiagSquare*math.sin(squareTheta+3*math.pi/2))


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
# Main -----------------------------------------------------------------------------------

walls = {1: wall(p1, p2), 2: wall(p2, p3), 3: wall(p3, p4), 4:wall(p4, p1)}

while True:
    screen.fill("black")
    frameTime = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not ball:
                r = (pygame.mouse.get_pos())
                theta = random.uniform(-math.pi, math.pi)
                v = [10*math.cos(theta), -10*math.sin(theta)]
                ball = True
            else:
                mid = pygame.math.Vector2(pygame.mouse.get_pos())
                theta = random.uniform(-math.pi, math.pi)
                halfWall = pygame.math.Vector2(50*math.cos(theta), -50*math.sin(theta))
                walls.update({len(walls)+1: wall(mid - halfWall, mid + halfWall)})

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
