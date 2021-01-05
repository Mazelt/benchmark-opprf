from appium import webdriver
import os
import subprocess
import logging
from datetime import date, datetime
import sys
import threading
import time
from queue import Queue
import argparse
import json


# own libraries
from parsing import Parser
from psi import Parameters, Psi_type, SERVER, SERVER_IP, CLIENT, BIN_PATH

logger = logging.getLogger('__name__')

EXPERIMENT_COOLDOWN = 3
# tc netem commands
enp = 'enp0s31f6'
# enp='lo'
tc_reset_enp_netem = f"sudo tc qdisc del dev {enp} root"
tc_add_enp = f"sudo tc qdisc add dev {enp} root netem"
tc_add_ifb = "sudo tc qdisc add dev ifb0 root netem"
tc_show_enp = f"sudo tc qdisc show dev {enp} root"
modeprobe = "sudo modprobe ifb"
ip_up = "sudo ip link set dev ifb0 up"
tc_ingress = f"sudo tc qdisc add dev {enp} ingress"
tc_filter = f"sudo tc filter add dev {enp} parent ffff: protocol ip u32 match u32 0 0 flowid 1:1 action mirred egress redirect dev ifb0"
wan_network = {'type': 'WAN', 'delay': 29, 'loss': 0.1, 'rateDown':50,'rateUp':50}
lte_network = {'type': 'LTE', 'delay': 39, 'loss': 0.1, 'rateDown': 24, 'rateUp': 4}
badlte_network = {'type': 'LTE', 'delay': 39, 'loss': 4, 'rateDown': 24, 'rateUp': 4}


# batch_name = 'Circuits_Unbalanced10'
batch_name = 'Network1019_LTE_wloss' # increase to 25 w/ start: 10
batch = [
# {
#         'setup': 'desktop-app',
#         'repeat': 20,
#         'start': 10,
#         'network': lte_network,
#         'reset': True,
#         'parameters': Parameters(client_n=2**10,server_n=2**19,psitype=Psi_type.Analytics)
#     },
#         {
#         'setup': 'desktop-app',
#         'repeat': 20,
#         'start': 10,
#         'network': lte_network,
#         'reset': True,
#         'parameters': Parameters(client_n=2**10,server_n=2**19,psitype=Psi_type.SumIfGtThreshold)
#     },
#         {
#         'setup': 'desktop-app',
#         'repeat': 20,
#         'start': 10,
#         'network': lte_network,
#         'reset': True,
#         'parameters': Parameters(client_n=2**10,server_n=2**19,psitype=Psi_type.PayloadASumGT)
#     },
    {
        'setup': 'desktop-app',
        'repeat': 20,
        'start': 19,
        'network': lte_network,
        'reset': True,
        'parameters': Parameters(client_n=2**10,server_n=2**19,psitype=Psi_type.PayloadABSumGT)
    },
    {
        'setup': 'desktop-app',
        'repeat': 20,
        'start': 18,
        'network': lte_network,
        'reset': True,
        'parameters': Parameters(client_n=2**10,server_n=2**19,psitype=Psi_type.PayloadABMulSumGT)
    },
]


class FailedExperiment(Exception):
    pass    


def init_appium(app_path=None):
    desired_caps = dict(
        platformName='Android',
        orientation='PORTRAIT',
        platformVersion='9',
        automationName='uiautomator2',
        deviceName='4a1d7995',
        # fullreset=True,
        app='/home/marcel/AndroidStudioProjects/OpprfPSI/app/build/outputs/apk/debug/app-debug.apk' if app_path == None else app_path
    )
    logger.debug('Connecting to appium session.')
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    return driver


def run_batch():
    failed = {}
    numFailed = 0
    logger.info(f"Running a batch {batch_name}")
    logger.info(f"Batchjob contains {sum([b['repeat'] for b in batch])} runs.")
    for b in batch:
        # network 
        if 'network' in b:
            network = b['network']
        else:
            network = None
        if network:
            logger.info(f"Network of type {network['type']}")
            if network['type'] == 'LAN':
                logger.info(f"LAN network does not need any configurations.")
            else:
                set_network(**network)
        if b['setup'] == 'desktop-app':
            driver = init_appium()
        else:
            driver = None
        logger.info(f"Running batch job: {b.items()}")
        repeat = b['repeat']
        start = b['start'] if 'start' in b else 0
        del b['repeat']
        for i in range(start,repeat):
            try:
                run_data = run_experiment(driver, b, i)
            except FailedExperiment:
                numFailed += 1
                fun_type = b['parameters'].fun_type
                c_num = b['parameters'].client_neles
                s_num = b['parameters'].server_neles
                if fun_type in failed:
                    failed[fun_type].append({i:{'c':c_num,'s':s_num}})
                else:
                    failed[fun_type]=[{i:{'c':c_num,'s':s_num}}]
                logger.error(f"Failed Experiment (count: {numFailed})! Continueing...")
                logger.error(failed)
                continue
            run_data['batch'] = batch_name
            save_data(run_data)
            logger.info(
                f"Waiting for experiment cooldown of {EXPERIMENT_COOLDOWN} s.")
            if driver and 'reset' in b and b['reset'] == True:
                logger.info(f"Resetting app!")
                driver.reset()
            time.sleep(EXPERIMENT_COOLDOWN)
        if driver:
            logger.info(f"Batch cooldown of {EXPERIMENT_COOLDOWN}")
            time.sleep(EXPERIMENT_COOLDOWN/2)
            driver.quit()
            time.sleep(EXPERIMENT_COOLDOWN/2)
        if network and network['type']!='LAN':
            reset_networks()
    logger.info("Done with batch")
    logger.info(failed)
    exit(0)


