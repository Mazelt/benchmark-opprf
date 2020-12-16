import numpy as np
import os.path
import glob
import json

def load_batch(pattern, silent=True,sort_batches="server_neles"):
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
    if sort_batches:
        batches = sorted(batches, key=lambda k: k['parameters'][sort_batches])
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


def get_specific_s_c_mean_std(data, key, circuit=None,  server_neles=None, parameter='server_neles', pfilter=[]):
    # data is data
    # key is the key that the mean and std is computed for
    # circuit, server_neles, 
    #   are the properties that describe the runs that will be parsed
    #   keep the one that is the 'parameter' that is dynamic as None.
    # parameter is the parameter that is the dynamic one.
    parameters = []
    server_means = []
    client_means = []
    server_stds = []
    client_stds = []
    for b in data:
        if circuit and not b['parameters']['fun_type'] == circuit:
            continue
        if server_neles and not b['parameters']['server_neles'] == server_neles:
            continue
        
        # what is the variable
        if parameter == 'server_neles':
            bpara = b['parameters']['server_neles']
            if len(pfilter) > 0:
                if bpara not in pfilter:
                    continue
            parameters.append(bpara)
        elif parameter == 'fun_type':
            bpara = b['parameters']['fun_type']
            if len(pfilter) > 0:
                if bpara not in pfilter:
                    continue
            parameters.append(bpara)
        else:
            raise f"not implemented yet for parameter {parameter}"
        s_measure = []
        c_measure = []
        # still here? then let's get some means computed.
        for i in range(len(b)-1):
            try:
                # if rs:
                #     if rs =='r':
                #         index = 0
                #     elif rs == 's':
                #         index = 1
                #     s_measure.append(b[i]['s_output'][key][index])
                #     c_measure.append(b[i]['c_output'][key][index])
                # else:
                s_measure.append(b[i]['s_output'][key])
                c_measure.append(b[i]['c_output'][key])
            except KeyError as k:
                print(f"KEYERROR for key: {key} in repeat {i} for {b['parameters']['client_neles']}")
                # raise k
        server_means.append(np.mean(s_measure))
        server_stds.append(np.std(s_measure))
        client_means.append(np.mean(c_measure))
        client_stds.append(np.std(c_measure))

    return np.array(parameters), np.array(server_means), np.array(server_stds), np.array(client_means), np.array(client_stds)


def xticks_to_potencies_label(xticks):
    potencies = [int(np.log2(x)) for x in xticks]
    return [f"$2^{{{p}}}$" for p in potencies]
