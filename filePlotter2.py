#0.008714509196579456 is the lidar angle step ish
# goes from -pi to +pi

import matplotlib.pyplot as plt
from utilities import FileReader

# Plot Line
line_odom = "odom_content_line.csv"
line_imu = "imu_content_line.csv"
line_laser = "laser_content_line.csv"

headers, vals = FileReader.readfile(line_odom)

# Plot Circle
circ_odom = "odom_content_circle.csv"
circ_imu = "imu_content_circle.csv"
circ_laser = "laser_content_circle.csv"

# Plot Spiral
spiral_odom = "odom_content_spiral.csv"
spiral_imu = "imu_content_spiral.csv"
spiral_laser = "laser_content_spiral.csv"