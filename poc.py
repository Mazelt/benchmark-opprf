from appium import webdriver
import os
import enum
import subprocess
import logging
from datetime import date, datetime
import sys
import threading
import time
from queue import Queue
import re

logger = logging.getLogger('__name__')

SERVER = 0
CLIENT = 1
SERVER_IP = "192.168.178.100"
BIN_PATH = '/home/marcel/repos/original-opprf/buildassociated/bin/psi_analytics_eurocrypt19_example'

class psi_type(enum.IntEnum):
    Analytics = 0
    Threshold = 1
    Sum = 2
    SumIfGtThreshold = 3
    PayloadASum = 4
    PayloadASumGT = 5
    PayloadABSum = 6
    PayloadABSumGT = 7
    PayloadABMulSum = 8
    PayloadABMulSumGT = 9
    
##
# CHECK: Desktop-desktop variant
# Desktop-app variant
# CHECK: Parsing of output
# Experiment batching
# Collect network traffic (extend protocol logs)
# Collecting other information (energy?)
# save data
# create plots
##


re_success_result = re.compile(r"PSI circuit successfully executed. Result: (?P<result>\d+)")
re_app_result = re.compile(r"PSI run returned: (?P<result>\d+)")
re_time_hashing = re.compile(r"Time for hashing (?P<hashing_t>\d+\.\d+) ms")
re_time_oprf = re.compile(r"Time for OPRF (?P<oprf_t>\d+\.\d+) ms")
re_time_poly = re.compile(r"Time for polynomials (?P<poly_t>\d+\.\d+) ms")
re_time_poly_trans = re.compile(
    r"Time for transmission of the polynomials (?P<poly_trans_t>\d+\.\d+) ms")
re_time_aby = re.compile(
    r"ABY timings: online time (?P<aby_online_t>\d+\.\d+) ms, setup time (?P<aby_setup_t>\d+\.\d+) ms, total time (?P<aby_total_t>\d+\.\d+) ms")
re_time_total = re.compile(r"Total runtime: (?P<total_t>\d+\.\d+)ms")
re_time_nobase = re.compile(
    r"Total runtime w/o base OTs: (?P<nobase_t>\d+\.\d+)ms")

def parse_output(s):
    lines = s.split('\n')
    data = {}
    for l in lines:
        m = re_success_result.match(l)
        if m:
            result = int(m.group(1))
            logger.debug(f'Result: {result}')
            data['result'] = result
            continue
        m = re_app_result.match(l)
        if m:
            result = int(m.group(1))
            logger.debug(f'Result: {result}')
            data['result'] = result
            continue
        m = re_time_hashing.match(l)
        if m:
            hashing_t = float(m.group(1))
            logger.debug(f'Hashing time in ms: {hashing_t}')
            data['hashing'] = hashing_t
            continue
        m = re_time_oprf.match(l)
        if m:
            oprf_t = float(m.group(1))
            logger.debug(f'OPRF time in ms: {oprf_t}')
            data['oprf'] = oprf_t
            continue
        m = re_time_poly.match(l)
        if m:
            poly_t = float(m.group(1))
            logger.debug(f"Polynomials time in ms: {poly_t}")
            data['poly'] = poly_t
            continue
        m = re_time_poly_trans.match(l)
        if m:
            poly_trans_t = float(m.group(1))
            logger.debug(f"Polynomials transmission time in ms: {poly_trans_t}")
            data['poly_trans'] = poly_trans_t
            continue
        m = re_time_aby.match(l)
        if m:
            aby_online_t = float(m.group(1))
            aby_setup_t = float(m.group(2))
            aby_total_t = float(m.group(3))
            logger.debug(f"Aby timings in ms: online {aby_online_t}, setup {aby_setup_t}, total {aby_total_t}")
            data['aby_online'] = aby_online_t
            data['aby_setup'] = aby_setup_t
            data['aby_total'] = aby_total_t
            continue
        m = re_time_total.match(l)
        if m:
            total_t = float(m.group(1))
            logger.debug(f"Total time in ms: {total_t}")
            data['total'] = total_t
            continue
        m = re_time_nobase.match(l)
        if m:
            nobase_t = float(m.group(1))
            logger.debug(f"Total time w/o base OTs in ms: {nobase_t}")
            data['nobase'] = nobase_t
            continue
    return data


class Parameters(object):

    def __init__(self):
        self.client_neles = 4096
        self.server_neles = 4096
        self.bit_len = 61
        self.epsilon = 2.4
        self.server_ip = SERVER_IP
        self.port = 7777
        self.threads = 1
        self.threshold = 0
        self.nmegabins = 16
        self.poly_size = 975
        self.n_fun = 3
        self.payload_bl = 2
        self.fun_type = psi_type.Analytics
        self.overlap = 100

    def getEncodedContext(self, role=CLIENT):
        if (role == CLIENT):
            elements = str(self.client_neles) + ";" + str(self.server_neles)
        else:
            elements = str(self.server_neles) + ";" + str(self.client_neles)
        encodedContext = ";".join((elements, str(self.bit_len), str(self.epsilon), self.server_ip,
                                   str(self.port), str(self.threads), str(self.threshold), str(self.nmegabins),
                                   str(self.poly_size), str(self.n_fun), str(self.payload_bl), str(self.fun_type.value)))
        return encodedContext

    def getCommandlineArgs(self, role):
        if (role == CLIENT):
            neles = self.client_neles
            oneles = self.server_neles
        else:
            neles = self.server_neles
            oneles = self.client_neles
        args = ['-r', str(role),
                '-n', str(neles),
                '-o', str(oneles),
                '-b', str(self.bit_len),
                '-e', str(self.epsilon),
                '-a', self.server_ip,
                '-p', str(self.port),
                '-t', str(self.threads),
                '-c', str(self.threshold),
                '-m', str(self.nmegabins),
                '-s', str(self.poly_size),
                '-f', str(self.n_fun),
                '--payload_a_bitlen', str(self.payload_bl)]
        
        if (role == SERVER):
            args.extend(['--overlap', str(self.overlap)])
        
        if self.fun_type:
            args.extend(['-y', self.fun_type.name])

        return args


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
    logger.info("== New experiment! ===================")
    paras = Parameters()

    server_q = Queue()
    # desktop_wrapper(paras, BIN_PATH, server_q, SERVER)
    client_q = Queue()
    # app_wrapper(paras, client_q)
    server_thread = threading.Thread(target=desktop_wrapper, args=(paras, BIN_PATH, server_q, SERVER))
    client_thread = threading.Thread(target=app_wrapper, args=(paras, client_q))
    server_thread.start()
    client_thread.start()
    server_thread.join()
    client_thread.join()
    server_output = server_q.get()
    client_output = client_q.get()
    print(parse_output(server_output))
    print(parse_output(client_output))
    logger.info("== Experiment done! ==================")


