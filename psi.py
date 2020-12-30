import enum
import math


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

    def __init__(self, preset=None, psitype=Psi_type.Analytics,client_n=1024, server_n=1024):
        # all things are tailored to security parameter 40
        self.client_neles = client_n
        self.server_neles = server_n
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
        elif preset != None:
            raise f"unknonw preset {preset}"
        if client_n != server_n:
            self.nmegabins = self.get_mega_unbalanced()
            self.poly_size = self.get_polys_unbalanced()
        else: 
            self.nmegabins = self.get_mega()
            self.poly_size = self.get_polys()
        if self.nmegabins > math.ceil(self.epsilon*self.client_neles):
            self.client_neles = math.ceil(self.nmegabins/1.27)
        self.bit_len = self.get_bitlen()


    def __str__(self):
        return f"psitype: {self.fun_type}, client_n: {self.client_neles}, server_n: 2**{math.log2(self.server_neles)}"

    def __repr__(self):
        return f"psitype: {self.fun_type}, client_n: {self.client_neles}, server_n: 2**{math.log2(self.server_neles)}"


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
            2**8: 1,
            2**9: 2,
            2**10: 4,
            2**11: 8,
            2**12: 16,
            2**13: 31,
            2**14: 62,
            2**15: 124,
            2**16: 248,
            2**17: 497,
            2**18: 996,
            2**19: 1997,
            2**20: 4006}
        return mega_map[self.server_neles]


    def get_polys(self):
        if self.n_fun != 3:
            raise f"Polysize computation only for n_fun=3"
        polys_map = {
            2**8: 769,
            2**9: 909,
            2**10: 947,
            2**11: 965,
            2**12: 976,
            2**13: 1010,
            2**14: 1015,
            2**15: 1019,
            2**16: 1022,
            2**17: 1023,
            2**18: 1024,
            2**19: 1024,
            2**20: 1024}
        return polys_map[self.server_neles]

    def get_mega_unbalanced(self):
        allowed_client_sets = [2**12, 2**10]
        if self.n_fun != 3 or self.client_neles not in allowed_client_sets:
            raise f"Megabin unbalanced computation only for n_fun=3 and client_neles in {allowed_client_sets}"
        mega_map = { 
            2**12: {
                2**12: 17,
                2**13: 32,
                2**14: 63,
                2**15: 127,
                2**16: 261,
                2**17: 521,
                2**18: 1041,
                2**19: 2601,
                2**20: 5202,
                2**21: 8035,
                2**22: 16115,
                2**23: 32321,
                2**24: 64822
                },
            2**10: {
                2**10: 5,
                2**11: 9,
                2**12: 17,
                2**13: 32,
                2**14: 66,
                2**15: 131,
                2**16: 261,
                2**17: 651,
                2**18: 1301,
                2**19: 1997,
                2**20: 4006,
                2**21: 8035,
                2**22: 16115,
                2**23: 32321,
                2**24: 64822
            }}
        return mega_map[self.client_neles][self.server_neles]

    def get_polys_unbalanced(self):
        allowed_client_sets = [2**12, 2**10]
        if self.n_fun != 3 or self.client_neles not in allowed_client_sets:
            raise f"Polysize unbalanced computation only for n_fun=3 and client_neles in {allowed_client_sets}"
        polys_map = {
            2**12: {
                2**12: 925,
                2**13: 1010,
                2**14: 1015,
                2**15: 1005,
                2**16: 980,
                2**17: 983,
                2**18: 986,
                2**19: 815,
                2**20: 817,
                2**21: 1024,
                2**22: 1024,
                2**23: 1024,
                2**24: 1024
                },
            2**10: {
                2**10: 947,
                2**11: 965,
                2**12: 976,
                2**13: 1010,
                2**14: 974,
                2**15: 977,
                2**16: 980,
                2**17: 810,
                2**18: 812,
                2**19: 1024,
                2**20: 1024,
                2**21: 1024,
                2**22: 1024,
                2**23: 1024,
                2**24: 1024
            }
            }
        return polys_map[self.client_neles][self.server_neles]

    def get_bitlen(self):
        if self.epsilon != 1.27:
            raise f"Bitlen computation only for eppsilon=1.27"
        blen1 = math.ceil(40 + math.log2(self.epsilon*self.client_neles))
        blen2 = math.ceil(40 + 2*math.log2(self.poly_size))
        blen = max(blen1, blen2)
        if blen > 61:
            raise f"ERROR: no bitlen > 61 allowed ({blen})"
        return blen
