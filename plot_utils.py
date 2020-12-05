import numpy as np
import os.path
import glob
import json

def load_batch(pattern, silent=True):
    os.path.exists('./batchlogs/experiments')
    files = glob.glob(f"./batchlogs/experiments/{pattern}/Batch-{pattern}*.json")
    files = sorted(files)
    if silent:
        print(f"using pattern: {pattern}")
    else:
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
                batches.append({'parameters': b['parameters'], b['repeat']: {
                               's_output': b['s_output'], 'c_output': b['c_output']}})
    return batches
# rs is either None, 'r' or 's'


def get_s_c_mean_std(data, key, rs=None, parameter='server_set'):
    parameters = []
    server_means = []
    client_means = []
    server_stds = []
    client_stds = []
    for b in data:
        if parameter == 'server_set':
            parameters.append(b['parameters']['server_neles'])
        elif parameter == 'psi':
            parameters.append(b['parameters']['fun_type'])
        s_measure = []
        c_measure = []
        for i in range(len(b)-1):
            try:
                if rs:
                    if rs =='r':
                        index = 0
                    elif rs == 's':
                        index = 1
                    s_measure.append(b[i]['s_output'][key][index])
                    c_measure.append(b[i]['c_output'][key][index])
                else:
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
    
    return np.array(parameters), np.array(server_means), np.array(server_stds), np.array(client_means), np.array(client_stds)


def xticks_to_potencies_label(xticks):
    potencies = [int(np.log2(x)) for x in xticks]
    return [f"$2^{{{p}}}$" for p in potencies]
