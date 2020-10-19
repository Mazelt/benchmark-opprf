import enum


SERVER = 0
CLIENT = 1
SERVER_IP = "192.168.178.66"
BIN_PATH = '/home/marcel/repos/original-opprf/buildassociated/bin/psi_analytics_eurocrypt19_example'

class Psi_type(enum.IntEnum):
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


class Parameters(dict):

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
        self.fun_type = Psi_type.Analytics
        self.overlap = 100

    def getEncodedContext(self, role=CLIENT):
        if (role == CLIENT):
            elements = str(self.client_neles) + ";" + str(self.server_neles)
        else:
            elements = str(self.server_neles) + ";" + str(self.client_neles)
        encodedContext = ";".join((elements, str(self.bit_len), str(self.epsilon), self.server_ip,
                                   str(self.port), str(self.threads), str(
                                       self.threshold), str(self.nmegabins),
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
    
    