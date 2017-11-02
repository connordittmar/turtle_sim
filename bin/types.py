from math import sqrt, atan2

class InputKeys(object):
    def __init__(self):
        self.w = "U"
        self.a = "U"
        self.s = "U"
        self.d = "U"

class Vector(object):
    def __init__(self,x,y):
        self.x = float(x)
        self.y = float(y)

    def __str__(self):
        return str((self.x,self.y))

    def difference(self,pos1,pos2):
        self.x = pos1.x - pos2.x
        self.y = pos1.y - pos2.y
        return self

    def subtract(self,pos2):
        self.x = self.x - pos2.x
        self.y = self.y - pos2.y
        return self

    def dot(self,v2):
        self.x = self.x * v2.x
        self.y = self.y * v2.y
        return self

    def scale(self,scale_factor):
        self.x = self.x * scale_factor
        self.y = self.y * scale_factor
        return self

    def magnitude(self):
        magnitude = sqrt(self.x**2 + self.y**2)
        return magnitude

    def direction(self):
        direction = atan2(self.y,self.x)
        return direction

    def aslist(self):
        return [self.x,self.y]


class Ship(object):

    def __init__(self,bu=.8,bv=.5,br=0.07,mass=1.29,j=0.1161,z=0.1):
        self.uv_ddot = [0,0]
        self.uv_dot = [0,0]
        self.vel = [0,0]
        self.pos = [10,5]
        self.theta_ddot = 0.0
        self.theta_dot = 0.0
        self.theta = 2.0
        self.old_uv_dot = [0,0]
        self.old_pos = self.pos
        self.old_theta_dot = 0.0
        self.old_theta = 2.0
        self.force = [0.0,0.0]
        self.bu = bu
        self.bv = bv
        self.br = br
        self.mass = mass
        self.j = j
        self.z = z

    def sim_state(self,physics,dt):
        self.theta_dot = physics.get_ang_velocity(self.theta_ddot,self.old_theta_dot,dt)
        self.theta = physics.get_ang_position(self.theta_dot,self.old_theta,dt)
        self.uv_dot = physics.get_velocity_local(self.uv_ddot,self.old_uv_dot,dt)
        self.vel = physics.get_velocity(self.theta,self.uv_dot)
        self.pos = physics.get_position(self.vel,self.old_pos,dt)
        self.old_theta_dot = self.theta_dot
        self.old_theta = self.theta
        self.old_uv_dot = self.uv_dot
        self.old_pos = self.pos