def run_experiment(driver, config, repeat=None):
    retry = 1
    while retry >= 0:
        try:
            logger.info("== New experiment! ===================")
            parser = Parser(logger)
            data = {}
            data['setup'] = config['setup']
            if repeat != None:
                data['repeat'] = repeat
            paras = config['parameters']
            data['parameters'] = vars(paras)
            if 'network' in config:
                data['network'] = config['network']
            server_q = Queue()
            client_q = Queue()
            stop_thread = False
            server_thread = threading.Thread(target=desktop_wrapper, args=(
                paras, BIN_PATH, server_q, lambda: stop_thread, SERVER))

            server_thread.start()

            if config['setup'] == 'desktop-desktop':
                desktop_wrapper(paras, BIN_PATH, client_q,
                                lambda: None, CLIENT)
            elif config['setup'] == 'desktop-app':
                app_wrapper(driver, paras, client_q)
            else:
                logger.error(f"Unknown setup in experiment {config['setup']}")
                exit(2)
            server_thread.join()
            server_output = server_q.get()
            client_output = client_q.get()
            data['s_output'] = parser.parse_output(server_output)
            data['c_output'] = parser.parse_output(client_output)
            logger.info("== Experiment done! ==================")
            retry = -1
        except Exception as e:
            logger.error(f"Caught execption {e}")
            stop_thread = True
            server_thread.join()
            if retry > 0:
                logger.info(f"Retrying!")
                driver.reset()
                time.sleep(EXPERIMENT_COOLDOWN)
                retry -= 1
            else:
                raise FailedExperiment()
    return data


##
# CHECK: Desktop-desktop variant
# CHECK: Desktop-app variant
# CHECK: Parsing of output
# CHECK: Experiment batching
# CHECK: save data
# CHECK: Collect network traffic (extend protocol logs)
# Collecting other information (energy?)
# create plots
##

def app_wrapper(driver, parameters, out_queue):
    encoded_context = parameters.getEncodedContext()
    logger.info(
        f'Running app wrapper as client with context: {encoded_context}')

    logger.debug('Cleaning up text in output field.')
    output = driver.find_element_by_id('textViewOUTPUT')
    output.set_text('')
    logger.debug('Setting context (encoded).')
    context_input = driver.find_element_by_id('editTextEncodedContext')
    context_input.set_text(encoded_context)
    logger.info('Starting run_psi on app with')
    run_button = driver.find_element_by_id('buttonrun')
    run_button.click()
    time.sleep(1)
    while (not run_button.is_enabled()):
        time.sleep(5)
    text_output = output.get_attribute('text')
    logger.info(text_output)
    out_queue.put(text_output)


