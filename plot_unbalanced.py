import numpy as np
import matplotlib.pyplot as plt
import os.path
import glob
import json
import argparse
from psi import Psi_type, CLIENT, SERVER
from plot_utils import load_batch, get_s_c_mean_sd, get_s_c_mean_se, xticks_to_potencies_label, \
tableau_c10, get_specific_s_c_mean_sd, print_table




def plot_hashing(data):
    # simple plot right now.
    set_sizes, server_means, server_stds, client_means, client_stds = get_s_c_mean_sd(data, "hashing_t")
    server_means = server_means/1e3
    server_stds = server_stds/1e3
    x_pos = np.arange(len(set_sizes))

    fig, ax = plt.subplots()
    server = ax.bar(x_pos, server_means, yerr=server_stds, color=tableau_c10[0], align='center', alpha=0.5,
           ecolor='black', capsize=5) 
    ax.set_ylabel(f"Time for hashing in seconds")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(xticks_to_potencies_label(set_sizes))
    ax.set_title(
        f"Server: Hashing times for Desktop-App. Unbalanced sets with different server set sizes.\nMean over {len(data[0])-1} runs with std-error.")
    ax.yaxis.grid(True)
    ax.set_xlabel(f"Server set sizes")
    plt.tight_layout()
    plt.show()

def plot_poly_size(data):
    # simple plot right now.
    set_sizes, server_means, server_stds, _, _ = get_s_c_mean_sd(
        data, "poly_d_rs",rs='s')
    x_pos = np.arange(len(set_sizes))
    server_means = server_means/1e6
    server_stds = server_stds/1e6
    fig, ax = plt.subplots()
    server = ax.bar(x_pos, server_means, width=0.2, color=tableau_c10[0], align='center', alpha=0.5, capsize=10)
    ax.set_ylabel(f"Data transmitted im MegaBytes")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(set_sizes)
    ax.set_title(
        "Polynomials transmitted for Desktop-App for different set sizes. With std-error.")
    ax.yaxis.grid(True)
    ax.set_xlabel(f"Server set sizes")
    # ax.legend((server[0]), ('server'))

    plt.tight_layout()
    plt.show()

def plot_total_time(data):
    set_sizes, server_means, server_stds, client_means, client_stds = get_s_c_mean_se(
        data, "total_t")
    x_pos = np.arange(len(set_sizes))
    client_means = client_means/1e3
    client_stds = client_stds/1e3
    fig, ax = plt.subplots()
    client = ax.bar(x_pos, client_means, yerr=client_stds, color=tableau_c10[1], align='center', alpha=0.5,
           ecolor='black', capsize=5)
    ax.set_ylabel(f"Total time in seconds")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(xticks_to_potencies_label(set_sizes))
    ax.set_title(
        f"Total time for Desktop-App with the basic analytics circuit.\nUnbalanced sets with client set size $2^{{{int(np.log2(data[0]['parameters']['client_neles']))}}}$\nMean over {len(data[0])-1} runs with std-error.")
    ax.yaxis.grid(True)
    ax.set_xlabel(f"Server set sizes")
    # ax.legend((server[0], client[0]),('server', 'client'))

    plt.tight_layout()
    plt.show()


