import matplotlib.pyplot as plt
from utilities import FileReader


def plot_errors(filename):
    
    headers, values=FileReader(filename).read_file()

    time_list=[]

    first_stamp=values[0][-1]

    for val in values:
        time_list.append(val[-1] - first_stamp)

    fig, axes = plt.subplots(1,2, figsize=(14,6))

    axes[0].plot([lin[0] for lin in values], [lin[1] for lin in values])
    axes[0].set_title("x vs y" if "pose" in filename else "e vs e_dot")
    axes[0].set_xlabel("x" if "pose" in filename else "e")
    axes[0].set_ylabel("y" if "pose" in filename else "e_dot")
    axes[0].grid()

    axes[1].set_title("x, y, theta vs time" if "pose" in filename else "e, e_dot, e_int vs time")
    axes[1].set_xlabel("time [nsec]")
    axes[1].set_ylabel("x/y/theta" if "pose" in filename else "e/e_dot/e_int")
    for i in range(0, len(headers) - 1):
        axes[1].plot(time_list, [lin[i] for lin in values], label= headers[i]+ (" linear" if "linear" in filename else " angular"))

    axes[1].legend()
    axes[1].grid()

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
