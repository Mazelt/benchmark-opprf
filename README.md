# Quick Start (Experiments)
1. Install python3 requirements
2. Download appium-linux client.
3. Run appium appimage
4. Connect phone via USB with debugging enabled.
5. Configure in psi.py, prepare apk and server binary
6. Run python run.py [-b, -e]

# Quick Start (Plots)
1. Install python3 requirements (virtualenv + requirements.txt)
2. Go through the plot_(network|unbalanced).py files
3. Run the plot scripts with the desired parameters


# Source Code and Directories
## Main scripts
|`run.py`| Execute a batch, single or energy experiment. 
|`plot*`| Scripts to create plots and tables. 
|`psi.py`| Configuration and parameters for opprf_psi.
|`parsing.py`| Script to parse log files for result data.
|`maxbin.py`| Script for calculating psi parameters.

## Directories
|`batchlogs`| Logs and parsed data related to batch runs.
|`batterystats`| Battery historian data dumps and analysis.
|`logs`| Logs and parsed data related to single experiment runs.
|`network_measure`| Iperf3 json dumps and parsing for network throughput
measurements.
|`plots`| Plots of different experiments.

# Experiments and Batch Experiments
Experiments can be run once or batches can be run which consist of a list of
batch run configurations. Each configuration configures the type of setup,
number of repeats, start iteration, reset behavior, opprf_psi parameters and
network environment.

An experiment can either be desktop-desktop (only local binaries are used),
desktop-app, or desktop-manual (with app but no appium automation).
The experiment is repeated a configured number of times beginning at `start`.
The parameters objects holds all necessary opprf_psi parameters which are
automatically generated from given element numbers. The network setting is a
configuration for netem.

Normal experiment logs and parsed data is put in `logs` and batch runs are
stored in `batchlogs` under the directory with the batchname.

## Energy Consumption
Before the app started adb is used to reset its battery stats. An experiment as
run and a bugreport dump is executed which outputs a zip. This process is partly
manual since appium cannot be used when the USB cable is disconnected for
energy tests (wifi adb debugging was not investigated). The -e option of
`run.py` was used to automate the other process.
The battery historian tool is run with docker and the bugreports have been
analysed for the energy consumption of the app and CPU usage statistics. Results
were manually put in `*_data` files.


# Experiments

## Set-up
Server: Lenovo t480s
Client: OnePlus 5 (Android 9)

Wifi router with wired connection to server.
Client connected per 5GHz WiFi. 

## Batches
Topics covered:
* Unbalanced set protocol behavior
* Balanced scaling behavior
* Differences between PSI types
* Payload bitlength impact
* Network impacts and characteristic measurements
* Energy/cpu/memory usage on phone.

# Netem
using netem simulator which is part of iproute2.
https://wiki.linuxfoundation.org/networking/netem#rate_control
https://man7.org/linux/man-pages/man8/tc-netem.8.html

outbound
tc qdisc add dev $ENP root netem
* delay Xms 5ms 25%
* loss random X% 
* rate Xmbit

inbound
modprobe ifb
ip link set dev ifb0 up
tc qdisc add dev $ENP ingress
tc filter add dev $ENP parent ffff: protocol ip u32 match u32 0 0 flowid 1:1 action mirred egress redirect dev ifb0 
tc qdisc add dev ifb0 root netem
* delay Xms 5ms 25%
* rate XMbits


# Plots
For plotting the experiment data is parsed. This data was saved in the form of json files that hold the parameters and parsed results from a given run. All related json files (all runs from a batch experiment) are grouped in
 `batchlogs/experiments`. To use those results for a plot, just use the directory name as `batchname`.

`plot.py` is a legacy script which was used before the unbalanced and network scripts were introduced.

`plot_unbalanced.py` focuses on plots that handle different server set sizes (and 2 different client sets).

`plot_network.py` shows different plots for the different network environments.

`plot_utils.py` consists of utility functions that are used by the other plotting scripts.

## Usage
For each of the main plotting scripts, scroll down to the main function from which the different plots can be produced using different script parameter. The code does not use matplotlib to directly generate images, but opens the plot window where the save button can be used after the dimensions have been corrected.

### Examples

Figure 5.1:
In `plot_unbalanced.py` you can plot the communication data plot for different server sets and both client sets with `python plot_unbalanced.py --both --total_d_stacked` 
It loads the _Unbalanced10AnalyticsDA\_2_ and _Unbalanced12AnalyticsDA\_1_ experiments, uses `plot_total_data_stacked_combined()` for plotting.

Figure 5.2:
With `python plot_unbalanced.py --both --total_t` the running time for the same experiments of Figure 5.1 can be plotted. (with `--all` both plots would be generated)

Figure 5.3
`python plot_unbalanced.py --psi_types_dt` uses the PsiTypes1019DA_1 experiments.

Figure 5.4
Is the first network plot with _plot\_network.py_
`python plot_network.py --time` parses the _Network1019_* experiments for LAN, WAN and LTE_wloss.

The tables are also generated with these scripts. These methods are prefixed with _table_ and output almost correct latex tables.