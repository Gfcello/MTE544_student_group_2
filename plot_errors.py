import matplotlib.pyplot as plt
from utilities import FileReader

def plot_errors(files):

    # Plot only one robotPose.csv file
    if (len(files) == 1):
        filename = files[0]
        headers, values=FileReader(filename).read_file()
        
        time_list=[]
    
        first_stamp=values[0][-1]

        for val in values:
            time_list.append(val[-1] - first_stamp)

        # Isolate x and y poses of robot from data
        x = [lin[0] for lin in values]
        y = [lin[1] for lin in values]

        plt.plot(x, y, label = "Trajectory")

        # Set label for plot title based on heuristic used
        if "man" in filename:
            heuristic = "Manhattan"
        else:
            heuristic = "Euclidian"

    # Plot two robotPose.csv file (both paths for one heuristic)
    elif (len(files) == 2):
        # Everything is the same as the 1 file case, just doubled
        file1, file2 = files
        headers1, values1=FileReader(file1).read_file()
        headers2, values2=FileReader(file2).read_file()

        time_list1=[]
        time_list2=[]
    
        first_stamp1=values1[0][-1]
        first_stamp2=values2[0][-1]

        for val in values1:
            time_list1.append(val[-1] - first_stamp1)

        for val in values2:
            time_list2.append(val[-1] - first_stamp2)

        # Plot image of the map in background
        im = plt.imread('room.pgm')
        fig, ax = plt.subplots()
        # Image dimensions taken by measuring the map in RVIZ and using the offset
        # from the yaml file
        im = ax.imshow(im, extent = [-7.699941, 5.019859, -2.500001 , 5.590559])

        # Isolate x and y poses for each trajectory
        x1 = [lin[0] for lin in values1]
        y1 = [lin[1] for lin in values1]

        x2 = [lin[0] for lin in values2]
        y2 = [lin[1] for lin in values2]

        # Get heuristic label for graph title, assume both files are the same heuristic
        if "man" in file1:
            heuristic = "Manhattan"
        else:
            heuristic = "Euclidian"

        # Add the grid, trajectories, start and goal points to plot
        ax.grid(zorder=-1)
        ax.plot(x1, y1, label = "Goal 1 Trajectory", color="red", zorder=0)
        ax.plot(x2, y2, label = "Goal 2 Trajectory", color="blue", zorder=0)
        ax.scatter(x1[0], y1[0], color="red", label = "Start Point", zorder=1)
        ax.scatter(x1[-1], y1[-1], color="purple", label = "Goal 1", zorder=1)
        ax.scatter(x2[-1], y2[-1], color="blue", label="Goal 2", zorder=1)

    plt.legend()
    plt.title("X vs Y Trajectory Using " + heuristic + " Distance")
    plt.xlabel("X [m]")
    plt.ylabel("Y [m]")

    plt.show()
    
import argparse

if __name__=="__main__":

    ap = argparse.ArgumentParser(description='Make graph')
    ap.add_argument('--files', nargs='+', required=True, help='list of files')

    args = ap.parse_args()

    print('plotting the files', args.files)

    plot_errors(args.files)