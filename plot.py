import numpy as np
import matplotlib.pyplot as plt
import os.path
import glob
import json
import argparse
from psi import Psi_type, CLIENT, SERVER
from plot_utils import load_batch, xticks_to_potencies_label, get_s_c_mean_std

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


def plot_poly_size(data):
    # simple plot right now.
    set_sizes, server_means, server_stds, _, _ = get_s_c_mean_std(
        data, "poly_d_rs",rs='s')
    x_pos = np.arange(len(set_sizes))
    server_means = server_means/1e6
    server_stds = server_stds/1e6
    fig, ax = plt.subplots()
    server = ax.bar(x_pos, server_means, width=0.2, color='b', align='center', alpha=0.5, capsize=10)
    ax.set_ylabel(f"Data transmitted im MegaBytes")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(set_sizes)
    ax.set_title(
        "Polynomials transmitted for Desktop-App for different set sizes. With std-error.")
    ax.yaxis.grid(True)

    # ax.legend((server[0]), ('server'))

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


def plot_total_data_stacked(data):
    set_sizes, server_r_means, server_r_stds, client_r_means, client_r_stds = get_s_c_mean_std(
        data, "total_d_rs", rs='r') 
    set_sizes, server_s_means, server_s_stds, client_s_means, client_s_stds = get_s_c_mean_std(
        data, "total_d_rs", rs='s')
    x_pos = np.arange(len(set_sizes))
    fig, ax = plt.subplots()
    client_r_means = client_r_means/1e9
    client_s_means = client_s_means/1e9
    # print(f"mean: {client_r_means[0]} single: {data[]}")
    # client_r_stds = client_r_stds/1e9
    # client_s_stds = client_s_stds/1e9

    # Add a table at the bottom of the axes
    client_r = ax.bar(x_pos, client_r_means, color='b', align='center', alpha=0.5)
    client_s = ax.bar(x_pos, client_s_means, color='g', align='center', alpha=0.5, bottom=client_r_means)
    ax.set_ylabel(f"Total data in GigaBytes ($10^9$ Bytes)")
    
    ax.set_xticks(x_pos)
    potencies = [int(np.log2(x)) for x in set_sizes]
    ax.set_xticklabels([f"$2^{{{p}}}$" for p in potencies])

    ax.set_xlabel(f"Set sizes for both server and client (n_1=n_2).")
    ax.set_title(
        f"Client: Total data received/sent for Desktop-App.\nBasic analytics circuit. Balanced sets.")
    ax.yaxis.grid(True)

    ax.legend((client_r[0], client_s[0]), ('client received', 'client sent'))

    plt.tight_layout()
    plt.show()

