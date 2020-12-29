import numpy as np
import matplotlib.pyplot as plt
import os.path
import glob
import json
import argparse
from psi import Psi_type, CLIENT, SERVER
from plot_utils import load_batch, get_s_c_mean_std, get_specific_s_c_mean_std, xticks_to_potencies_label, tableau_c10



def plot_total_time(datalan, datalte):

    set_sizes_lan, server_means_lan, server_stds_lan, client_means_lan, client_stds_lan = \
        get_specific_s_c_mean_std(datalan, 'total_t', circuit=Psi_type.Analytics, 
                                  parameter='server_neles', pfilter=[2**17,2**19,2**21])
    set_sizes_lte, server_means_lte, server_stds_lte, client_means_lte, client_stds_lte = \
        get_specific_s_c_mean_std(datalte, 'total_t', circuit=Psi_type.Analytics,
                                  parameter='server_neles', pfilter=[2**17, 2**19, 2**21])
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
    set_sizes, server_means, server_stds, client_means, client_stds = get_s_c_mean_std(
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
    set_sizes, _, _, online_means, online_stds = get_s_c_mean_std(
        data, "aby_online_t")
    if not online_only:
        set_sizes, _, _, setup_means, setup_stds = get_s_c_mean_std(
            data, "aby_setup_t")
    # set_sizes, _, _, total_means, total_stds = get_s_c_mean_std(
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
    set_sizes, _, _, online_means, online_stds = get_s_c_mean_std(
        data, "aby_online_t")
    if not online_only:
        set_sizes, _, _, setup_means, setup_stds = get_s_c_mean_std(
            data, "aby_setup_t")
    # set_sizes, _, _, total_means, total_stds = get_s_c_mean_std(
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
    ap.add_argument('--total_t', action='store_true')
    ap.add_argument('--aby_t', action='store_true')
    ap.add_argument('--pies_t', action='store_true')
    args = ap.parse_args()
    
    batch_10_LAN = load_batch('Unbalanced10AnalyticsDA_2')
    batch_10_LTE = load_batch('NetworkLTE10AnalyticsDA_1')
    
    plot_total_time(batch_10_LAN, batch_10_LTE)