def plot_total_time_combined(data10,data12):
    set_sizes_10, server_means_10, server_sd_10, client_means_10, client_sd_10 = get_s_c_mean_sd(
        data10, "total_t")
    set_sizes_12, server_means_12, server_sd_12, client_means_12, client_sd_12 = get_s_c_mean_sd(
        data12, "total_t")
    x_pos_10 = np.arange(len(set_sizes_10))
    x_pos_12 = np.arange(len(set_sizes_12))
    client_means_10 = client_means_10/1e3
    client_sd_10 = client_sd_10/1e3
    client_means_12 = client_means_12/1e3
    client_sd_12 = client_sd_12/1e3
    fig, ax = plt.subplots()
    # client = ax.bar(x_pos, client_means, yerr=client_sd_10, color=tableau_c10[1], align='center', alpha=0.5,
    #                 ecolor='black', capsize=5)
    client_10 = ax.bar(x_pos_10-0.1, client_means_10, yerr=client_sd_10, width=0.2,
                       color=tableau_c10[0], align='center', alpha=0.5, ecolor='black', capsize=2)
    client_12 = ax.bar(x_pos_12+0.1+2, client_means_12,yerr=client_sd_12, width=0.2,
                       color=tableau_c10[1], align='center', alpha=0.5, ecolor='black', capsize=2)

    ax.set_ylabel(f"Total runtime in seconds")
    ax.set_xticks(x_pos_10)
    ax.set_xticklabels(xticks_to_potencies_label(set_sizes_10))
    # for i in range(1,len(client_means_10)):
    #     print(client_means_10[i]/client_means_10[0])
    # for i in range(1, len(client_means_12)):
    #     print(client_means_12[i]/client_means_12[0])
    print(client_means_10)
    print(client_means_12)
    # ax.set_title(
    #     f"Total time for Desktop-App with the basic analytics circuit.\nUnbalanced sets with client set size $2^{{{int(np.log2(data[0]['parameters']['client_neles']))}}}$\nMean over {len(data[0])-1} runs with std-error.")
    ax.yaxis.grid(True)
    ax.set_xlabel(f"Server set sizes ($n_2$)")
    ax.legend((client_10[0], client_12[0]),
              ('$n_1$ = $2^{10}$', '$n_1$ = $2^{12}$'))

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
    ax.set_xlabel(f"Server set sizes ($n_2$)")
    # ax.legend((server[0], client[0]),('server', 'client'))

    plt.tight_layout()
    plt.show()

def plot_total_data_stacked_combined(data10,data12):
    set_sizes_10, server_r_means_10, server_r_stds_10, client_r_means_10, client_r_stds_10 = get_s_c_mean_sd(
        data10, "total_d_rs", rs='r')
    _, server_s_means_10, server_s_stds_10, client_s_means_10, client_s_stds_10 = get_s_c_mean_sd(
        data10, "total_d_rs", rs='s')

    set_sizes_12, server_r_means_12, server_r_stds_12, client_r_means_12, client_r_stds_12 = get_s_c_mean_sd(
        data12, "total_d_rs", rs='r')

    _, server_s_means_12, server_s_stds_12, client_s_means_12, client_s_stds_12 = get_s_c_mean_sd(
        data12, "total_d_rs", rs='s')
    x_pos_10 = np.arange(len(set_sizes_10))
    x_pos_12 = np.arange(len(set_sizes_12))
    fig, ax = plt.subplots()
    client_r_means_10 = client_r_means_10/1e6
    client_s_means_10 = client_s_means_10/1e6
    client_r_means_12 = client_r_means_12/1e6
    client_s_means_12 = client_s_means_12/1e6
    # print(f"mean: {client_r_means[0]} single: {data[]}")
    # client_r_stds = client_r_stds/1e9
    # client_s_stds = client_s_stds/1e9

    print(client_r_means_10+client_s_means_10)
    print(client_r_means_12+client_s_means_12)
    # Add a table at the bottom of the axes
    client_r_10 = ax.bar(x_pos_10-0.1, client_r_means_10, width=0.2,
                      color=tableau_c10[0], align='center', alpha=0.5)
    client_s_10 = ax.bar(x_pos_10-0.1, client_s_means_10, width=0.2, color=tableau_c10[1],
                         align='center', alpha=0.5, bottom=client_r_means_10)

    client_r_12 = ax.bar(x_pos_12+0.1+2, client_r_means_12, width=0.2, hatch='///',
                         color=tableau_c10[0], align='center', alpha=0.5)
    client_s_12 = ax.bar(x_pos_12+0.1+2, client_s_means_12, width=0.2, color=tableau_c10[1], hatch='///',
                         align='center', alpha=0.5, bottom=client_r_means_12)
    ax.set_ylabel(f"Total data in in MegaBytes")

    ax.set_xticks(x_pos_10)
    potencies = [int(np.log2(x)) for x in set_sizes_10]
    ax.set_xticklabels([f"$2^{{{p}}}$" for p in potencies])
    # ax.set_yscale('log')

    ax.set_xlabel(f"Server set sizes ($n_2$)")
    # ax.set_title(
    #     f"Client: Total data received/sent for Desktop-App.\nBasic analytics circuit. Unbalanced sets with client set sizes $2^{{10}}$,$2^{{12}}$")
    ax.yaxis.grid(True)

    ax.legend((client_r_10[0], client_s_10[0], client_r_12[0], client_s_12[0], ),
              ('client received $n_1=2^{10}$', 'client sent $n_1=2^{10}$', 'client received $n_1=2^{12}$', 'client sent $n_1=2^{12}$'))

    plt.tight_layout()
    plt.show()

