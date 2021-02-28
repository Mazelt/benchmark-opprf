import json
import numpy as np


def get_tps(file_name):
    with open(f'./{file_name}', 'r') as fp:
        data = json.load(fp)

    tps = []

    # remove ramp-up phase and get only 25 runs
    start = 10
    max_v = 35
    for i, inter in enumerate(data['intervals']):
        if i < start:
            continue
        elif i == max_v:
            break
        tps.append(inter['sum']['bits_per_second']/1e6)

    print(f"{file_name} Measures: {len(tps)}, Avg: {np.mean(tps):.2f} Mbit/s, SD: {np.std(tps):0.4f}")

fnames = ["LAN_2500_c.json","LAN_2500_s.json","WAN_500_c.json","WAN_500_s.json","LTE_50_c.json","LTE_50_s.json"]

for f in fnames:
    get_tps(f)