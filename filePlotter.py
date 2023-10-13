# You can use this file to plot the loged sensor data
# Note that you need to modify/adapt it to your own files
# Feel free to make any modifications/additions here

from math import cos, pi, sin
import matplotlib.pyplot as plt
from utilities import FileReader

def plot_errors(filename):
    # Odometry and imu plots
    if "odom" in filename or "imu" in filename:
        headers, values=FileReader(filename).read_file() 

        values = list(map(list, zip(*values)))

        t_start = values[-1][0] # Start time, used to have time start at zero
        t_prev = values[-1][0] # Previous time value, used for rollover checks
        adj = 0 # time adjustment value
        WRAP_TIME = 1e9 # time readings wrap every 1e9 ns
        num_wrapped = 0 # how many times the time readings have wrapped

        # Clean up time readings to account for time valuse wrapping around every second
        for i, t in enumerate(values[-1]):
            t += adj

            # Timer has looped around
            if t < t_prev:
                num_wrapped += 1
                adj = num_wrapped * WRAP_TIME
                t += WRAP_TIME

            # Add good values converted to seconds to values list
            values[-1][i] = (t - t_start) / WRAP_TIME
            t_prev = t

        # Constructing the main plot
        plt.plot(values[-1], values[0], label=headers[0])
        plt.plot(values[-1], values[1], label=headers[1])
        plt.plot(values[-1], values[2], label=headers[2])
        plt.grid()
        plt.legend()
        plt.title("odom data" if "odom" in filename else "imu data")
        plt.xlabel("time (sec)")
        plt.ylabel("pose" if "odom" in filename else "accelerations")
        plt.show()
        
        # plot x vs y trajectory for odom data
        if "odom" in filename:
            plt.plot(values[0], values[1])
            plt.grid()
            plt.title("x vs y trajectory")
            plt.xlabel("x")
            plt.ylabel("y")
            plt.show()

    # TODO: whatever needs to be done for LIDAR
    elif "laser" in filename:
        headers, lines=FileReader(filename).read_lidar_file() 

        # Find the first line in the csv that has the fewest "inf" entries
        full_line_found = False
        row_index = 0
        while not full_line_found:
            row_index += 1 # Skip first line as it is the headings
            # print("Row: ", row_index, " Count: ", lines[row_index].count("inf"))

            # Since there are many inf readings in each row, get row with as few bad readings as possible
            if lines[row_index].count("inf") < 320:
                full_line_found = True
        
        # Looking at outputs want to plot a few rows of readings:
        x_points = [] # at 0 degrees
        y_points = []
        for i in range(5):
            laser_vals = str(lines[row_index]).replace("array('f', [", "").replace("])", "")
            # Note still have to ignore the last value as it is the timestamp
            laser_vals = laser_vals.split(',')
            laser_vals = laser_vals[0:len(laser_vals)-2] # This chops off the timestamp

            # Now should have a single good list of distance readings.
            reading_angle = 0
            reading_angle_increment = 2.0 * pi / len(laser_vals) # As each row is 360deg of readings
            # Make lists to store readging points in reference to the robot
            for reading in laser_vals:
                if reading != "inf":
                    x_points.append(float(reading) * cos(reading_angle))
                    y_points.append(float(reading) * sin(reading_angle))

                reading_angle += reading_angle_increment
            
            row_index += 1
        
        print(len(x_points))

        # plot x vs y laser scan
        plt.plot(y_points, x_points)
        plt.grid()
        if "spiral" in filename:
            plt.title("x vs y Laser Scan Spiral")
        elif "circle" in filename:
            plt.title("x vs y Laser Scan Circle")
        elif "line" in filename:
            plt.title("x vs y Laser Scan Line")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()
        

import argparse

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--files', nargs='+', required=True, help='List of files to process')
    
    args = parser.parse_args()
    
    print("plotting the files", args.files)

    filenames=args.files
    for filename in filenames:
        plot_errors(filename)
