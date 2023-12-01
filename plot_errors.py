import matplotlib.pyplot as plt
from utilities import FileReader




def plot_errors(filename):
    
    headers, values=FileReader(filename).read_file()
    
    time_list=[]
    
    first_stamp=values[0][-1]
    
    for val in values:
        time_list.append(val[-1] - first_stamp)

    
    
    fig = plt.subplot(2,1, 1)


    plt.plot([lin[len(headers) - 3] for lin in values], [lin[len(headers) - 2] for lin in values])
    fig.set_title("X vs Y Trajectory")
    fig.set_xlabel("X [m]")
    fig.set_ylabel("Y [m]")
    fig.grid()

    figx = plt.subplot(2,2,3)
    
    figx.set_title("each individual x state")
    for i in range(0, len(headers) - 1):
        if (i % 2 == 0):
            plt.plot(time_list, [lin[i] for lin in values], label= headers[i])

    figx.legend()
    figx.set_xlabel("Time [nS]")
    figx.set_ylabel("Value")
    figx.grid()

    figy = plt.subplot(2,2,4)
    
    figy.set_title("each individual y state")
    for i in range(0, len(headers) - 1):
        if (i % 2 != 0):
            plt.plot(time_list, [lin[i] for lin in values], label= headers[i])

    figy.legend()
    figy.set_xlabel("Time [nS]")
    figy.set_ylabel("Value")
    figy.grid()

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


