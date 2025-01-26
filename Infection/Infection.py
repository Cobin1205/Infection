from codecs import xmlcharrefreplace_errors
import pygame
import random
import math

class Ball:
    def __init__(self, x, y, r, speed, infected=False):
        self.x = x
        self.y = y
        self.color = (100, 100, 100)
        self.vel = [random.uniform(-1, 1)*speed, random.uniform(-1, 1)*speed]
        self.r = r
        self.gridPos = tuple()
        self.infected = infected

    #Draw circle and bouce off walls
    def update(self, screen):
        #Move ball
        self.x += self.vel[0]
        self.y += self.vel[1]

        if self.vel[0] + self.vel[1] > speed:
            self.vel[0] /= 2
            self.vel[1] /= 2

        if not self.infected:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

        else:
            pygame.draw.circle(screen, "Green", (self.x, self.y), self.r)

        #Bounce off walls
        if self.x <= self.r:
            self.vel[0] *= -1

        if self.x >= screen.get_width() - self.r:
             self.vel[0] *= -1

        if self.y <= self.r:
            self.vel[1] *= -1

        if self.y >= screen.get_height() - self.r:
            self.vel[1] *= -1

pygame.init()
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()

#Speed multiplier
speed = 0.5
#Ball radii
radius = 5
#Toggle the lines and boxes
visual = False

balls = []

for i in range(1, 75):
    for j in range(1, 40):
        balls.append(Ball(radius*3*i, radius*3*j, radius, speed))

balls[0].infected = True

if visual:
    #Instatiate the boxes
    boxesSurf = [[0 for i in range(screen.get_width()//(radius*2))] for j in range(screen.get_height()//(radius*2))]
    boxesRect = [[0 for i in range(screen.get_width()//(radius*2))] for j in range(screen.get_height()//(radius*2))]

if visual:
    #Create the 2d arrays for the boxes
    for i in range(int(screen.get_height()//(radius*2))):
        for j in range(screen.get_width()//(radius*2)):
            boxesSurf[i][j] = pygame.surface.Surface((radius*2, radius*2))
            boxesSurf[i][j].fill("white")
            boxesRect[i][j] = boxesSurf[i][j].get_rect(topleft=(i*(radius*2), j*(radius*2)))

while True:
    screen.fill("White")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            SystemExit()
            quit()

    #Boxes
    if visual:
        for i in range(len(boxesSurf)):
            for j in range(len(boxesSurf[i])):
                screen.blit(boxesSurf[i][j], boxesRect[i][j])
                boxesSurf[i][j].fill("white")

    shDict = dict()

    #Create the Dictionary of ball locations
    for ball in balls:
        #Get ball location
        ball.gridPos = (int(ball.x // (radius*2)), int(ball.y // (radius*2) ))
        #Key: location. Value: ball
        shDict[ball.gridPos] = ball

    
    for ball in balls:
        x, y = ball.gridPos[0], ball.gridPos[1]
        for loc in ((x-1, y), (x+1, y), (x, y+1), (x, y-1), (x-1, y-1), (x+1, y-1), (x-1, y+1), (x+1, y+1)):
            #if another ball is in adjacent cell
            if loc in shDict:
                otherBall = shDict[loc]
                distance = math.sqrt( (otherBall.x - ball.x)**2 + (otherBall.y - ball.y)**2 )

                #If they're touching
                if distance <= (radius*2):

                    #Infect other ball
                    if ball.infected:
                        otherBall.infected = True
                    elif otherBall.infected:
                        ball.infected = True

                    #Collide
                    impact = [otherBall.x - ball.x, otherBall.y - ball.y]
                    vDiff = (otherBall.vel[0] - ball.vel[0], otherBall.vel[1] - ball.vel[1])

                    #Ball
                    numA = (vDiff[0] * impact[0]) + (vDiff[1] * impact[1])
                    denA = distance*distance
                    deltaV = impact.copy()
                    deltaV[0] *= (numA / denA)
                    deltaV[1] *= (numA / denA)
                    ball.vel[0] += deltaV[0]
                    ball.vel[1] += deltaV[1]


                    #Other Ball
                    numB = (vDiff[0] * impact[0]) + (vDiff[1] * impact[1])
                    denB = distance*distance
                    deltaVB = impact.copy()
                    deltaVB[0] *= -(numB / denB)
                    deltaVB[1] *= -(numB / denB)
                    otherBall.vel[0] += deltaVB[0]
                    otherBall.vel[1] += deltaVB[1]

                    shDict.pop(loc)



                        

        ball.update(screen)

    if visual:
        #Vertical Lines
        for i in range(screen.get_width()//(radius*2)):
            pygame.draw.line(screen, "Gray", (i*(radius*2), 0), (i*(radius*2), screen.get_height()), 1)

        #Horizontal Lines
        for i in range(screen.get_height()//(radius*2)):
            pygame.draw.line(screen, "Gray", (0, i*(radius*2)), (screen.get_width(), i*(radius*2)), 1)
    
        #Color boxes
        for x in shDict:
            #The box the circle's center is in
            boxesSurf[x[0]][x[1]].fill("Red")

            #Top Left Bottom Right
            if x[0] > 0: boxesSurf[x[0]-1][x[1]].fill("Green") #Left
            if x[0] < len(boxesSurf[0]) - 1: boxesSurf[x[0]+1][x[1]].fill("Green") #Right
            if x[1] > 0: boxesSurf[x[0]][x[1]-1].fill("Green") #Top
            if x[1] < len(boxesSurf) - 1: boxesSurf[x[0]][x[1]+1].fill("Green") #Bottom

            #Corners
            if x[0] > 0 and x[1] > 0: boxesSurf[x[0]-1][x[1]-1].fill("Green") #Top Left
            if x[0] < len(boxesSurf[0]) - 1 and x[1] > 0: boxesSurf[x[0]+1][x[1]-1].fill("Green") #Top Right
            if x[1] < len(boxesSurf) - 1 and x[0] > 0: boxesSurf[x[0]-1][x[1]+1].fill("Green") #Bottom Left
            if x[1] < len(boxesSurf) - 1 and x[0] < len(boxesSurf[0]) - 1: boxesSurf[x[0]+1][x[1]+1].fill("Green") #Botom Right

    pygame.display.update()
    #clock.tick(120)