def plot_total_data_stacked(data):
    set_sizes, server_r_means, server_r_stds, client_r_means, client_r_stds = get_s_c_mean_sd(
        data, "total_d_rs", rs='r') 
    set_sizes, server_s_means, server_s_stds, client_s_means, client_s_stds = get_s_c_mean_sd(
        data, "total_d_rs", rs='s')
    x_pos = np.arange(len(set_sizes))
    fig, ax = plt.subplots()
    client_r_means = client_r_means/1e6
    client_s_means = client_s_means/1e6
    # print(f"mean: {client_r_means[0]} single: {data[]}")
    # client_r_stds = client_r_stds/1e9
    # client_s_stds = client_s_stds/1e9

    # Add a table at the bottom of the axes
    client_r = ax.bar(x_pos, client_r_means, width=0.2, color=tableau_c10[0], align='center', alpha=0.5)
    client_s = ax.bar(x_pos, client_s_means, width=0.2, color=tableau_c10[1], align='center', alpha=0.5, bottom=client_r_means)
    ax.set_ylabel(f"Total data in in MegaBytes")
    
    ax.set_xticks(x_pos)
    potencies = [int(np.log2(x)) for x in set_sizes]
    ax.set_xticklabels([f"$2^{{{p}}}$" for p in potencies])

    ax.set_xlabel(f"Server set sizes")
    ax.set_title(
        f"Client: Total data received/sent for Desktop-App.\nBasic analytics circuit. Unbalanced sets with client set size $2^{{{int(np.log2(data[0]['parameters']['client_neles']))}}}$")
    ax.yaxis.grid(True)

    ax.legend((client_r[0], client_s[0]), ('client received', 'client sent'))

    plt.tight_layout()
    plt.show()


def plot_total_data_absum_stacked(data):
    set_sizes, server_r_means, server_r_stds, client_r_means, client_r_stds = get_s_c_mean_sd(
        data, "total_d_rs", rs='r')
    set_sizes, server_s_means, server_s_stds, client_s_means, client_s_stds = get_s_c_mean_sd(
        data, "total_d_rs", rs='s')
    x_pos = np.arange(len(set_sizes))
    fig, ax = plt.subplots()
    client_r_means = client_r_means/1e6
    client_s_means = client_s_means/1e6
    # print(f"mean: {client_r_means[0]} single: {data[]}")
    # client_r_stds = client_r_stds/1e9
    # client_s_stds = client_s_stds/1e9

    # Add a table at the bottom of the axes
    client_r = ax.bar(x_pos, client_r_means, 
                      color=tableau_c10[0], align='center', alpha=0.5)
    client_s = ax.bar(x_pos, client_s_means,  color=tableau_c10[1],
                      align='center', alpha=0.5, bottom=client_r_means)
    ax.set_ylabel(f"Total data in in MegaBytes")

    ax.set_xticks(x_pos)
    potencies = [int(np.log2(x)) for x in set_sizes]
    ax.set_xticklabels([f"$2^{{{p}}}$" for p in potencies])

    ax.set_xlabel(f"Server set sizes")
    ax.set_title(
        f"Client: Total data received/sent for Desktop-App.\nPayloadABSum circuit. Unbalanced sets with client set size $2^{{{int(np.log2(data[0]['parameters']['client_neles']))}}}$")
    ax.yaxis.grid(True)

    ax.legend((client_r[0], client_s[0]), ('client received', 'client sent'))

    plt.tight_layout()
    plt.show()