def plot_total_data(data):
    set_sizes, server_r_means, server_r_stds, client_r_means, client_r_stds = get_s_c_mean_std(
        data, "total_d_rs", rs='r')
    set_sizes, server_s_means, server_s_stds, client_s_means, client_s_stds = get_s_c_mean_std(
        data, "total_d_rs", rs='s')
    x_pos = np.arange(len(set_sizes))
    fig, ax = plt.subplots()
    client_r_means = client_r_means/1e9
    client_s_means = client_s_means/1e9
    # print(f"mean: {client_r_means[0]} single: {data[]}")
    # client_r_stds = client_r_stds/1e9
    # client_s_stds = client_s_stds/1e9

    # Add a table at the bottom of the axes
    client_r = ax.bar(x_pos-0.1, client_r_means, width=0.2, color='b', align='center', alpha=0.5,
                      ecolor='black', capsize=5)
    client_s = ax.bar(x_pos+0.1, client_s_means, width=0.2, color='g', align='center', alpha=0.5,
                      ecolor='black', capsize=5)
    ax.set_ylabel(f"Total data in in GigaBytes")

    ax.set_xticks(x_pos)
    ax.set_xticklabels(set_sizes)
    ax.set_xlabel(f"Server set sizes")
    ax.set_title(
        "Client: Total data received/sent for Desktop-App for different set sizes.")
    ax.yaxis.grid(True)

    ax.legend((client_r[0], client_s[0]), ('client received', 'client sent'))

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
    online = ax.bar(x_pos, online_means, yerr=online_stds, width=0.2, color='g', align='center', alpha=0.5,
                    ecolor='black', capsize=10)
    if not online_only:
        setup = ax.bar(x_pos, setup_means, yerr=setup_stds, width=0.2, color='b', align='center', alpha=0.5,
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

    if not online_only:
        ax.legend((setup[0], online[0]), ('Setup-phase', 'Online-phase'))

    plt.tight_layout()
    plt.show()

def plot_time_pies(data, combined=False):
    # for each !OR FOR ONE DEPENDING ON COMBINED!
    # batch (equal parameters, different repeats)
        # for each repeat
            # the *_t timings are averaged
        # the other_t is calculated as the differents of the sum of all measured
        # timings and the total timing.
        # the percentage of the total running time is taken.
    # the percentages are averaged over the batches.
    if combined:
        batches = data
    else:
        batches = [data[0]]
    pct_client = {
        'hashing_t': 0.0,
        'oprf_t': 0.0,
        'poly_trans_t': 0.0,
        'poly_t': 0.0,
        'aby_online_t': 0.0,
        'aby_setup_t': 0.0,
        'base_t': 0.0,
        'other_t': 0.0
    }
    pct_server = {
        'hashing_t': 0.0,
        'oprf_t': 0.0,
        'poly_trans_t': 0.0,
        'poly_t': 0.0,
        'aby_online_t': 0.0,
        'aby_setup_t': 0.0,
        'base_t' : 0.0,
        'other_t': 0.0
    }
    for b in batches:
        client = {
            'hashing_t': 0,
            'oprf_t': 0,
            'poly_trans_t': 0,
            'poly_t': 0,
            'aby_online_t': 0,
            'aby_setup_t': 0,
            'total_t': 0,
            'nobase_t': 0
        }
        server = {
            'hashing_t': 0,
            'oprf_t': 0,
            'poly_trans_t': 0,
            'poly_t': 0,
            'aby_online_t': 0,
            'aby_setup_t': 0,
            'total_t' : 0,
            'nobase_t': 0
        }
        
        # sum up 
        for i in range(len(b)-1):
            for k in client:
                client[k] += b[i]['c_output'][k]
            for k in server:
                server[k] += b[i]['s_output'][k]

        client['base_t'] = client['total_t'] - client['nobase_t']
        server['base_t'] = server['total_t'] - server['nobase_t']
        del client['nobase_t']
        del server['nobase_t']

        # get average
        for k in client:
            client[k] = float(client[k])/(len(b)-1.0)

        for k in server:
            server[k] = float(server[k])/(len(b)-1.0)
        
        print(server)
        # client poly trans wait is mostly waiting for the server to begin.
        client['poly_trans_t'] = server['poly_trans_t']
        
        # other
        c_other = 2*client['total_t'] 
        for k in client:
            c_other -= client[k]
        client['other_t'] = c_other

        s_other = 2*server['total_t']
        for k in server:
            s_other -= server[k]
        server['other_t'] = s_other


        for k in pct_client:
            pct_client[k] += client[k]/client['total_t']

        for k in pct_server:
            pct_server[k] += server[k]/server['total_t']

    # get average
    for k in pct_client:
        pct_client[k] = (pct_client[k]/float(len(batches)))*100.0

    for k in pct_server:
        pct_server[k] = (pct_server[k]/float(len(batches)))*100.0

    print(pct_server)
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    #### For inside text!
    # wedges, texts, autotexts = ax.pie(pct_server.values(), autopct=lambda pct: f"{pct:.1f}%",
    #                                   textprops=dict(color="w"), counterclock=False)

    # ax.legend(wedges, pct_server.keys(),
    #           title="Phases",
    #           loc="center left",
    #           bbox_to_anchor=(1, 0, 0.5, 1))

    # plt.setp(autotexts, size=8, weight="bold")

    wedges, texts, = ax.pie(pct_server.values(),startangle=-90)

    # from https://matplotlib.org/3.1.1/gallery/pie_and_polar_charts/pie_and_donut_labels.html
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
            bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(f"{list(pct_server.values())[i]:.2f}% {list(pct_server.keys())[i]}", xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                    horizontalalignment=horizontalalignment, **kw)


    ax.set_title("Server (DA): Combination of phases time-wise")

    plt.show()

def plot_psi_types_dt(data):
    set_sizes, server_means, server_stds, client_means, client_stds = get_s_c_mean_std(
        data, "total_t", parameter='psi')
    set_sizes, server_r_means, server_r_stds, client_r_means, client_r_stds = get_s_c_mean_std(
        data, "total_d_rs", rs='r', parameter='psi')
    set_sizes, server_s_means, server_s_stds, client_s_means, client_s_stds = get_s_c_mean_std(
        data, "total_d_rs", rs='s', parameter='psi')
    # client_means = client_means/1e3 # seconds?
    client_r_means = client_r_means/1e9
    client_s_means = client_s_means/1e9
    client_r_stds = client_r_stds/1e9
    client_s_stds = client_s_stds/1e9

    x_pos = np.array(set_sizes)
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('PSI Function Types')
    ax1.set_ylabel('Total data in in GigaBytes')
    ax1.set_xticks(x_pos)
    ax1.set_title(
        "Client: Time and data for Desktop-App for different psi types with n=4096 elements. With std-error.")
    labels = [Psi_type(i).name for i in set_sizes]
    ax1.set_xticklabels(labels)
    client_r = ax1.bar(x_pos-0.1, client_r_means, yerr=client_r_stds, width=0.1, color='b', align='center', alpha=0.5,
                       ecolor='black', capsize=5)
    client_s = ax1.bar(x_pos, client_s_means, yerr=client_s_stds, width=0.1, color='g', align='center', alpha=0.5,
                       ecolor='black', capsize=5)
    ax2 = ax1.twinx()
    ax2.set_ylabel('time (ms)',color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')
    # Add a table at the bottom of the axes
    client_t = ax2.bar(x_pos+0.1, client_means, yerr=client_stds, width=0.1, color='tab:red', align='center', alpha=0.5,
                       ecolor='black', capsize=5)
    ax1.legend((client_r[0], client_s[0], client_t[0]),
               ('client received', 'client sent', 'time'))
    # fig.tight_layout()
    plt.show()


def plot_server_scaling_dt(data):
    set_sizes, server_means, server_stds, client_means, client_stds = get_s_c_mean_std(
        data, "total_t", parameter='server_set')
    set_sizes, server_r_means, server_r_stds, client_r_means, client_r_stds = get_s_c_mean_std(
        data, "total_d_rs", rs='r', parameter='server_set')
    set_sizes, server_s_means, server_s_stds, client_s_means, client_s_stds = get_s_c_mean_std(
        data, "total_d_rs", rs='s', parameter='server_set')
    client_means = client_means/1e3 # seconds?
    client_stds = client_stds/1e3 # seconds?
    client_r_means = client_r_means/1e6
    client_s_means = client_s_means/1e6
    client_r_stds = client_r_stds/1e6
    client_s_stds = client_s_stds/1e6
    x_pos = np.arange(len(set_sizes))
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Server set sizes')
    ax1.set_ylabel('Total data in in MegaBytes')
    # ax1.set_yscale('log')
    ax1.set_xticks(x_pos)
    ax1.set_title(
        "Client: Time and data for Desktop-App for different server set sizes with n_client=1024 elements. 5 runs with std-error.")
    ax1.set_xticklabels(set_sizes)
    client_r = ax1.bar(x_pos-0.1, client_r_means, yerr=client_r_stds, width=0.1, color='b', align='center', alpha=0.5,
                       ecolor='black', capsize=5)
    client_s = ax1.bar(x_pos, client_s_means, yerr=client_s_stds, width=0.1, color='g', align='center', alpha=0.5,
                       ecolor='black', capsize=5)
    ax2 = ax1.twinx()
    ax2.set_ylabel('time (s)', color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    client_t = ax2.bar(x_pos+0.1, client_means, yerr=client_stds, width=0.1, color='tab:red', align='center', alpha=0.5,
                       ecolor='black', capsize=5)
    ax1.legend((client_r[0], client_s[0], client_t[0]),
               ('client received', 'client sent', 'time'))
    # fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--hash', action='store_true')
    ap.add_argument('--poly_d', action='store_true')
    ap.add_argument('--total_t', action='store_true')
    ap.add_argument('--total_d', action='store_true')
    ap.add_argument('--total_d_stacked', action='store_true')
    ap.add_argument('--aby_t', action='store_true')
    ap.add_argument('--pies_t', action='store_true')
    ap.add_argument('--psi_types_dt', action='store_true')
    ap.add_argument('--server_scaling_dt', action='store_true')
    args = ap.parse_args()
    batch_name = "BalancedAnalyticsDA_1"
    data = load_batch(batch_name)
    if args.all or args.hash:
        plot_hashing(data)
    if args.all or args.poly_d:
        plot_poly_size(data)
    if args.all or args.total_t:
        plot_total_time(data)
    if args.all or args.aby_t:
        plot_aby_time(data)
    if args.all or args.pies_t:
        plot_time_pies(data)
    if args.all or args.total_d:
        plot_total_data(data)
    if args.all or args.total_d_stacked:
        plot_total_data_stacked(data)
    if args.all or args.psi_types_dt:
        if 'PsiTypes' in batch_name:
            plot_psi_types_dt(data)
    if args.all or args.server_scaling_dt:
        if 'ServerScaling' in batch_name:
            plot_server_scaling_dt(data)
