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

def plot_total_time(datalan, datawan, datalte):

    set_sizes_lan, server_means_lan, server_stds_lan, client_means_lan, client_stds_lan = \
        get_specific_s_c_mean_sd(datalan, 'total_t', server_neles=2**19, parameter='fun_type', pfilter={'fun_type':[3,5,7,9]})
    set_sizes_wan, server_means_wan, server_stds_wan, client_means_wan, client_stds_wan = \
        get_specific_s_c_mean_sd(datawan, 'total_t', server_neles=2**19, parameter='fun_type', pfilter={'fun_type':[3,5,7,9]})
    set_sizes_lte, server_means_lte, server_stds_lte, client_means_lte, client_stds_lte = \
        get_specific_s_c_mean_sd(datalte, 'total_t', server_neles=2**19 , parameter='fun_type', pfilter={'fun_type':[3,5,7,9]})
    x_pos = np.array(set_sizes_lan)
    labels = [Psi_type(i).name for i in set_sizes_lan]
    client_means_lan = client_means_lan/1e3
    client_stds_lan = client_stds_lan/1e3
    client_means_wan = client_means_wan/1e3
    client_stds_wan = client_stds_wan/1e3
    client_means_lte = client_means_lte/1e3
    client_stds_lte = client_stds_lte/1e3
    fig, ax = plt.subplots()
    client_lan = ax.bar(x_pos-0.4, client_means_lan, yerr=client_stds_lan, color=tableau_c10[1], align='center', alpha=0.5, width=0.3,
           ecolor='black', capsize=2)
    client_wan = ax.bar(x_pos, client_means_wan, yerr=client_stds_wan, color=tableau_c10[0], align='center', alpha=0.5, width=0.3,
                        ecolor='black', capsize=2)
    client_lte = ax.bar(x_pos+0.4, client_means_lte, yerr=client_stds_lte, color=tableau_c10[2], align='center', alpha=0.5, width=0.3,
           ecolor='black', capsize=2)
    ax.set_ylabel(f"Total time in seconds")
    ax.set_xticks(x_pos)
    # ax.set_title(
    #     f"Client: Total time for Desktop-App with different networks.\nUnbalanced sets with client set size $2^{{{int(np.log2(datalan[0]['parameters']['client_neles']))}}}$ and the basic analytics circuit.\nMean over {len(datalan[0])-1} runs with std-error.")
    ax.yaxis.grid(True)
    ax.set_xlabel('PSI Functionalities')
    ax.set_xticklabels(labels)
    ax.legend((client_lan[0], client_wan[0], client_lte[0]),('LAN','WAN','LTE'))

    fig.autofmt_xdate()
    plt.tight_layout()
    plt.show()

