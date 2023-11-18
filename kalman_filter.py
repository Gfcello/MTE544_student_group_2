
import numpy as np



# TODO Part 3: Comment the code explaining each part
class kalman_filter:
    
    # TODO Part 3: Initialize the covariances and the states    
    def __init__(self, P, Q, R, x, dt):
        # Set all values to the values passed into the init function
        self.P=P
        self.Q=Q
        self.R=R
        self.x=x
        self.dt=dt
        
    # TODO Part 3: Replace the matrices with Jacobians where needed        
    def predict(self):

        # For an EKF, these have to be Jacobian Matrices
        self.A = self.jacobian_A() # State matrix
        self.C = self.jacobian_H() # Mape state to observation
        
        self.motion_model()
        
        self.P= np.dot( np.dot(self.A, self.P), self.A.T) + self.Q

    # TODO Part 3: Replace the matrices with Jacobians where needed
    def update(self, z):

        S=np.dot(np.dot(self.C, self.P), self.C.T) + self.R
            
        kalman_gain=np.dot(np.dot(self.P, self.C.T), np.linalg.inv(S))
        
        surprise_error= z - self.measurement_model()
        
        self.x=self.x + np.dot(kalman_gain, surprise_error)
        self.P=np.dot( (np.eye(self.A.shape[0]) - np.dot(kalman_gain, self.C)) , self.P)
        
    
    # TODO Part 3: Implement here the measurement model
    def measurement_model(self):
        x, y, th, w, v, vdot = self.x

        # Theta is always zero because the x axis of the turtle bot is the front of the robot
        th = 0
        
        return np.array([
            v,# v, maps directly to the state v
            w,# w, maps directly to the state w
            vdot*np.cos(th)-v*w*np.sin(th), # ax, accel purely due to linear movement
            vdot*np.sin(th)+v*w*np.cos(th) # ay, accel based on the turning of the robot
        ])

    # TODO Part 3: Implement the motion model (state-transition matrice)
    def motion_model(self):
        x, y, th, w, v, vdot = self.x
        dt = self.dt
        
        self.x = np.array([
            x + v * np.cos(th) * dt, # Multiply by v component * dt for incremental change in distance
            y + v * np.sin(th) * dt, # Multiply by v component * dt for incremental change in distance
            th + w * dt,
            w,
            v  + vdot*dt,
            vdot,
        ])


    
    def jacobian_A(self):
        x, y, th, w, v, vdot = self.x
        dt = self.dt
        
        # Partial derivatives are taken based on the motion_model matrix
        return np.array([
            #x, y,               th, w,             v, vdot
            [1, 0,              -v * np.sin(th) * dt, 0,   np.cos(th) * dt,  0],
            [0, 1,              v * np.cos(th) * dt,  0,   np.sin(th) * dt,  0],
            [0, 0,                1, dt,              0,  0],
            [0, 0,                0, 1,               0,  0],
            [0, 0,                0, 0,               1,  dt],
            [0, 0,                0, 0,               0,  1 ]
        ])
    
    
    # TODO Part 3: Implement here the jacobian of the H matrix (measurements)    
    def jacobian_H(self):
        x, y, th, w, v, vdot=self.x

        # Partial derivatives are taken based on the measurement model matrix
        # Remember that th=0 for the measurement model (hence no theta terms in partial
        # derivatives)
        return np.array([
            #x, y,th, w, v,vdot
            [0, 0, 0, 0, 1, 0], # v
            [0, 0, 0, 1, 0, 0], # w
            [0, 0, 0, 0, 0, 1], # ax
            [0, 0, 0, v, w, 0], # ay
        ])
            
    # TODO Part 3: return the states here
    def get_states(self):
        return self.x # Return the state matrix
