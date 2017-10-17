
import sys, os
import pygame
import math

from math import atan2, cos, sin
from pygame.locals import *
from pygame.color import THECOLORS
from types import Vector, Ship, InputKeys
from physics import Physics, SurfaceDynamics

class Engine(object):
    def __init__(self):
        pass

    def play(self):
        pygame.init()
        dims = [640,640]
        display_surface = pygame.display.set_mode((dims[0],dims[1]))
        display_surface.fill(THECOLORS["white"])
        gameclock = pygame.time.Clock()
        framerate_limit = 120
        time_s = 0.0
        keys = InputKeys()
        user_done = False
        asv = Ship()
        physics = Physics()
        asv_dynamics = SurfaceDynamics()
        while not user_done:

            #Get User Input
            display_surface.fill(THECOLORS["white"])
            dt_s = float(gameclock.tick(framerate_limit) * 1e-3)
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    user_done = True

                elif (event.type == pygame.KEYDOWN):
                    if (event.key == K_ESCAPE):
                        user_done = True
                    elif (event.key==K_w):
                        keys.w = 'D'
                    elif (event.key==K_a):
                        keys.a = 'D'
                    elif (event.key==K_s):
                        keys.s = 'D'
                    elif (event.key==K_d):
                        keys.d = 'D'

                elif (event.type == pygame.KEYUP):
                    if (event.key==K_w):
                        keys.w = 'U'
                    elif (event.key==K_a):
                        keys.a = 'U'
                    elif (event.key==K_s):
                        keys.s = 'U'
                    elif (event.key==K_d):
                        keys.d = 'U'

            # If keys are down, input control commands
            if keys.w == 'D':
                asv.force = [1.0,1.0]
            elif keys.s == 'D':
                asv.force = [-1.0,-1.0]
            elif keys.a == 'D':
                asv.force = [-1.0,1.0]
            elif keys.d == 'D':
                asv.force = [1.0,-1.0]
            else:
                asv.force = [0.0,0.0]

            # Run Physics Loop
            asv_dynamics.update_accelerations(asv) #updates asv.uv_ddot and asv.theta_ddot
            asv.sim_state(physics,dt_s) #integrates other vehicle states
            print time_s,dt_s,  asv.uv_ddot, asv.uv_dot

            # Case for wall bounce (note: add to phyics class)

            pygame.draw.circle(display_surface, THECOLORS["red"], [40+int(4*asv.pos[0]),40+int(4*asv.pos[1])], 20, 1)
            offset = [40+int(4*asv.pos[0] + 20*cos(asv.theta)), 40+int(4*asv.pos[1] + 20*sin(asv.theta))]
            pygame.draw.circle(display_surface, THECOLORS["blue"], offset, 2,0)
            #pygame.draw.circle(display_surface, planet.color, [planet.pos.x,planet.pos.y], planet.radius,1)
            time_s += dt_s

            pygame.display.flip()
