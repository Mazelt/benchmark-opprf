import numpy as np
import matplotlib.pyplot as plt
import os.path
import glob
import json
import argparse


batch_name = "ScalingElementsDA_2"

def load_batch(pattern):
    os.path.exists('./batchlogs/experiments')
    files = glob.glob(f"./batchlogs/experiments/Batch-{pattern}*.json")
    files = sorted(files)
    for i,e in enumerate(files):
        print(f"{i}:\t {e}")
    all_right = input('Take all? Press any key to continue')
    batches = []
    for f in files:
        with open(f, 'r') as fp:
            b = json.load(fp)
            for batch in batches:
                if batch['parameters'] == b['parameters']:
                    batch[b['repeat']] = {
                        's_output': b['s_output'], 'c_output': b['c_output']}
                    b = 0
                    break
            if b:
                batches.append({'parameters':b['parameters'], b['repeat']: {'s_output': b['s_output'], 'c_output': b['c_output']}})
    return batches
    # list batch files that match a pattern
    # later choose from them. now take them all.
    # load batch
    # return data object


def get_s_c_mean_std(data, key):
    set_sizes = []
    server_means = []
    client_means = []
    server_stds = []
    client_stds = []
    for b in data:
        set_sizes.append(b['parameters']['client_neles'])
        s_measure = []
        c_measure = []
        for i in range(len(b)-1):
            try:
                s_measure.append(b[i]['s_output'][key])
                c_measure.append(b[i]['c_output'][key])
            except KeyError as k:
                print(f"KEYERROR for key: {key} in repeat {i} for {b['parameters']['client_neles']}")
                # raise k
        # print(f"Server hashing time: {sum(s_measure)/(len(b)-1)}")
        # print(f"Client hashing time: {sum(c_measure)/(len(b)-1)}")
        server_means.append(np.mean(s_measure))
        server_stds.append(np.std(s_measure))
        client_means.append(np.mean(c_measure))
        client_stds.append(np.std(c_measure))
    
    return set_sizes, server_means, server_stds, client_means, client_stds

def plot_hashing(data):
    # simple plot right now.
    set_sizes, server_means, server_stds, client_means, client_stds = get_s_c_mean_std(data, "hashing_t")
    x_pos = np.arange(len(set_sizes))
    fig, ax = plt.subplots()
    server = ax.bar(x_pos-0.1, server_means, yerr=server_stds, width=0.2, color='b', align='center', alpha=0.5,
           ecolor='black', capsize=10) 
    client = ax.bar(x_pos+0.1, client_means, yerr=client_stds, width=0.2, color='g', align='center', alpha=0.5,
           ecolor='black', capsize=10)
    ax.set_ylabel(f"Time for hashing in ms")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(set_sizes)
    ax.set_title("Hashing times for Desktop-App for different set sizes. With std-error.")
    ax.yaxis.grid(True)

    ax.legend((server[0], client[0]),('server', 'client'))

    plt.tight_layout()
    plt.show()

def plot_total_time(data):
    set_sizes, server_means, server_stds, client_means, client_stds = get_s_c_mean_std(
        data, "total_t")
    x_pos = np.arange(len(set_sizes))
    fig, ax = plt.subplots()
    server = ax.bar(x_pos-0.1, server_means, yerr=server_stds, width=0.2, color='b', align='center', alpha=0.5,
           ecolor='black', capsize=10) 
    client = ax.bar(x_pos+0.1, client_means, yerr=client_stds, width=0.2, color='g', align='center', alpha=0.5,
           ecolor='black', capsize=10)
    ax.set_ylabel(f"Total time in in ms")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(set_sizes)
    ax.set_title("Total time for Desktop-App for different set sizes. With std-error.")
    ax.yaxis.grid(True)

    ax.legend((server[0], client[0]),('server', 'client'))

    plt.tight_layout()
    plt.show()


def plot_time_donut(data):
    pass

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--hash', action='store_true')
    ap.add_argument('--total_t', action='store_true')
    args = ap.parse_args()
    data = load_batch(batch_name)
    if args.hash:
        plot_hashing(data)
    if args.total_t:
        plot_total_time(data)