def plot_total_data(data):
    set_sizes, server_r_means, server_r_stds, client_r_means, client_r_stds = get_s_c_mean_sd(
        data, "total_d_rs", rs='r')
    set_sizes, server_s_means, server_s_stds, client_s_means, client_s_stds = get_s_c_mean_sd(
        data, "total_d_rs", rs='s')
    x_pos = np.arange(len(set_sizes))
    fig, ax = plt.subplots()
    client_r_means = client_r_means/1e9
    client_s_means = client_s_means/1e9
    # print(f"mean: {client_r_means[0]} single: {data[]}")
    # client_r_stds = client_r_stds/1e9
    # client_s_stds = client_s_stds/1e9

    # Add a table at the bottom of the axes
    client_r = ax.bar(x_pos-0.1, client_r_means, width=0.2, color=tableau_c10[0], align='center', alpha=0.5,
                      ecolor='black', capsize=5)
    client_s = ax.bar(x_pos+0.1, client_s_means, width=0.2, color=tableau_c10[1], align='center', alpha=0.5,
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
        batches = [data[7]]
        print(batches[0]['parameters']['server_neles'])
    translate_s = {
        'poly_trans_t': 'Polynomialtransport',
        'hashing_t': 'Hashing',
        'aby_online_t': 'ABY Online',
        'poly_t': 'Polynomial Interpolation',
        'other_t': 'Waiting',
        'aby_setup_t': 'ABY Setup',
        'aby_baseot_t': 'ABY BaseOT',
        'oprf_t': 'OPRF',
    }
    translate_c = {
        'poly_trans_t': 'Polynomialtransport',
        'hashing_t': 'Hashing',
        'aby_online_t': 'ABY Online',
        'poly_t': 'Polynomial Evaluation',
        'other_t': 'Waiting',
        'aby_setup_t': 'ABY Setup',
        'aby_baseot_t': 'ABY BaseOT',
        'oprf_t': 'OPRF',
    }
    pct_client = {
        'poly_trans_t': 0.0,
        'hashing_t': 0.0,
        'aby_online_t': 0.0,
        'poly_t': 0.0,
        'other_t': 0.0,
        'aby_setup_t': 0.0,
        'aby_baseot_t': 0.0,
        'oprf_t': 0.0,
        # 'base_t': 0.0,
    }
    pct_server = {
        'hashing_t': 0.0,
        'oprf_t': 0.0,
        'poly_trans_t': 0.0,
        'poly_t': 0.0,
        'aby_baseot_t': 0.0,
        'aby_setup_t': 0.0,
        'aby_online_t': 0.0,
        # 'base_t' : 0.0,
        'other_t': 0.0
    }
    for b in batches:
        client = {
            'hashing_t': 0,
            'oprf_t': 0,
            'poly_trans_t': 0,
            'poly_t': 0,
            'aby_baseot_t': 0,
            'aby_setup_t': 0,
            'aby_online_t': 0,

            # 'nobase_t': 0,
            'total_t': 0
        }
        server = {
            'hashing_t': 0,
            'oprf_t': 0,
            'poly_trans_t': 0,
            'poly_t': 0,
            'aby_baseot_t': 0,
            'aby_setup_t': 0,
            'aby_online_t': 0,
            # 'nobase_t': 0,
            'total_t' : 0
        }
        # sum up 
        for i in range(len(b)-1):
            for k in client:
                client[k] += b[i]['c_output'][k]
            for k in server:
                server[k] += b[i]['s_output'][k]

        # client['base_t'] = client['total_t'] - client['nobase_t']
        # server['base_t'] = server['total_t'] - server['nobase_t']
        # del client['nobase_t']
        # del server['nobase_t']

        # get average
        for k in client:
            client[k] = float(client[k])/(len(b)-1.0)

        for k in server:
            server[k] = float(server[k])/(len(b)-1.0)
        
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

    for k in translate_c:
        pct_client[translate_c[k]] = pct_client[k]
        del pct_client[k]

    for k in translate_s:
        pct_server[translate_s[k]] = pct_server[k]
        del pct_server[k]

    print(pct_client)
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    # #### For inside text!
    # wedges, texts, autotexts = ax1.pie(pct_server.values(), autopct=lambda pct: f"{pct:.1f}%",
    #                                   textprops=dict(color="w"), counterclock=False)

    # ax.legend(wedges, pct_server.keys(),
    #           title="Phases",
    #           loc="center left",
    #           bbox_to_anchor=(1, 0, 0.5, 1))

    # plt.setp(autotexts, size=8, weight="bold")

    wedges, texts, autotexts = ax.pie(pct_server.values(), colors=tableau_c10 ,autopct=lambda pct: f"{pct:.1f}%", textprops=dict(color="black"))
    # autotexts = autotexts[3:]
    ax.legend(wedges, pct_server.keys(), title="Protocol Phases", loc="center left", bbox_to_anchor=(1,0,0.5,1))
    
    # plt.setp(autotexts, size=8, weight='bold')

    ax.set_title("Server (DA): Combination of phases time-wise for the unbalanced set size 1017.\nBasic analytics circuit")

    plt.show()

def plot_psi_types_dt(data):
    set_sizes, server_means, server_stds, client_means, client_sd = get_s_c_mean_sd(
        data, "total_t", parameter='psi')
    set_sizes, server_r_means, server_r_stds, client_r_means, client_r_stds = get_s_c_mean_sd(
        data, "total_d_rs", rs='r', parameter='psi')
    set_sizes, server_s_means, server_s_stds, client_s_means, client_s_stds = get_s_c_mean_sd(
        data, "total_d_rs", rs='s', parameter='psi')
    client_means = client_means/1e3
    client_sd = client_sd/1e3
    print(client_r_means[7]+client_s_means[7])
    client_r_means = client_r_means/1e6
    client_s_means = client_s_means/1e6
    x_pos = np.array(set_sizes)
    fig, ax1 = plt.subplots()

    ax1.set_ylabel('Total data in MB')
    ax1.set_xlabel('PSI Functionalities')
    ax1.set_xticks(x_pos)
    # ax1.set_title(
    #     f"Client: Time and data for Desktop-App for different circuits. Unbalanced sets with client set size $2^{{{int(np.log2(data[0]['parameters']['client_neles']))}}}$\nTimes are the mean over {len(data[0])-1} runs with std-error.")
    labels = [Psi_type(i).name for i in set_sizes]
    ax1.set_xticklabels(labels)
    client_r = ax1.bar(x_pos-0.1, client_r_means,width=0.2, color=tableau_c10[0], align='center', alpha=0.5)
    client_s = ax1.bar(x_pos-0.1, client_s_means, width=0.2, color=tableau_c10[4], align='center', alpha=0.5, bottom=client_r_means)
    ax2 = ax1.twinx()
    ax2.set_ylabel('Runtime (seconds)', color=tableau_c10[7])
    ax2.tick_params(axis='y', labelcolor=tableau_c10[7])
    # Add a table at the bottom of the axes
    client_t = ax2.bar(x_pos+0.1, client_means, yerr=client_sd, width=0.2, color=tableau_c10[7], align='center', alpha=0.5,
                       ecolor='black', capsize=2)
    ax1.legend((client_r[0], client_s[0], client_t[0]),
               ('Client received', 'Client sent'))
    ax2.legend(['Runtime'], loc=9)

    fig.autofmt_xdate()
    fig.tight_layout()
    plt.show()


def table_psi_types_scaling_dt(data):
    table_data_1 = []
    table_data_2 = []
    for ft in [5,7,9]:
        set_sizes, server_means, server_stds, client_means, client_sd = get_specific_s_c_mean_sd(
            data, "total_t", parameter='fun_type', pfilter={'fun_type':[ft]})
        set_sizes, server_r_means, server_r_stds, client_r_means, client_r_stds = get_specific_s_c_mean_sd(
            data, "total_d_rs", rs='r', parameter='fun_type', pfilter={'fun_type': [ft]})
        set_sizes, server_s_means, server_s_stds, client_s_means, client_s_stds = get_specific_s_c_mean_sd(
            data, "total_d_rs", rs='s', parameter='fun_type', pfilter={'fun_type': [ft]})
        client_means = client_means/1e3
        client_sd = client_sd/1e3
        client_d_means = client_r_means + client_s_means
        client_d_means = client_d_means/1e6
        row_1  = []
        row_2  = []
        for i in range(len(client_means)):
            row_1.append(f"{client_means[i]:.3f}$\pm${client_sd[i]:.2f}")
            row_2.append(f"{client_d_means[i]:.3f}")
        table_data_1.append(row_1)
        table_data_2.append(row_2)
    print("runtime")
    print(print_table(table_data_1))
    print("comm")
    print(print_table(table_data_2))


def table_psi_types_phases_d(data):
    table_data = [['Phase'],['OPRF'],['Polynomials'],['Circuit'],['Circuit (Online)']]
    for sn in [2**18,2**21]:
        for ft in [5, 7, 9]:
            for b in data:
                if b['parameters']['server_neles'] != sn or b['parameters']['fun_type'] != ft:
                    continue
                else:
                    total_d = sum(b[0]['s_output']['total_d_rs'])
                    aby_d = sum(b[0]['s_output']['aby_total_d_rs'])
                    aby_online_d = sum(b[0]['s_output']['aby_online_d_rs'])
                    oprf_d = sum(b[0]['s_output']['oprf_d_rs'])
                    poly_d = sum(b[0]['s_output']['poly_d_rs'])
                    aby_d_pct = float(aby_d/total_d)*100.0
                    oprf_d_pct = float(oprf_d/total_d)*100.0 
                    print("There is a bug for the oprf_d value for AB circuits. Manual fix: count the data twice for oprf_d")
                    poly_d_pct = float(poly_d/total_d)*100.0
                    aby_online_d_pct = float(aby_online_d/total_d)*100.0
                    aby_online_aby_pct = float(aby_online_d/aby_d)*100.0
                    column_val = np.array([ft*1e6, oprf_d, poly_d, aby_d, aby_online_d])
                    column_val = column_val/1e6
                    column_pct = [ft, oprf_d_pct, poly_d_pct, aby_d_pct, aby_online_aby_pct]
                    for i in range(len(table_data)):
                        table_data[i].append(f"{column_val[i]:.1f} ({column_pct[i]:.2f}\%)")
                    
    print("comm")
    print(print_table(table_data))


   

def plot_payload_len_psi_types_dt(data):
    set_sizes_2, server_means_2, server_stds_2, client_means_2, client_sd_2 = get_specific_s_c_mean_sd(
        data, "total_t", parameter='fun_type',pfilter={'payload_bl':[2]})
    set_sizes_2, server_r_means_2, server_r_stds_2, client_r_means_2, client_r_stds_2 = get_specific_s_c_mean_sd(
        data, "total_d_rs", rs='r', parameter='fun_type',pfilter={'payload_bl':[2]})
    set_sizes_2, server_s_means_2, server_s_stds_2, client_s_means_2, client_s_stds_2 = get_specific_s_c_mean_sd(
        data, "total_d_rs", rs='s', parameter='fun_type',pfilter={'payload_bl':[2]})
    set_sizes_3, server_means_3, server_stds_3, client_means_3, client_sd_3 = get_specific_s_c_mean_sd(
        data, "total_t", parameter='fun_type',pfilter={'payload_bl':[3]})
    set_sizes_3, server_r_means_3, server_r_stds_3, client_r_means_3, client_r_stds_3 = get_specific_s_c_mean_sd(
        data, "total_d_rs", rs='r', parameter='fun_type',pfilter={'payload_bl':[3]})
    set_sizes_3, server_s_means_3, server_s_stds_3, client_s_means_3, client_s_stds_3 = get_specific_s_c_mean_sd(
        data, "total_d_rs", rs='s', parameter='fun_type',pfilter={'payload_bl':[3]})
    set_sizes_4, server_means_4, server_stds_4, client_means_4, client_sd_4 = get_specific_s_c_mean_sd(
        data, "total_t", parameter='fun_type',pfilter={'payload_bl':[4]})
    set_sizes_4, server_r_means_4, server_r_stds_4, client_r_means_4, client_r_stds_4 = get_specific_s_c_mean_sd(
        data, "total_d_rs", rs='r', parameter='fun_type',pfilter={'payload_bl':[4]})
    set_sizes_4, server_s_means_4, server_s_stds_4, client_s_means_4, client_s_stds_4 = get_specific_s_c_mean_sd(
        data, "total_d_rs", rs='s', parameter='fun_type',pfilter={'payload_bl':[4]})
    client_means_2 = client_means_2/1e3
    client_sd_2 = client_sd_2/1e3
    client_r_means_2 = client_r_means_2/1e6
    client_s_means_2 = client_s_means_2/1e6
    client_means_3 = client_means_3/1e3
    client_sd_3 = client_sd_3/1e3
    client_r_means_3 = client_r_means_3/1e6
    client_s_means_3 = client_s_means_3/1e6
    client_means_4 = client_means_4/1e3
    client_sd_4 = client_sd_4/1e3
    client_r_means_4 = client_r_means_4/1e6
    client_s_means_4 = client_s_means_4/1e6
    client_r_means_3 = client_r_means_3 - client_r_means_2
    client_s_means_3 = client_s_means_3 - client_s_means_2
    client_r_means_4 = client_r_means_4 - client_r_means_2
    client_s_means_4 = client_s_means_4 - client_s_means_2
    client_means_3 = client_means_3-client_means_2
    client_means_4 = client_means_4-client_means_2
    # client_sd_3 = client_sd_3-client_sd_2
    # client_sd_4 = client_sd_4-client_sd_2
    print(client_means_3)
    print(client_means_4)
    print(client_r_means_3+client_s_means_3)

    x_pos = np.array(set_sizes_2)
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('PSI Function Circuits')
    ax1.set_ylabel('Total data in in MegaBytes')
    ax1.set_xticks(x_pos)
    # ax1.set_title(
    #     f"Client: Time and data for Desktop-App for different circuits. Unbalanced sets with client set size $2^{{{int(np.log2(data[0]['parameters']['client_neles']))}}}$\nTimes are the mean over {len(data[0])-1} runs with std-error.")
    labels = [Psi_type(i).name for i in set_sizes_2]
    ax1.set_xticklabels(labels)
    # client_r_2 = ax1.bar(x_pos-0.1-0.3 , client_r_means_2, width=0.1,
    #                    color=tableau_c10[0], align='center', alpha=0.5)
    # client_s_2 = ax1.bar(x_pos-0.1-0.3, client_s_means_2, width=0.1,
    #                    color=tableau_c10[4], align='center', alpha=0.5, bottom=client_r_means_2)
    client_r_3 = ax1.bar(x_pos-0.1-0.3 , client_r_means_3, width=0.1,
                       color=tableau_c10[0], align='center', alpha=0.5)
    client_s_3 = ax1.bar(x_pos-0.1-0.3, client_s_means_3, width=0.1,
                       color=tableau_c10[4], align='center', alpha=0.5, bottom=client_r_means_3)
    client_r_3 = ax1.bar(x_pos-0.1+0.3, client_r_means_3, width=0.1,
                         color=tableau_c10[0], align='center', alpha=0.5)
    client_s_3 = ax1.bar(x_pos-0.1+0.3, client_s_means_3, width=0.1,
                         color=tableau_c10[4], align='center', alpha=0.5, bottom=client_r_means_3)
    ax2 = ax1.twinx()
    ax2.set_ylabel('runtime (seconds)', color=tableau_c10[7])
    ax2.tick_params(axis='y', labelcolor=tableau_c10[7])
    # Add a table at the bottom of the axes
    # client_t_2 = ax2.bar(x_pos+0.1-0.3, client_means_2, yerr=client_sd_2, width=0.1, color=tableau_c10[7], align='center', alpha=0.5,
    #                    ecolor='black', capsize=2)
    client_t_3 = ax2.bar(x_pos+0.1-0.3, client_means_3, width=0.1, color=tableau_c10[7], align='center', alpha=0.5,
                       ecolor='black', capsize=2)
    client_t_4 = ax2.bar(x_pos+0.1+0.3, client_means_4, width=0.1, color=tableau_c10[7], align='center', alpha=0.5,
                       ecolor='black', capsize=2)
    ax1.legend((client_r_3[0], client_s_3[0], client_t_3[0]),
               ('client received', 'client sent'))
    ax2.legend(['runtime'], loc=9)
    fig.tight_layout()
    fig.autofmt_xdate()
    plt.show()



if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--ten', action='store_true')
    ap.add_argument('--twelve', action='store_true')
    ap.add_argument('--both', action='store_true')
    ap.add_argument('--absum', action='store_true')
    ap.add_argument('--circuits', action='store_true')
    ap.add_argument('--phases_d', action='store_true')
    ap.add_argument('--hash', action='store_true')
    ap.add_argument('--poly_d', action='store_true')
    ap.add_argument('--payload_bl', action='store_true')
    ap.add_argument('--total_t', action='store_true')
    ap.add_argument('--total_d', action='store_true')
    ap.add_argument('--total_d_stacked', action='store_true')
    ap.add_argument('--aby_t', action='store_true')
    ap.add_argument('--pies_t', action='store_true')
    ap.add_argument('--psi_types_dt', action='store_true')
    ap.add_argument('--server_scaling_dt', action='store_true')
    args = ap.parse_args()
    if args.both:
        data10 = load_batch("Unbalanced10AnalyticsDA_2")
        data12 = load_batch("Unbalanced12AnalyticsDA_1")
        if args.all or args.total_d_stacked:
            plot_total_data_stacked_combined(data10,data12)
        if args.all or args.total_t:
            plot_total_time_combined(data10,data12)
    elif args.absum:
        data = load_batch("Unbalanced10PayloadABSumDA_1")
        if args.all or args.total_d_stacked:
            plot_total_data_absum_stacked(data)
        if args.all or args.total_t:
            plot_total_time_absum(data)
        if args.all or args.aby_t:
            plot_aby_time_absum(data)
    elif args.psi_types_dt:
        data17 = load_batch("PsiTypes1017DA_1", sort_batches="fun_type")
        data19 = load_batch("PsiTypes1019DA_1", sort_batches="fun_type")
        plot_psi_types_dt(data19)
    elif args.payload_bl:
        data = load_batch("PayloadBitlen_1019", sort_batches="fun_type")
        # for b in data:
        #     print(f"b circ{b['parameters']['fun_type']} payload{b['parameters']['payload_bl']} sn{b['parameters']['server_neles']}")
        plot_payload_len_psi_types_dt(data)
    elif args.circuits:
        data = load_batch("Circuits_Unbalanced10", important_parameters=['server_neles', 'fun_type'])
        for b in data:
            print(f"b circ{b['parameters']['fun_type']} sn{b['parameters']['server_neles']}")
        table_psi_types_scaling_dt(data)
    elif args.phases_d:
        data = load_batch("Circuits_Unbalanced10", important_parameters=[
                          'server_neles', 'fun_type'])
        for b in data:
            print(f"b circ{b['parameters']['fun_type']} sn{b['parameters']['server_neles']}")
        table_psi_types_phases_d(data)
    else:
        if args.ten:
            batch_name = "Unbalanced10AnalyticsDA_2"
        elif args.twelve:
            batch_name = "Unbalanced12AnalyticsDA_1"
        else:
            print("Please choose either --ten, --twelve or --both")
            exit(2)
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
