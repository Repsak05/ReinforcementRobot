import numpy as np
from neuralnet import NeuralNetwork
from Envrioment import Environment
import math
import pygame
import pymunk

MIN_POSITION = 0
MAX_POSITION = 80
ANGLE_SPEED = 0.01

bestLayers = []
bestBiases = []
for i in range(3):
    bestLayers.append(np.load(f'layers/bestLayer{i}.npy', allow_pickle=True))
    bestBiases.append(np.load(f'biases/bestBiases{i}.npy', allow_pickle=True))

print(bestLayers)

bestAgent = NeuralNetwork()
bestAgent.init(bestLayers, bestBiases, 0, 0)

def realDistanceToCenter(ballX, ballY, floorX, floorY):
    distance = math.sqrt(pow((ballX - floorX), 2) + pow((ballY - floorY), 2))
    # distance = math.sqrt(pow(ballX - floorX, 2))
    #Normalize distance
    normalDist = (distance - MIN_POSITION) / (MAX_POSITION - MIN_POSITION) 
    # print(ballX)
    # print(normalDist, " [0, 1]")
    return normalDist

# print(bestAgent.calcOutput(np.matrix([[0.4],[0.8]])))


WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))

def getDistanceToCenter(placement): #placement [0, 1]
    center = 0.5
    return abs(placement - center)

def draw(space, window, drawOptions):
    window.fill("white")
    space.debug_draw(drawOptions)
    pygame.display.update()

def calcCentroid(W, H, t):
    A_floor = W * t
    A_wall = t * H
    A_total = A_floor + 2 * A_wall
    y_floor = -t / 2
    y_wall = H / 2
    return (A_floor * y_floor + 2 * A_wall * y_wall) / A_total

def createRotatingUBox(space, center, width, height, wall_thickness=10):
    #Create U-shaped box
    W = width
    H = height
    t = wall_thickness

    y_centroid = calcCentroid(W, H, t)
    offset_y = 0

    # U shaped egdes
    floor_verts = [(-W/2, -t), (W/2, -t), (W/2, 0), (-W/2, 0)]
    left_verts = [(-W/2, 0), (-W/2 + t, 0), (-W/2 + t, H), (-W/2, H)]
    right_verts = [(W/2 - t, 0), (W/2, 0), (W/2, H), (W/2 - t, H)]

    def shift(verts, offset_y):
        return [(x, y - offset_y) for x, y in verts]

    floor_verts = shift(floor_verts, offset_y)
    left_verts = shift(left_verts, offset_y)
    right_verts = shift(right_verts, offset_y)

    # Create one kinematic body that will rotate about its center of mass.
    body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    body.position = center

    # Create shapes.
    floor_shape = pymunk.Poly(body, floor_verts)
    left_shape = pymunk.Poly(body, left_verts)
    right_shape = pymunk.Poly(body, right_verts)

    for shape in (floor_shape, left_shape, right_shape):
        shape.elasticity = 0.8
        shape.friction = 0.5

    space.add(body, floor_shape, left_shape, right_shape)
    return body

def addBall(space, radius, mass):
    # body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body = pymunk.Body()

    # body.position = (400, 450)
    body.position = (370, 450)

    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.elasticity = 0.1
    shape.friction = 0.4
    shape.color = (255, 0, 0, 100)
    space.add(body, shape)
    return body

def crateBounderies(space, width, height):
    rects = [
        [(width/2, height - 10), (width, 20)],
        [(width/2, 10), (width, 20)],
        [(10, height/2), (20, height)],
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
    run_flag = True
    clock = pygame.time.Clock()
    fps = 20
    dt = 1 / fps

    space = pymunk.Space()
    space.gravity = (0, 981)

    # Create a rotating U-shaped box.
    W = 200    # width of the U-box
    H = 200    # height of the side walls
    t = 10     # wall thickness
    box = createRotatingUBox(space, (400, 465), W, H, wall_thickness=t)
    ball_radius = 12
    ball = addBall(space, ball_radius, 30)
    
    crateBounderies(space, WIDTH, HEIGHT)
    drawOptions = pymunk.pygame_util.DrawOptions(window)

    box.angle = math.pi
    # angleSpeed = 0.003
    static_threshold = 0 # 0.122  #(about 7 degrees)

    # Pre-calculate the local coordinate for the bottom point of the left wall.
    # offset_y = calcCentroid(W, H, t)
    # left_bottom_local = (-W/2, 0 - offset_y)

    itera = 0
    while run_flag:
        # Rotate the U-shaped box within set limits.
        # if box.angle >= math.pi + math.pi/6:
        #     angleSpeed *= -1
        # if box.angle <= math.pi - math.pi/6:
        #     angleSpeed *= -1
        # box.angle += angleSpeed        

        # --- Static friction simulation for the ball ---

        # left_bottom_world = box.local_to_world(left_bottom_local)
        # ball_pos = ball.position
        # dist = math.sqrt((ball_pos[0] - left_bottom_world[0])**2 +
        #                 (ball_pos[1] - left_bottom_world[1])**2)
        # gap = dist - ball_radius
        # dist = (gap - MIN_POSITION) / (MAX_POSITION - MIN_POSITION) 

        tilt_offset = box.angle - math.pi  # deviation from the "neutral" angle
        if abs(tilt_offset) < static_threshold:
            v = ball.velocity
            floor_dir = pymunk.Vec2d(math.cos(box.angle), math.sin(box.angle))
            proj = v.dot(floor_dir)
            if abs(proj) < 5:
                ball.velocity = v - proj * floor_dir
        # --- End static friction simulation ---

        # Calculate the distance from the ball's center to the bottom point of the left wall.
        # left_bottom_world = box.local_to_world(left_bottom_local)
        # ball_pos = ball.position
        # dist = math.sqrt((ball_pos[0] - left_bottom_world[0])**2 +
                        #  (ball_pos[1] - left_bottom_world[1])**2)
        # gap = dist - ball_radius

        # print([[box.angle/(2*math.pi)],[gap/170]])
        # print((np.argmax(bestAgent.calcOutput(np.matrix([[box.angle/(2*math.pi)],[gap/170]]))) - 1))
       
        # UDKOMMENTER
        # box.angle += (np.argmax(bestAgent.calcOutput(np.matrix([[box.angle/(2*math.pi)],[gap/170]]))) - 1) * 0.003
        
        dist = realDistanceToCenter(ball.position[0], ball.position[1], 400, 450)
        angle = (box.angle - ((math.pi) - (math.pi / 18))) / (((math.pi) + (math.pi / 18)) - ((math.pi) - (math.pi / 18)))
        print(angle)
        retning = np.argmax(bestAgent.calcOutput(np.matrix([[angle],[dist]]))) - 1
        action = retning * bestAgent.calcOutput(np.matrix([[angle],[dist]]))[retning + 1, 0] * ANGLE_SPEED
        
        box.angle += action

        box.angle = min(box.angle, (math.pi) + (math.pi / 18))
        box.angle = max(box.angle, (math.pi) - (math.pi / 18))
        # print("after", box.angle)
        
        # # print("Distance from ball center to vertex:", dist)
        # print("Gap from ball surface to bottom point of left edge:", gap)
        # dist = (gap - MIN_POSITION) / (MAX_POSITION - MIN_POSITION) 
        # print(dist)
        itera += 1
        draw(space, window, drawOptions)
        space.step(dt)
        clock.tick(fps)
        # if (itera == 50):
        #     print("Dist:", getDistanceToCenter(dist))
        #     print("Pos:", ball.position)
        #     hej = input("Wait")

    pygame.quit()

run(window, WIDTH, HEIGHT)