def table_time_phases(data):
    table_data = [['Phase'], ['hashing'],['OPRF'], ['Poly int'],
                  ['Poly transm'], ['Poly eval'], ['Circuit'],['Waiting']]

    c_total_t_means = [] # hashing+oprf+ (pint)+(s_ptrans)+polyt + aby_t
    c_hashing_t_means = []
    c_oprf_t_means = []
    c_poly_t_means = []
    c_aby_t_means = []
    c_aby_bot_t_means = []

    s_total_t_means = []  # hashing+oprf+ poly_t +ptrans+ (peval) + aby_t
    s_hashing_t_means = []
    s_oprf_t_means = []
    s_poly_t_means = []
    s_poly_trans_t_means = []
    s_aby_t_means = []
    s_aby_bot_t_means = []
    
    for ft in [5]:  # , 7, 9
        for b in data:
            if b['parameters']['server_neles'] != 2**19 or b['parameters']['fun_type'] != ft:
                continue
            else:
                c_total_t = []
                c_hashing_t = []
                c_oprf_t = []
                c_poly_t = []
                c_aby_t = []
                c_aby_bot_t = []

                s_total_t = []
                s_hashing_t = []
                s_oprf_t = []
                s_poly_t = []
                s_poly_trans_t = []
                s_aby_t = []
                s_aby_bot_t = []
                for r in range(len(b)-1):
                    repeat_c = b[r]['c_output']
                    repeat_s = b[r]['s_output']
                    c_total_t.append(repeat_c['total_t'])
                    c_hashing_t.append(repeat_c['hashing_t'])
                    c_oprf_t.append(repeat_c['oprf_t'])
                    c_poly_t.append(repeat_c['poly_t'])
                    c_aby_t.append(repeat_c['aby_total_t'])
                    c_aby_bot_t.append(repeat_c['aby_baseot_t'])

                    s_total_t.append(repeat_s['total_t'])
                    s_hashing_t.append(repeat_s['hashing_t'])
                    s_oprf_t.append(repeat_s['oprf_t'])
                    s_poly_t.append(repeat_s['poly_t'])
                    s_poly_trans_t.append(repeat_s['poly_trans_t'])
                    s_aby_t.append(repeat_s['aby_total_t'])
                    s_aby_bot_t.append(repeat_s['aby_baseot_t'])

                c_total_t_means.append(np.mean(c_total_t))
                c_hashing_t_means.append(np.mean(c_hashing_t))
                c_oprf_t_means.append(np.mean(c_oprf_t))
                c_poly_t_means.append(np.mean(c_poly_t))
                c_aby_t_means.append(np.mean(c_aby_t))
                c_aby_bot_t_means.append(np.mean(c_aby_bot_t))

                s_total_t_means.append(np.mean(s_total_t))
                s_hashing_t_means.append(np.mean(s_hashing_t))
                s_oprf_t_means.append(np.mean(s_oprf_t))
                s_poly_t_means.append(np.mean(s_poly_t))
                s_poly_trans_t_means.append(np.mean(s_poly_trans_t))
                s_aby_t_means.append(np.mean(s_aby_t))
                s_aby_bot_t_means.append(np.mean(s_aby_bot_t))


                # aby_d_pct = float(aby_d/total_d)*100.0
                # oprf_d_pct = float(oprf_d/total_d)*100.0 
                # print("There is a bug for the oprf_d value for AB circuits. Manual fix: count the data twice for oprf_d")
                # poly_d_pct = float(poly_d/total_d)*100.0
                # column_val = np.array([ft*1e6, oprf_d, poly_d, aby_d])
                # column_val = column_val/1e6
                # column_pct = [ft, oprf_d_pct, poly_d_pct, aby_d_pct]
                # for i in range(len(table_data)):
                #     table_data[i].append(f"{column_val[i]:.1f} ({column_pct[i]:.2f}\%)")
    for i in range(len(c_total_t_means)):
        #c_total= hashing+oprf+ (pint)+(s_ptrans)+polyt + aby_t
        print("client")
        print(f"{c_hashing_t_means[i]} + {c_oprf_t_means[i]} (pint) (s_ptrans) {c_poly_t_means[i]} + {c_aby_t_means[i]+c_aby_bot_t_means[i]}")
        print(
            f"{c_total_t_means[i]}-all = {c_total_t_means[i]-(c_hashing_t_means[i] + c_oprf_t_means[i]+s_poly_t_means[i]+s_poly_trans_t_means[i]+ c_poly_t_means[i] + c_aby_t_means[i]+c_aby_bot_t_means[i])}")

        print("server")
        print(
            f"{s_hashing_t_means[i]} + {s_oprf_t_means[i]} + {s_poly_t_means[i]}  +{s_poly_trans_t_means[i]}+ (peval)+ {s_aby_t_means[i]+s_aby_bot_t_means[i]}")
        print(
            f"{s_total_t_means[i]}-all = {s_total_t_means[i]-(s_hashing_t_means[i] + s_oprf_t_means[i]+s_poly_t_means[i]+s_poly_trans_t_means[i]+ s_poly_t_means[i] +c_poly_t_means[i]+ s_aby_t_means[i]+s_aby_bot_t_means[i])}")

