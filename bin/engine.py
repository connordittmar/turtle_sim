
import sys, os
import pygame
import math
import time
import numpy as np
from math import atan2, cos, sin, pi
from pygame.locals import *
from pygame.color import THECOLORS
from types import Vector, Ship, InputKeys
from physics import Physics, SurfaceDynamics
from udp_helper import UDPComms
from concurrent.futures import ThreadPoolExecutor
import threading

class Engine(object):
    def __init__(self,workers=8):
        self.executor = ThreadPoolExecutor(max_workers=workers)

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
        udphandler = UDPComms(remoteport=8000,localport=8001)
        i = 0
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
                pwms = [0.6,0.6]
            elif keys.s == 'D':
                pwms = [-0.6,-0.6]
            elif keys.a == 'D':
                pwms = [-0.6,0.6]
            elif keys.d == 'D':
                pwms = [0.6,-0.6]
            else:
                pwms = [0.0,0.0]

                packet = self.executor.submit(udphandler.receive)
                try:
                    returned = packet.result()
                    pwms = returned.split('$')[1].split('!')[0].split(',')
                except Exception as exc:
                    pass
            asv.force = [physics.pwm_to_force(float(pwms[0]),'left'),physics.pwm_to_force(float(pwms[1]),'right')]
            if i ==20:
                print asv.pos
                i =0
            i += 1
            # Run Physics Loop
            asv_dynamics.update_accelerations(asv) #updates asv.uv_ddot and asv.theta_ddot
            asv.sim_state(physics,dt_s) #integrates other vehicle states

            vehicle_state = "${0},{1},{2},{3}".format(str(asv.pos[0]),str(asv.pos[1]),str(round(asv.theta*180.0/pi,3)),str(time.time()))
            self.executor.submit(udphandler.send(vehicle_state))
            # Case for wall bounce (note: add to phyics class)
            scale = 40
            wps = np.array([[10,10],[10,15],[15,15],[15,10]])
            wps = wps*scale
            pygame.draw.polygon(display_surface, THECOLORS["green"],wps.tolist(),5)
            pygame.draw.circle(display_surface, THECOLORS["red"], [int(scale*asv.pos[0]),int(scale*asv.pos[1])], 20, 1)
            offset = [int(scale*asv.pos[0] + 20*cos(asv.theta)), int(scale*asv.pos[1] + 20*sin(asv.theta))]
            pygame.draw.circle(display_surface, THECOLORS["blue"], offset, 2,0)
            #pygame.draw.circle(display_surface, planet.color, [planet.pos.x,planet.pos.y], planet.radius,1)
            time_s += dt_s

            pygame.display.flip()
