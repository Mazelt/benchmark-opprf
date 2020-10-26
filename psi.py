import enum


SERVER = 0
CLIENT = 1
SERVER_IP = "192.168.0.2"  # '127.0.0.1'
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

    def __init__(self, preset=None, psitype=Psi_type.Analytics):
        self.client_neles = 1024
        self.server_neles = 1024
        self.bit_len = 51
        self.epsilon = 1.27
        self.server_ip = SERVER_IP
        self.port = 7777
        self.threads = 1
        self.threshold = 0
        self.nmegabins = 1
        self.poly_size = 0  # todo: use formula to compute sub 1024 sized polys with statistical security.
        self.n_fun = 3
        self.payload_bl = 2
        self.fun_type = psitype
        self.overlap = 25
        if preset == '2_12':
            self.preset2_12()
        elif preset == '2_16':
            self.preset2_16()
        elif preset == '2_20':
            self.preset2_20()
        else:
            raise f"unknonw preset {preset}"

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
    
    def preset2_12(self):
        self.client_neles = 4096
        self.server_neles = 4096
        self.bit_len = 53
        self.nmegabins = 16
        self.poly_size = 975


    def preset2_16(self):
        self.client_neles = 65536
        self.server_neles = 65536
        self.bit_len = 57
        self.nmegabins = 248
        self.poly_size = 1021

    def preset2_20(self):
        self.client_neles = 1048576
        self.server_neles = 1048576
        self.bit_len = 61
        self.nmegabins = 4002
        self.poly_size = 1024
