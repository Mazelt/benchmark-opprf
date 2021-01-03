import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import sem
import os.path
import glob
import json
import argparse
from psi import Psi_type, CLIENT, SERVER
from plot_utils import load_batch, get_s_c_mean_sd, get_specific_s_c_mean_sd, xticks_to_potencies_label, tableau_c10


def get_rtt(data):
    b = data[0]
    rtts = []
    # rtts = [2.4205, 2.757, 2.518, 2.45363, 2.57025, 2.41744, 2.29819, 2.35794, 2.32744, 2.31425, 2.132, 2.37244, 2.92756, 2.752, 2.50294, 2.4095, 2.40994, 2.47906, 2.81631, 2.61075, 2.4955, 2.43962, 2.45887, 2.43662, 2.68319,
    #         2.62794, 2.46756, 2.38719, 2.23781, 2.49313, 2.32925, 2.5685, 2.32725, 2.63925, 2.8215, 2.372, 2.40856, 2.37625, 2.28494, 2.50756, 2.60763, 2.44612, 2.81256, 2.26719, 2.54137, 2.19531, 2.7655, 2.438, 2.41919, 2.38944]
    # print(b)
    for i in range(len(b)-1):
        rtts.append(b[i]['s_output']['rtt'])
    rtt_mean = np.mean(rtts)
    rtt_sd = np.std(rtts)
    rtt_se = sem(rtts)
    print(f"{len(rtts)} RTTs: mean: {rtt_mean}, sd: {rtt_sd}, se {rtt_se}.")


def get_tp(data):
    b = data[0]
    tps = []
    # tps = [2.4205, 2.757, 2.518, 2.45363, 2.57025, 2.41744, 2.29819, 2.35794, 2.32744, 2.31425, 2.132, 2.37244, 2.92756, 2.752, 2.50294, 2.4095, 2.40994, 2.47906, 2.81631, 2.61075, 2.4955, 2.43962, 2.45887, 2.43662, 2.68319,
    #         2.62794, 2.46756, 2.38719, 2.23781, 2.49313, 2.32925, 2.5685, 2.32725, 2.63925, 2.8215, 2.372, 2.40856, 2.37625, 2.28494, 2.50756, 2.60763, 2.44612, 2.81256, 2.26719, 2.54137, 2.19531, 2.7655, 2.438, 2.41919, 2.38944]
    # print(b)
    for i in range(len(b)-1):
        tps.append(b[i]['s_output']['throughput'])
    tp_mean = np.mean(tps)
    tp_sd = np.std(tps)
    tp_se = sem(tps)
    print(f"{len(tps)} tps: mean: {tp_mean}, sd: {tp_sd}, se {tp_se}.")

def plot_total_time(datalan, datalte):

    set_sizes_lan, server_means_lan, server_stds_lan, client_means_lan, client_stds_lan = \
        get_specific_s_c_mean_sd(datalan, 'total_t', circuit=Psi_type.Analytics, 
                                  parameter='server_neles', pfilter={'server_neles':[2**17,2**19,2**21]})
    set_sizes_lte, server_means_lte, server_stds_lte, client_means_lte, client_stds_lte = \
        get_specific_s_c_mean_sd(datalte, 'total_t', circuit=Psi_type.Analytics,
                                 parameter='server_neles', pfilter={'server_neles': [2**17, 2**19, 2**21]})
    x_pos = np.arange(len(set_sizes_lan))
    client_means_lan = client_means_lan/1e3
    client_stds_lan = client_stds_lan/1e3
    client_means_lte = client_means_lte/1e3
    client_stds_lte = client_stds_lte/1e3
    fig, ax = plt.subplots()
    client_lan = ax.bar(x_pos-0.1, client_means_lan, yerr=client_stds_lan, color=tableau_c10[1], align='center', alpha=0.5, width=0.2,
           ecolor='black', capsize=5)
    client_lte = ax.bar(x_pos+0.1, client_means_lte, yerr=client_stds_lte, color=tableau_c10[0], align='center', alpha=0.5, width=0.2,
           ecolor='black', capsize=5)
    ax.set_ylabel(f"Total time in in seconds")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(xticks_to_potencies_label(set_sizes_lan))
    ax.set_title(
        f"Client: Total time for Desktop-App with different networks.\nUnbalanced sets with client set size $2^{{{int(np.log2(datalan[0]['parameters']['client_neles']))}}}$ and the basic analytics circuit.\nMean over {len(datalan[0])-1} runs with std-error.")
    ax.yaxis.grid(True)
    ax.set_xlabel(f"Server set sizes")
    ax.legend((client_lan[0], client_lte[0]),('LAN', 'LTE'))

    plt.tight_layout()
    plt.show()


