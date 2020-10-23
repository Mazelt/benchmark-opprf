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

EXPERIMENT_COOLDOWN = 4

paras_n_12 = Parameters(preset='2_12')
paras_n_16 = Parameters(preset='2_16')
paras_n_20 = Parameters(preset='2_20')

batch_name = 'BetaScalingElementsDA'
batch = [
# {
#     'setup': 'desktop-app',
#     'repeat': 2,
#     'parameters': paras_n_12
# },
{
    'setup': 'desktop-app',
    'repeat': 3,
    'parameters': paras_n_16
}, 
{
    'setup': 'desktop-app',
    'repeat': 3,
    'parameters': paras_n_20
}
# {
#     'setup': 'desktop-app',
#     'repeat': 1,
#     'parameters': Parameters()
#     # todo? variable that is changed?
# }
]

class FailedExperiment(Exception):
    pass


def run_batch():
    logger.info(f"Running a batch {batch_name}")
    logger.info(f"Batchjob contains {sum([b['repeat'] for b in batch])} runs.")
    for b in batch:
        logger.info(f"Running batch job: {b.items()}")
        repeat = b['repeat']
        del b['repeat']
        for i in range(repeat):
            try:
                run_data = run_experiment(b, i)
            except FailedExperiment:
                logger.error("Failed Experiment! Continueing...")
                continue
            run_data['batch'] = batch_name
            save_data(run_data)
            logger.info(f"Waiting for experiment cooldown of {EXPERIMENT_COOLDOWN} s.")
            time.sleep(EXPERIMENT_COOLDOWN)
    logger.info("Done with batch")
    exit(0)

def run_experiment(config, repeat=None):
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
            server_q = Queue()
            client_q = Queue()
            stop_thread = False
            server_thread = threading.Thread(target=desktop_wrapper, args=(
                paras, BIN_PATH, server_q, lambda: stop_thread, SERVER))
            
            server_thread.start()
            
            if config['setup'] == 'desktop-desktop':
                desktop_wrapper(paras, BIN_PATH, client_q, CLIENT)
            elif config['setup'] == 'desktop-app':
                app_wrapper(paras, client_q)
            else:
                logger.error(f"Unknown setup in experiment {config['setup']}")
                exit(2)
            server_thread.join()
            server_output = server_q.get()
            client_output = client_q.get()
            data['s_output'] = parser.parse_output(server_output)
            data['c_output'] = parser.parse_output(client_output)
            logger.info("== Experiment done! ==================")
            retry =-1
        except Exception as e:
            logger.error(f"Caught execption {e}")
            stop_thread = True
            server_thread.join()
            if retry > 0:
                logger.info(f"Retrying!")
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

def app_wrapper(parameters, out_queue,app_path=None):
    encoded_context = parameters.getEncodedContext()
    logger.info(f'Running app wrapper as client with context: {encoded_context}')

    desired_caps = dict(
        platformName='Android',
        orientation='PORTRAIT',
        platformVersion='9',
        automationName='uiautomator2',
        deviceName='4a1d7995',
        # fullreset=True,
        app='/home/marcel/AndroidStudioProjects/OpprfPSI/app/build/outputs/apk/debug/app-debug.apk' if not app_path else app_path
    )
    logger.debug('Connecting to appium session.')
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
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
    # logger.info(text_output)
    out_queue.put(text_output)


def desktop_wrapper(parameters, binary_path, out_queue, stop, role=SERVER):
    assert(isinstance(parameters, Parameters))
    assert(os.path.exists(binary_path))
    srole = "server" if role == 0 else "client"
    args = parameters.getCommandlineArgs(role)
    logger.info(f'Running desktop wrapper as {srole} with args: {args}')
    run_args = [binary_path]
    run_args.extend(args)
    process = subprocess.Popen(run_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
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
        fname = f"Batch-{data['batch']}-Run-{data['repeat']}-{datetime.now().isoformat()}-Setup-{data['setup']}.json"  # add parameter of interest?
        fname = os.path.join('./batchlogs/experiments', fname)
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
        p = Parameters()
        p.overlap = 20
        conf = {
            'setup': 'desktop-app',
            'parameters': p
        }
        results = run_experiment(conf)
        save_data(results)


