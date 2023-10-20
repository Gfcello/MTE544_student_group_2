import numpy as np

# Type of planner
POINT_PLANNER=0; TRAJECTORY_PLANNER=1

# Trajectory types
QUADRATIC_PATH=0; SIGMA_PATH=1


class planner:
    def __init__(self, type_):

        self.type=type_

    
    def plan(self, goalPoint=[-1.0, -1.0, 0.0]):
        
        if self.type==POINT_PLANNER:
            return self.point_planner(goalPoint)
        
        elif self.type==TRAJECTORY_PLANNER:
            return self.trajectory_planner(traj_type)


    def point_planner(self, goalPoint):
        x = goalPoint[0]
        y = goalPoint[1]
        theta = goalPoint[2]
        return x, y, theta

    # TODO Part 6: Implement the trajectories here
    def trajectory_planner(self, traj_type):
        timeseries = np.linspace(0, 10, 1000) # 6000 points at 100Hz
        trajectory = []
        if traj_type == QUADRATIC_PATH:
            for time in timeseries:
                trajectory.append([time, time ** 2, np.arctan2((time ** 2 - trajectory[-1][1]) / (time - trajectory[-1][0]))])
        elif traj_type == SIGMA_PATH:
            for time in timeseries:
                trajectory.append([time, 1/(1+np.exp(-time)), np.arctan2((1/(1+np.exp(-time)) - trajectory[-1][1]) / (time - trajectory[-1][0]))])
        return trajectory