def plot_total_time_absum(data):
    set_sizes, server_means, server_stds, client_means, client_stds = get_s_c_mean_sd(
        data, "total_t")
    x_pos = np.arange(len(set_sizes))
    client_means = client_means/1e3
    client_stds = client_stds/1e3
    fig, ax = plt.subplots()
    client = ax.bar(x_pos, client_means, yerr=client_stds, color=tableau_c10[1], align='center', alpha=0.5,
                    ecolor='black', capsize=5)
    ax.set_ylabel(f"Total time in in seconds")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(xticks_to_potencies_label(set_sizes))
    ax.set_title(
        f"Total time for Desktop-App with the PayloadABSum circuit.\nUnbalanced sets with client set size $2^{{{int(np.log2(data[0]['parameters']['client_neles']))}}}$\nMean over {len(data[0])-1} runs with std-error.")
    ax.yaxis.grid(True)
    ax.set_xlabel(f"Server set sizes")
    # ax.legend((server[0], client[0]),('server', 'client'))

    plt.tight_layout()
    plt.show()



def plot_aby_time(data, online_only=True ,role=CLIENT):
    set_sizes, _, _, online_means, online_stds = get_s_c_mean_sd(
        data, "aby_online_t")
    if not online_only:
        set_sizes, _, _, setup_means, setup_stds = get_s_c_mean_sd(
            data, "aby_setup_t")
    # set_sizes, _, _, total_means, total_stds = get_s_c_mean_sd(
    #     data, "aby_total_t")
    x_pos = np.arange(len(set_sizes))
    fig, ax = plt.subplots()
    online = ax.bar(x_pos, online_means, yerr=online_stds, width=0.2, color=tableau_c10[1], align='center', alpha=0.5,
                    ecolor='black', capsize=10)
    if not online_only:
        setup = ax.bar(x_pos, setup_means, yerr=setup_stds, width=0.2, color=tableau_c10[0], align='center', alpha=0.5,
                        ecolor='black', capsize=10, bottom=online)
    ax.set_ylabel(f"Time in in ms")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(set_sizes)
    if online_only:
        ax.set_title(
            "Aby online phase timings for different set sizes. With std-error.")
    else:
        ax.set_title(
            "Aby timings for different set sizes. With std-error."
        )
    ax.yaxis.grid(True)
    ax.set_xlabel(f"Server set sizes")
    if not online_only:
        ax.legend((setup[0], online[0]), ('Setup-phase', 'Online-phase'))

    plt.tight_layout()
    plt.show()


def plot_aby_time_absum(data, online_only=True, role=CLIENT):
    set_sizes, _, _, online_means, online_stds = get_s_c_mean_sd(
        data, "aby_online_t")
    if not online_only:
        set_sizes, _, _, setup_means, setup_stds = get_s_c_mean_sd(
            data, "aby_setup_t")
    # set_sizes, _, _, total_means, total_stds = get_s_c_mean_sd(
    #     data, "aby_total_t")
    x_pos = np.arange(len(set_sizes))
    fig, ax = plt.subplots()
    online = ax.bar(x_pos, online_means, yerr=online_stds, width=0.2, color=tableau_c10[1], align='center', alpha=0.5,
                    ecolor='black', capsize=10)
    if not online_only:
        setup = ax.bar(x_pos, setup_means, yerr=setup_stds, width=0.2, color=tableau_c10[0], align='center', alpha=0.5,
                       ecolor='black', capsize=10, bottom=online)
    ax.set_ylabel(f"Time in in ms")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(xticks_to_potencies_label(set_sizes))
    if online_only:
        ax.set_title(
           f"Aby online phase times for PayloadABSum circuit.\nUnbalanced sets with client set size $2^{{{int(np.log2(data[0]['parameters']['client_neles']))}}}$")
    else:
        ax.set_title(
            "Aby setup/online phase times for PayloadABSum circuit.\nUnbalanced sets with client set size $2^{{{int(np.log2(data[0]['parameters']['client_neles']))}}}$"
        )
    ax.yaxis.grid(True)
    ax.set_xlabel(f"Server set sizes")
    if not online_only:
        ax.legend((setup[0], online[0]), ('Setup-phase', 'Online-phase'))

    plt.tight_layout()
    plt.show()

 
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--rtts', action='store_true')
    ap.add_argument('--tps', action='store_true')
    ap.add_argument('--total_t', action='store_true')
    ap.add_argument('--aby_t', action='store_true')
    ap.add_argument('--pies_t', action='store_true')
    args = ap.parse_args()
    
    if args.rtts:
        batch = load_batch('NetworkDebugging_NewRTTs_LTE')
        get_rtt(batch)
    elif args.tps:
        batch = load_batch('NetworkDebugging_NewRTTs_LTE')
        get_tp(batch)
    else:

        batch_10_LAN = load_batch('Unbalanced10AnalyticsDA_2')
        batch_10_LTE = load_batch('NetworkLTE10AnalyticsDA_1')
        
        plot_total_time(batch_10_LAN, batch_10_LTE)
