import sys
import matplotlib.pyplot as plt
import numpy as np

def cellular_usage_1(title, x_name, y_name, data):
    min_cost = [0, 0, 0]
    min_delay = [50, 98, 125]
    proposed = [29, 29, 30]
    MDP = [45, 70, 110]
    plot(title, x_name, y_name, data, min_cost, min_delay, proposed, MDP)
    plt.savefig("result/1_cellular_usage.png", bbox_inches='tight', dpi=600, pad_inches=0.1)
    
def finished_time_2(title, x_name, y_name, data):
    min_cost = [139, 343, 643]
    min_delay = [50, 99, 125]
    proposed = [103, 173, 402]
    MDP = [125, 185, 460]
    plot(title, x_name, y_name, data, min_cost, min_delay, proposed, MDP)
    plt.savefig("result/2_finished_time.png", bbox_inches='tight', dpi=600, pad_inches=0.1)


# Cellular Usage Change Data Rate
def cellular_usage_3(title, x_name, y_name, data):
    min_cost = [0, 0, 0, 0, 0]
    min_delay = [50, 75, 90, 100, 100]
    proposed = [29, 50, 51, 52, 50]
    MDP = [45, 45, 60, 85, 80]
    plot(title, x_name, y_name, data, min_cost, min_delay, proposed, MDP)
    plt.savefig("result/3_cellular_usage.png", bbox_inches='tight', dpi=600, pad_inches=0.1)

# Finished Time
def finished_time_4(title, x_name, y_name, data):
    min_cost = [139, 139, 139, 139, 139]
    min_delay = [50, 38, 31, 25, 20]
    proposed = [103, 46, 46, 46, 46]
    MDP = [125, 115, 110, 70, 85]
    plot(title, x_name, y_name, data, min_cost, min_delay, proposed, MDP)
    plt.savefig("result/4_finished_time.png", bbox_inches='tight', dpi=600, pad_inches=0.1)

def plot(title, x_name, y_name, data, min_cost, min_delay, proposed, MDP):
    plt.title(title, fontweight = "bold", fontsize=16)
    plt.xlabel(x_name, fontsize=16)
    plt.ylabel(y_name, fontsize=16)
    plt.xticks(data, fontsize=16)
    plt.plot(data, min_delay, marker='.', label = "min_delay")
    plt.plot(data, min_cost, marker='.', label = "min_cost")
    plt.plot(data, proposed, marker='.', label = "proposed")
    plt.plot(data, MDP, marker='.', label = "MDP")
    plt.legend(labels=["Minimal delay", "Minimal cost", "Without V2V", "MDP"], loc = 'best')

if __name__ == '__main__':
    data_size = [100, 150, 200]
    data_rate = [1, 2, 3, 4, 5]

    if sys.argv[1] == '1':
        cellular_usage_1("Cellular Usage", "Data Size (MB)", "Usage (MB)", data_size)
    elif sys.argv[1] == '2':
        finished_time_2("Finished Time", "Data Size (MB)", "Finished Time (s)", data_size)
    elif sys.argv[1] == '3':
        cellular_usage_3("Cellular Usage", "Cellular Data Rate (MB/s)", "Usage (MB)", data_rate)
    elif sys.argv[1] == '4':
        finished_time_4("Finished Time", "Cellular Data Rate (MB/s)", "Finished Time (s)", data_rate)
