import pymunk             # Import pymunk..
import pygame
import pymunk.pygame_util
import math

WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))

def draw(space, window, drawOptions):
    window.fill("white")
    space.debug_draw(drawOptions)
    pygame.display.update()

def calcDist(p1,p2):
    return math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0]) + (p1[1]-p2[1])*(p1[1]-p2[1]))

def addBall(space, radius, mass):
    body = pymunk.Body()
    body.position = (300,300)
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.elasticity = 1
    shape.friction = 0.4
    shape.color = (255, 0, 0, 100)
    space.add(body, shape)
    return body

def addRect(space, pos, size):
    body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    body.position = pos
    shape = pymunk.Poly.create_box(body, size)
    shape.elasticity = 0.8
    shape.friction = 0.5
    shape.mass = 10
    body.angle = 0
    space.add(body, shape)
    return body


def crateBounderies(space, width, height):
    rects = [
        [(width/2,height - 10), (width, 20)],
        [(width/2, 10), (width, 20)],
        [(10,height/2), (20, height)],
        [(width - 10, height/2), (20, height)],
    ]

    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.8
        shape.friction = 0.5
        space.add(body, shape)

def run(window, WIDTH, HEIGHT):
    run = True
    clock = pygame.time.Clock()
    fps = 120
    dt = 1/fps

    space = pymunk.Space()
    space.gravity = 0,981

    box = addRect(space, (400,400), (400,10))
    
    ball = addBall(space, 30, 10)
    crateBounderies(space, WIDTH, HEIGHT)

    drawOptions = pymunk.pygame_util.DrawOptions(window)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        box.angle += 0.01
        draw(space, window, drawOptions)
        space.step(dt)
        clock.tick(fps)

    pygame.quit()

run(window, WIDTH, HEIGHT)