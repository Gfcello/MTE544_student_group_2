# You can use this file to plot the loged sensor data
# Note that you need to modify/adapt it to your own files
# Feel free to make any modifications/additions here

import matplotlib.pyplot as plt
from utilities import FileReader

def plot_errors(filename):
    headers, values=FileReader(filename).read_file() 

    # Odometry and imu plots
    if "odom" or "imu" in filename:
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
        pass

import argparse

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--files', nargs='+', required=True, help='List of files to process')
    
    args = parser.parse_args()
    
    print("plotting the files", args.files)

    filenames=args.files
    for filename in filenames:
        plot_errors(filename)
