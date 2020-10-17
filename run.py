from appium import webdriver
import os
import subprocess
import logging
from datetime import date, datetime
import sys
import threading
import time
from queue import Queue


# own libraries
from parsing import Parser
from psi import Parameters, Psi_type, SERVER, SERVER_IP, CLIENT, BIN_PATH

logger = logging.getLogger('__name__')

batch_name = 'develop'
batch = [{
    'setup': 'desktop-desktop',
    'repeat': 2,
    'parameters': Parameters()
    # todo? variable that is changed?
},
{
    'setup': 'desktop-app',
    'repeat': 1,
    'parameters': Parameters()
    # todo? variable that is changed?
}]


def run_batch():
    logger.info(f"Running a batch {batch_name}")
    logger.info(f"Batchjob contains {sum([b['repeat'] for b in batch])} runs.")
    for b in batch:
        logger.info(f"Running batch job: {b.items()}")
        repeat = b['repeat']
        del b['repeat']
        for i in range(repeat):
            run_experiment(b, i)
    logger.info("Done with batch")

def run_experiment(config, repeat):
    logger.info("== New experiment! ===================")
    parser = Parser(logger)
    paras = config['parameters']
    
    server_q = Queue()
    client_q = Queue()
    
    server_thread = threading.Thread(target=desktop_wrapper, args=(paras, BIN_PATH, server_q, SERVER))
    if config['setup'] == 'desktop-desktop':
        client_thread = threading.Thread(target=desktop_wrapper, args=(paras, BIN_PATH, client_q, CLIENT))
    elif config['setup'] == 'desktop-app':
        client_thread = threading.Thread(target=app_wrapper, args=(paras, client_q))
    else:
        logger.error(f"Unknown setup in experiment {config['setup']}")
        exit(2)
    server_thread.start()
    client_thread.start()
    server_thread.join()
    client_thread.join()
    server_output = server_q.get()
    client_output = client_q.get()
    print(parser.parse_output(server_output))
    print(parser.parse_output(client_output))
    logger.info("== Experiment done! ==================")

    
##
# CHECK: Desktop-desktop variant
# CHECK: Desktop-app variant
# CHECK: Parsing of output
# Experiment batching
# Collect network traffic (extend protocol logs)
# Collecting other information (energy?)
# save data
# create plots
##

def app_wrapper(parameters, out_queue, app_path=None):
    encoded_context = parameters.getEncodedContext()
    logger.info(f'Running app wrapper as client with context: {encoded_context}')

    desired_caps = dict(
        platformName='Android',
        orientation='PORTRAIT',
        platformVersion='9',
        automationName='uiautomator2',
        deviceName='4a1d7995',
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
    logger.info(text_output)
    out_queue.put(text_output)


def desktop_wrapper(parameters, binary_path, out_queue, role=SERVER):
    assert(isinstance(parameters, Parameters))
    assert(os.path.exists(binary_path))
    srole = "server" if role == 0 else "client"
    args = parameters.getCommandlineArgs(role)
    logger.info(f'Running desktop wrapper as {srole} with args: {args}')
    run_args = [binary_path]
    run_args.extend(args)
    process = subprocess.Popen(run_args, stdout=subprocess.PIPE, encoding='utf-8')
    output = ''
    while True:
        output_line = process.stdout.readline()
        if process.poll() is not None and output_line == '':
            break
        if output_line:
            output += output_line
            logger.info(f'{srole}   {output_line.strip()}')
    out_queue.put(output)

def setup_logger(logpath, filename):
    exp_path = os.path.join(logpath, 'experiments')
    os.makedirs(exp_path, exist_ok=True)

    logFormatter = logging.Formatter(
        "%(asctime)s [%(module)-12.12s-%(funcName)-12.12s] [%(levelname)-5.5s]  %(message)s")

    fileHandler = logging.FileHandler(f"{logpath}/{filename}")
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    filename = f"{date.today().isoformat()}.log"
    setup_logger('./logs', filename)
    # p = Parameters()
    # p.fun_type = Psi_type.Sum
    # p.overlap = 20
    # conf = {
    #     'setup': 'desktop-desktop',
    #     'parameters': p
    # }
    run_batch()
   