def plot_total_data(datalan, datawan, datalte):

    set_sizes_r_lan, server_means_r_lan, _, client_means_r_lan, _ = \
        get_specific_s_c_mean_sd(
            datalan, 'total_d_rs', rs='r', server_neles=2 **
            19, parameter='fun_type', pfilter={'fun_type': [3,5, 7, 9]})
    set_sizes_s_lan, server_means_s_lan, _, client_means_s_lan, _ = \
        get_specific_s_c_mean_sd(
            datalan, 'total_d_rs', rs='s', server_neles=2 **
            19, parameter='fun_type', pfilter={'fun_type': [3,5, 7, 9]})
    
    set_sizes_r_wan, server_means_r_wan, _, client_means_r_wan, _ = \
        get_specific_s_c_mean_sd(datawan, 'total_d_rs', rs='r', server_neles=2 **
                                 19, parameter='fun_type', pfilter={'fun_type': [3,5, 7, 9]})
    set_sizes_s_wan, server_means_s_wan, _, client_means_s_wan, _ = \
        get_specific_s_c_mean_sd(datawan, 'total_d_rs', rs='s', server_neles=2 **
                                 19, parameter='fun_type', pfilter={'fun_type': [3,5, 7, 9]})

    set_sizes_r_lte, server_means_r_lte, _, client_means_r_lte, _ = \
        get_specific_s_c_mean_sd(datalte, 'total_d_rs', rs='r', server_neles=2 **
                                 19, parameter='fun_type', pfilter={'fun_type': [3,5, 7, 9]})
    set_sizes_s_lte, server_means_s_lte, _, client_means_s_lte, _ = \
        get_specific_s_c_mean_sd(datalte, 'total_d_rs', rs='s', server_neles=2 **
                                 19, parameter='fun_type', pfilter={'fun_type': [3,5, 7, 9]})

    x_pos = np.array(set_sizes_r_lan)
    labels = [Psi_type(i).name for i in set_sizes_r_lan]
    client_means_r_lan = client_means_r_lan/1e6
    client_means_r_wan = client_means_r_wan/1e6
    client_means_r_lte = client_means_r_lte/1e6
    client_means_s_lan = client_means_s_lan/1e6
    client_means_s_wan = client_means_s_wan/1e6
    client_means_s_lte = client_means_s_lte/1e6
    fig, ax = plt.subplots()
    client_r_lan = ax.bar(x_pos-0.2, client_means_r_lan, color=tableau_c10[0], align='center', alpha=0.5,width=0.2)
    client_s_lan = ax.bar(x_pos-0.2, client_means_s_lan, color=tableau_c10[4], align='center', alpha=0.5,width=0.2, bottom=client_means_r_lan)

    client_r_wan = ax.bar(x_pos, client_means_r_wan, color=tableau_c10[0], align='center', alpha=0.5,width=0.2)
    client_s_wan = ax.bar(x_pos, client_means_s_wan, color=tableau_c10[4], align='center', alpha=0.5,width=0.2,bottom=client_means_r_wan)
    
    client_r_lte = ax.bar(x_pos+0.2, client_means_r_lte, color=tableau_c10[0], align='center', alpha=0.5,width=0.2)
    client_s_lte = ax.bar(x_pos+0.2, client_means_s_lte, color=tableau_c10[4], align='center', alpha=0.5,width=0.2, bottom=client_means_r_lte)
    ax.set_ylabel(f"Total time in in seconds")
    ax.set_xticks(x_pos)
    # ax.set_title(
    #     f"Client: Total time for Desktop-App with different networks.\nUnbalanced sets with client set size $2^{{{int(np.log2(datalan[0]['parameters']['client_neles']))}}}$ and the basic analytics circuit.\nMean over {len(datalan[0])-1} runs with std-error.")
    ax.yaxis.grid(True)
    ax.set_xlabel('PSI Function Circuits')
    ax.set_xticklabels(labels)
    # ax.legend((client_r_lan[0], client_r_wan[0],
    #            client_r_lte[0]), ('LAN', 'WAN', 'LTE'))
    plt.tight_layout()
    fig.autofmt_xdate()
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
    ap.add_argument('--time', action='store_true')
    ap.add_argument('--aby_t', action='store_true')
    ap.add_argument('--pies_t', action='store_true')
    ap.add_argument('--phases_t', action='store_true')
    args = ap.parse_args()
    
    if args.rtts:
        batch = load_batch('NetworkDebugging_NewRTTs_LTE')
        get_rtt(batch)
    elif args.tps:
        batch = load_batch('NetworkDebugging_NewRTTs_LTE')
        get_tp(batch)
    elif args.phases_t:
        batch_10_LAN = load_batch('Network1019_LAN')
        batch_10_WAN = load_batch('Network1019_WAN')
        batch_10_LTE = load_batch('Network1019_LTE')
        table_time_phases(batch_10_LAN)
    elif args.time:

        batch_10_LAN = load_batch('Network1019_LAN')
        batch_10_WAN = load_batch('Network1019_WAN')
        batch_10_LTE = load_batch('Network1019_LTE')
        
        plot_total_time(batch_10_LAN, batch_10_WAN, batch_10_LTE)
        # plot_total_data(batch_10_LAN,batch_10_WAN,batch_10_LTE)
    else:
        print('nothing to do...')
