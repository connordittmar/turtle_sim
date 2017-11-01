# Vector Calculations Module
from math import sin, cos, pi
from types import Vector
class Physics(object):

    def __init__(self):
        pass

    def get_position(self,vel2d,pos2d_old,dt):
        position = [pos2d_old[0] + vel2d[0] * dt , pos2d_old[1] +  vel2d[1] * dt]
        return position

    def get_velocity(self,theta,vel2d):
        velocity = [vel2d[0] * cos(theta) - vel2d[1] * sin(theta),vel2d[0] * sin(theta) + vel2d[1] * cos(theta)]
        return velocity

    def get_velocity_local(self,acc2d,uv_dot_old,dt):
        local_velocity = [uv_dot_old[0] + acc2d[0]*dt , uv_dot_old[1] + acc2d[1]*dt]
        return local_velocity

    def get_ang_velocity(self,theta_ddot,theta_dot_old,dt):
        ang_velocity = theta_dot_old + theta_ddot * dt
        return ang_velocity

    def get_ang_position(self,theta_dot,theta_old,dt):
        theta = theta_old + theta_dot * dt
        return theta % (2*pi)

    def pwm_to_force(self,pwm,motor):
        #Takes a PWM and converts to force output equivalent in Newtons
        if pwm < 0.4 and pwm > -0.4:
            force = 0.0
            return force
        if motor == 'left':
            if pwm >= 0.4:
                force = 0.1099*pwm**2 + 1.6363*pwm - 0.4019
                return force
            if pwm <= -0.4:
                force = -1.2637*pwm**2 - 0.528*pwm - 0.215
                return force
        if motor == 'right':
            if pwm >= 0.4:
                force = 1.0989*pwm**2 + 0.286*pwm + 0.0354
                return force
            if pwm <= -0.4:
                force = -1.0989*pwm**2 - 0.5692*pwm - 0.2675
                return force


class SurfaceDynamics(object):
    def __init__(self):
        pass

    def update_accelerations(self,ship):

        ship.uv_ddot[0] = (ship.force[0]+ship.force[1] - ship.uv_dot[0] * ship.bu) / ship.mass
        ship.uv_ddot[1] = - ship.uv_dot[1] * ship.bv / ship.mass
        ship.theta_ddot = (ship.z*(ship.force[0]-ship.force[1]) - ship.theta_dot * ship.br) / ship.j;
