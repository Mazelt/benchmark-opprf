import enum
import math


SERVER = 0
CLIENT = 1
SERVER_IP = '127.0.0.1'  # "192.168.0.2"
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

    def __init__(self, preset=None, psitype=Psi_type.Analytics, server_n=None):
        # all things are tailored to security parameter 40
        self.client_neles = 1024
        self.server_neles = 1024
        self.epsilon = 1.27
        self.server_ip = SERVER_IP
        self.port = 7777
        self.threads = 1
        self.threshold = 0
        self.n_fun = 3
        self.payload_bl = 2
        self.fun_type = psitype
        self.overlap = 25
        if preset == '2_12':
            self.preset2_12(server_n)
        elif preset == '2_16':
            self.preset2_16(server_n)
        elif preset == '2_20':
            self.preset2_20(server_n)
        else:
            raise f"unknonw preset {preset}"

        self.nmegabins = self.get_mega()

        self.poly_size = self.get_polys()
        self.bit_len = self.get_bitlen()

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
    
    def preset2_12(self, server_n):
        self.client_neles = 4096
        if server_n:
            self.server_neles = server_n
        else:
            self.server_neles = 4096


    def preset2_16(self, server_n):
        self.client_neles = 65536
        if server_n:
            self.server_neles = server_n
        else:
            self.server_neles = 65536

    def preset2_20(self, server_n):
        self.client_neles = 1048576
        if server_n:
            self.server_neles = server_n
        else:
            self.server_neles = 1048576

    def get_mega(self):
        if self.n_fun != 3:
            raise f"Megabin computation only for n_fun=3"
        mega_map = {
            2**10: 4,
            2**11: 8,
            2**12: 16,
            2**13: 31,
            2**14: 62,
            2**15: 124,
            2**16: 248,
            2**17: 496,
            2**18: 996, # increasing to match Pinkas et al.
            2**19: 1996,
            2**20: 4002}
        return mega_map[self.server_neles]


    def get_polys(self):
        if self.n_fun != 3:
            raise f"Polysize computation only for n_fun=3"
        polys_map = {
            2**10: 946,
            2**11: 964,
            2**12: 975,
            2**13: 1009,
            2**14: 1014,
            2**15: 1018,
            2**16: 1021,
            2**17: 1024,
            2**18: 1024,
            2**19: 1024,
            2**20: 1024}
        return polys_map[self.server_neles]

    def get_bitlen(self):
        if self.epsilon != 1.27:
            raise f"Bitlen computation only for eppsilon=1.27"
        blen = math.ceil(40 + math.log2(self.epsilon*self.client_neles))
        if blen > 61:
            raise f"ERROR: no bitlen > 61 allowd ({blen})"
        return blen
# from computations:
# n: 1024, mega: 4, psize: 946
# n: 2048, mega: 8, psize: 964
# n: 4096, mega: 16, psize: 975
# n: 8192, mega: 31, psize: 1009
# n: 16384, mega: 62, psize: 1014
# n: 32768, mega: 124, psize: 1018
# n: 65536, mega: 248, psize: 1021 # the following computations might be off.
# n: 131072, mega: 496, psize: 1024
# n: 262144, mega: 995, psize: 1024
# n: 524288, mega: 1994, psize: 1024
# n: 1048576, mega: 3998, psize: 1024
