from appium import webdriver
import os
import enum
import subprocess
import logging
from datetime import date, datetime
import sys

logger = logging.getLogger('__name__')

SERVER = 0
CLIENT = 1
SERVER_IP = "127.0.0.1"
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
# Experiments Batch objects
##
# Desktop-desktop variant
##
## Parsing of app and server
##
# Collect network traffic
##
# Collecting other information (energy?)
##
# save data
##
# create plots
##

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

    def getEncodedContext(self, role):
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




def desktop_wrapper(parameters, binary_path, role=SERVER):
    assert(isinstance(parameters, Parameters))
    logger.info(f'Running desktop wrapper for role: {"Server" if role == 0 else "Client"}')
    parameters.fun_type = psi_type.PayloadABSum
    args = parameters.getCommandlineArgs(role)
    logger.info(f'  with args: {args}')
    


# desired_caps = dict(
#     platformName='Android',
#     orientation='PORTRAIT',
#     platformVersion='9',
#     automationName='uiautomator2',
#     deviceName='4a1d7995',
#     app='/home/marcel/AndroidStudioProjects/OpprfPSI/app/build/outputs/apk/debug/app-debug.apk'
# )

# driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
# el = driver.find_element_by_id('buttonclear')
# el.click()

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
    desktop_wrapper(paras, BIN_PATH, role=SERVER)
    desktop_wrapper(paras, BIN_PATH, role=CLIENT)
    logger.info("== Experiment done! ==================")
