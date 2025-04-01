import pymunk
import pygame
import pymunk.pygame_util
import math
import numpy as np

class Environment:
    
    def init(self, draw = False):
        self.drawBool = draw

        self.MIN_POSITION = 0
        self.MAX_POSITION = 80

        self.staticThreshold = 0

        self.center = (400, 465)
        
        self.WIDTH = 800
        self.HEIGHT = 600

        self.fps = 20
        self.dt = 1 / self.fps
        
        self.space = pymunk.Space()
        self.space.gravity = (0, 981)

        # xStart = np.random.uniform(340, 460)
        startPos = (460, 450)

        self.ball = self.addBall(12, 30, startPos, False)
        # self.hej = self.addBall(12, 30, (400, 450), True)

        startDist = self.realDistanceToCenter(startPos[0],startPos[1], self.center[0], self.center[1])
        
        self.steps = np.array([[math.pi],[startDist],[math.pi],[startDist],[math.pi],[startDist]])


        self.plane = self.createRotatingUBox(self.center, 200, 200, 10)
        self.plane.angle = math.pi
        
        if self.drawBool:
            self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
            self.run_flag = True
            self.clock = pygame.time.Clock()

            self.drawOptions = pymunk.pygame_util.DrawOptions(self.window)

    def run(self, action):
        
        # self.tiltCheck()

        self.plane.angle += action
        self.plane.angle = min(self.plane.angle, (math.pi) + (math.pi / 18))
        self.plane.angle = max(self.plane.angle, (math.pi) - (math.pi / 18))

        self.space.step(self.dt)


    def tiltCheck(self):
        tilt_offset = self.plane.angle - math.pi  # deviation from the "neutral" angle
        if abs(tilt_offset) < self.static_threshold:
            v = self.ball.velocity
            floor_dir = pymunk.Vec2d(math.cos(self.plane.angle), math.sin(self.plane.angle))
            proj = v.dot(floor_dir)
            if abs(proj) < 5:
                self.ball.velocity = v - proj * floor_dir

    def runDraw(self, action):
        self.run(action)

        self.draw()
        self.clock.tick(self.fps)

    def draw(self):
        self.window.fill("white")
        self.space.debug_draw(self.drawOptions)
        pygame.display.update()

    def addBall(self, r, m, pos, static = False):
        if static: body = pymunk.Body(body_type=pymunk.Body.STATIC)
        else: body = pymunk.Body()

        body.position = pos

        shape = pymunk.Circle(body, r)
        shape.mass = m
        shape.elasticity = 0.1
        shape.friction = 0.4
        shape.color = (255, 0, 0, 100)
        self.space.add(body, shape)
        return body
    
    def createRotatingUBox(self, posistion, width, height, wall_thickness=10):
        w = width
        h = height
        t = wall_thickness

        floor_verts = [(-w/2, -t), (w/2, -t), (w/2, 0), (-w/2, 0)]
        left_verts = [(-w/2, 0), (-w/2 + t, 0), (-w/2 + t, h), (-w/2, h)]
        right_verts = [(w/2 - t, 0), (w/2, 0), (w/2, h), (w/2 - t, h)]

        body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        body.position = posistion

        floor_shape = pymunk.Poly(body, floor_verts)
        left_shape = pymunk.Poly(body, left_verts)
        right_shape = pymunk.Poly(body, right_verts)

        for shape in (floor_shape, left_shape, right_shape):
            shape.elasticity = 0.8
            shape.friction = 0.5

        self.space.add(body, floor_shape, left_shape, right_shape)
        return body
    
    def normalizeDist(self, value):
        return (value - self.MIN_POSITION) / (self.MAX_POSITION - self.MIN_POSITION)
        
    def realDistanceToCenter(self, ballX, ballY, floorX, floorY):
        distance = math.sqrt(pow((ballX - floorX), 2) + pow((ballY - floorY), 2))
        nDist = self.normalizeDist(distance)
        
        if(nDist < 0 or nDist > 1): print("INVALID: ", nDist, " must be within bounds [0, 1]")
        return nDist
    
    # def realDistanceToCenter(self):
    #     distance = math.sqrt(pow((self.ball.position[0] - self.center[0]), 2) + pow((self.ball.position[1] - self.center[1]), 2))

    #     normalDist = (distance - self.MIN_POSITION) / (self.MAX_POSITION - self.MIN_POSITION) 
    #     return normalDist


    def stop(self):
        pygame.quit()
        
# env = Environment()
# env.init(True)

# while True:
#     env.runDraw()