def desktop_wrapper(parameters, binary_path, out_queue, stop, role=SERVER):
    assert(isinstance(parameters, Parameters))
    assert(os.path.exists(binary_path))
    srole = "server" if role == 0 else "client"
    args = parameters.getCommandlineArgs(role)
    logger.info(f'Running desktop wrapper as {srole} with args: {args}')
    run_args = [binary_path]
    run_args.extend(args)
    process = subprocess.Popen(
        run_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    output = ''
    while True:
        time.sleep(1)
        if stop():
            process.kill()
            break
        if process.poll() is not None:
            for line in process.stdout.readlines():
                logger.info(f'{srole}   {line.strip()}')
                output += line
            for line in process.stderr.readlines():
                logger.error(f'{srole}   {line.strip()}')
            break
    out_queue.put(output)


def reset_networks():
    logger.info("Resetting networks.")
    # checking root privileges
    ret = subprocess.run(['sudo','whoami'],capture_output=True)
    if ret.stdout!= b'root\n':
        logger.error("Please start this script as root (using sudo).")
    # reset netem
    tc_reset_netem = f"sudo tc qdisc del dev {enp} root"
    reset_args = tc_reset_netem.split()
    ret = subprocess.run(reset_args, capture_output=True, check=False)
    if ret.returncode != 0 and 'Cannot delete qdisc with handle of zero' not in str(ret.stderr):
        logger.error(str(ret.stderr))
    # reset ingress
    tc_reset_ingress = f"sudo tc qdisc del dev {enp} handle ffff: ingress"
    reset_args = tc_reset_ingress.split()
    ret = subprocess.run(reset_args, capture_output=True, check=False)
    if ret.returncode != 0 and 'Invalid handle' not in str(ret.stderr):
        logger.error(str(ret.stderr))
    # modprobe -r
    reset_args = ['sudo','modprobe', '-r', 'ifb']
    subprocess.run(reset_args,capture_output=True)
    


def set_network(type=None,delay=70,loss=0.1,rateDown=24,rateUp=4):
    logger.info(f"Setting network delay={delay}ms loss={loss}% rateDown={rateDown}mbit rateUp={rateUp}mbit.")
    delay = float(delay/2)
    # checking root privileges
    ret = subprocess.run(['sudo','whoami'],capture_output=True)
    if ret.stdout!= b'root\n':
        logger.error("Please start this script as root (using sudo).")
    # reset interface
    reset_networks()
    # add outbound
    add_args = tc_add_enp.split()
    options = ""
    if delay:
        options = f"{options} delay {delay}ms 5ms 25%"
    if loss:
        options = f"{options} loss random {loss}%"
    if rateDown:
        options = f"{options} rate {rateDown}mbit"
    
    add_args.extend(options.split())
    ret = subprocess.run(add_args, check=True)

    ret = subprocess.run(tc_show_enp.split(), capture_output=True)
    logger.info(f"Tc qdisc show: {ret.stdout}")
    # add inbound
    # modprobe ifb
    subprocess.run(modeprobe.split(), check=True)
    # ip link set dev ifb0 up
    subprocess.run(ip_up.split(), check=True)
    # tc qdisc add dev {enp} ingress
    subprocess.run(tc_ingress.split(), check=True)
    # tc filter add dev $ENP parent ffff: protocol ip u32 match u32 0 0 flowid 1:1 action mirred egress redirect dev ifb0
    subprocess.run(tc_filter.split(), check=True)
    add_args = tc_add_ifb.split()
    options = ""
    if delay:
        options = f"{options} delay {delay}ms 5ms 25%"
    if loss:
        options = f"{options} loss random {loss}%"
    if rateUp:
        options = f"{options} rate {rateUp}mbit"
    add_args.extend(options.split())
    ret = subprocess.run(add_args, check=True)


def setup_logger(logpath, filename):
    exp_path = os.path.join(logpath, 'experiments')
    os.makedirs(exp_path, exist_ok=True)

    logFormatter = logging.Formatter(
        "%(asctime)s [%(module)-8.8s-%(funcName)-12.12s] [%(levelname)-5.5s]  %(message)s")

    fileHandler = logging.FileHandler(f"{logpath}/{filename}")
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    logger.setLevel(logging.DEBUG)


def save_data(data):
    if 'batch' in data:
        # add parameter of interest?
        fname = f"Batch-{data['batch']}-Run-{data['repeat']}-{datetime.now().isoformat()}-Setup-{data['setup']}.json"
        dirname = os.path.join(f"./batchlogs/experiments/",batch_name)
        os.makedirs(dirname,exist_ok=True)
        fname = os.path.join(dirname, fname)
    else:
        fname = f"{datetime.now().isoformat()}-Setup-{data['setup']}.json"
        fname = os.path.join('./logs/experiments', fname)

    if os.path.exists(fname):
        logger.warn(f'Filename {fname} already exists!')
        fname = fname + '.collision'
    logger.info(f'Saving data to file {fname}.')
    with open(fname, 'w') as fp:
        json.dump(data, fp)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Run opprf experiments.')
    ap.add_argument('-b', '--batch', dest='batch_run', action='store_true')

    args = ap.parse_args()

    if args.batch_run:
        filename = f"{date.today().isoformat()}.log"
        setup_logger('./batchlogs', filename)
        logger.info('This is a batch run')
        run_batch()
        exit(0)
    else:
        filename = f"{date.today().isoformat()}.log"
        setup_logger('./logs', filename)
        p = Parameters(client_n=2**10,server_n=2**19, psitype=Psi_type.SumIfGtThreshold)
        p.overlap = 20
        # lte_network['loss'] = None
        # lte_network['rateUp'] = None
        # lte_network['rateDown'] = None
        conf = {
            'setup': 'desktop-app',
            'parameters': p,
            # 'network': wan_network
        }
        if 'network' in conf:
            network = conf['network']
        else:
            network = None

        if network:
            logger.info(f"Network of type {network['type']}")
            if network['type'] == 'LAN':
                logger.info(f"LAN network does not need any configurations.")
            else:
                set_network(**network)
        inp = input('press enter to stop')
        
        if conf['setup'] == 'desktop-app':
            driver = init_appium()
        else:
            driver = None
        results = run_experiment(driver, conf)
        save_data(results)
        if driver:
            driver.quit()
        if network and network['type']!='LAN':
            reset_networks()
