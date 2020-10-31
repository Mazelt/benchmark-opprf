
import re

re_success_result = re.compile(
    r"PSI circuit successfully executed. Result: (?P<result>\d+)")
re_app_result = re.compile(r"PSI run returned: (?P<result>\d+)")
re_time_hashing = re.compile(r"Time for hashing (?P<hashing_t>\d+(\.\d*)?) ms")
re_time_oprf = re.compile(r"Time for OPRF (?P<oprf_t>\d+(\.\d*)?) ms")
re_time_poly = re.compile(r"Time for polynomials (?P<poly_t>\d+(\.\d*)?) ms")
re_time_poly_trans = re.compile(
    r"Time for transmission of the polynomials (?P<poly_trans_t>\d+(\.\d*)?) ms")
re_time_aby = re.compile(
    r"ABY timings: online time (?P<aby_online_t>\d+(\.\d*)?) ms, setup time (?P<aby_setup_t>\d+(\.\d*)?) ms, total time (?P<aby_total_t>\d+(\.\d*)?) ms, base OTs time (?P<aby_baseot_t>\d+(\.\d*)?) ms")
re_time_total = re.compile(r"Total runtime: (?P<total_t>\d+(\.\d*)?)ms")
re_time_nobase = re.compile(
    r"Total runtime w/o base OTs: (?P<nobase_t>\d+(\.\d*)?)ms")
re_comm_poly = re.compile(
    r"Data for polynomials recv/sent (?P<recv>\d+) / (?P<sent>\d+) b")
re_comm_oprf = re.compile(
    r"Data for oprf recv/sent (?P<recv>\d+) / (?P<sent>\d+) b")
re_comm_aby_recv = re.compile(
    r"ABY recv: online (?P<online>\d+) bytes, setup (?P<setup>\d+) bytes, total (?P<total>\d+) bytes, base OTs (?P<baseot>\d+) bytes")
re_comm_aby_sent = re.compile(
    r"ABY sent: online (?P<online>\d+) bytes, setup (?P<setup>\d+) bytes, total (?P<total>\d+) bytes, base OTs (?P<baseot>\d+) bytes")
re_comm_total_recv = re.compile(r"Total recv: (?P<recv>\d+) bytes")
re_comm_total_sent = re.compile(r"Total sent: (?P<sent>\d+) bytes")
re_comm_nobase_recv = re.compile(r"Total recv w/o base OTs: (?P<recv>\d+) b")
re_comm_nobase_sent = re.compile(
    r"Total sent w/o base OTs: (?P<sent>\d+) b")
class Parser(object):

    def __init__(self, logger):
        self.logger = logger
    
    def parse_output(self, s):
        lines = s.split('\n')
        data = {}
        for l in lines:
            m = re_success_result.match(l)
            if m:
                result = int(m.group('result'))
                self.logger.debug(f'Result: {result}')
                data['result'] = result
                continue
            m = re_app_result.match(l)
            if m:
                result = int(m.group('result'))
                self.logger.debug(f'Result: {result}')
                data['result'] = result
                continue
            m = re_time_hashing.match(l)
            if m:
                hashing_t = float(m.group('hashing_t'))
                self.logger.debug(f'Hashing time in ms: {hashing_t}')
                data['hashing_t'] = hashing_t
                continue
            m = re_time_oprf.match(l)
            if m:
                oprf_t = float(m.group('oprf_t'))
                self.logger.debug(f'OPRF time in ms: {oprf_t}')
                data['oprf_t'] = oprf_t
                continue
            m = re_time_poly.match(l)
            if m:
                poly_t = float(m.group('poly_t'))
                self.logger.debug(f"Polynomials time in ms: {poly_t}")
                data['poly_t'] = poly_t
                continue
            m = re_time_poly_trans.match(l)
            if m:
                poly_trans_t = float(m.group('poly_trans_t'))
                self.logger.debug(
                    f"Polynomials transmission time in ms: {poly_trans_t}")
                data['poly_trans_t'] = poly_trans_t
                continue
            m = re_time_aby.match(l)
            if m:
                aby_online_t = float(m.group('aby_online_t'))
                aby_setup_t = float(m.group('aby_setup_t'))
                aby_total_t = float(m.group('aby_total_t'))
                aby_baseot_t = float(m.group('aby_baseot_t'))
                self.logger.debug(
                    f"Aby timings in ms: online {aby_online_t}, setup {aby_setup_t}, total {aby_total_t}, baseot {aby_baseot_t}")
                data['aby_online_t'] = aby_online_t
                data['aby_setup_t'] = aby_setup_t
                data['aby_total_t'] = aby_total_t
                data['aby_baseot_t'] = aby_baseot_t
                continue
            m = re_time_total.match(l)
            if m:
                total_t = float(m.group('total_t'))
                self.logger.debug(f"Total time in ms: {total_t}")
                data['total_t'] = total_t
                continue
            m = re_time_nobase.match(l)
            if m:
                nobase_t = float(m.group('nobase_t'))
                self.logger.debug(f"Total time w/o base OTs in ms: {nobase_t}")
                data['nobase_t'] = nobase_t
                continue
            m = re_comm_poly.match(l)
            if m:
                poly_d_r = int(m.group('recv'))
                poly_d_s = int(m.group('sent'))
                self.logger.debug(f"Polynomials data recv/sent in bytes: {poly_d_r}/{poly_d_s}")
                data['poly_d_rs'] = [poly_d_r , poly_d_s]
                continue
            m = re_comm_oprf.match(l)
            if m:
                oprf_d_r = int(m.group('recv'))
                oprf_d_s = int(m.group('sent'))
                self.logger.debug(
                    f"Oprf data recv/sent in bytes: {oprf_d_r}/{oprf_d_s}")
                data['oprf_d_rs'] = [oprf_d_r, oprf_d_s]
                continue
            m = re_comm_aby_recv.match(l)
            if m:
                aby_online_d_r = int(m.group('online'))
                aby_setup_d_r = int(m.group('setup'))
                aby_total_d_r = int(m.group('total'))
                aby_baseot_d_r = int(m.group('baseot'))
                self.logger.debug(
                    f"Aby data recv in bytes: online {aby_online_d_r}, setup {aby_setup_d_r}, total {aby_total_d_r}, baseot {aby_baseot_d_r}")
                data['aby_online_d_rs'] = [aby_online_d_r]
                data['aby_setup_d_rs'] = [aby_setup_d_r]
                data['aby_total_d_rs'] = [aby_total_d_r]
                data['aby_baseot_d_rs'] = [aby_baseot_d_r]
                continue
            m = re_comm_aby_sent.match(l)
            if m:
                aby_online_d_s = int(m.group('online'))
                aby_setup_d_s = int(m.group('setup'))
                aby_total_d_s = int(m.group('total'))
                aby_baseot_d_s = int(m.group('baseot'))
                self.logger.debug(
                    f"Aby data sent in bytes: online {aby_online_d_s}, setup {aby_setup_d_s}, total {aby_total_d_s}, baseot {aby_baseot_d_r}")
                data['aby_online_d_rs'].append(aby_online_d_s)
                data['aby_setup_d_rs'].append(aby_setup_d_s)
                data['aby_total_d_rs'].append(aby_total_d_s)
                data['aby_baseot_d_rs'].append(aby_baseot_d_s)
                continue
            m = re_comm_total_recv.match(l)
            if m:
                total_d_r = int(m.group('recv'))
                self.logger.debug(
                    f"Total data recv in bytes: {total_d_r}")
                data['total_d_rs'] = [total_d_r]
                continue
            m = re_comm_total_sent.match(l)
            if m:
                total_d_s = int(m.group('sent'))
                self.logger.debug(
                    f"Total data sent in bytes: {total_d_s}")
                data['total_d_rs'].append(total_d_s)
                continue
            m = re_comm_nobase_recv.match(l)
            if m:
                nobase_d_r = int(m.group('recv'))
                self.logger.debug(
                    f"Nobase data recv in bytes: {nobase_d_r}")
                data['nobase_d_rs'] = [nobase_d_r]
                continue
            m = re_comm_nobase_sent.match(l)
            if m:
                nobase_d_s = int(m.group('sent'))
                self.logger.debug(
                    f"Nobase data sent in bytes: {nobase_d_s}")
                data['nobase_d_rs'].append(nobase_d_s)
                continue
        return data


if __name__ == '__main__':
    to_parse = "PSI circuit successfully executed. Result: 0\n" + \
    "Time for hashing 6.59715 ms\n" + \
    "Time for OPRF 452.343 ms\n" + \
    "Time for polynomials 365.963 ms\n" + \
    "Time for transmission of the polynomials 0.072548 ms\n" + \
    "ABY timings: online time 2.669 ms, setup time 88.571 ms, total time 91.24 ms, base OTs time 222.2 ms\n" + \
    "Total runtime: 1250.27ms\n" + \
    "Total runtime w/o base OTs: 583.952ms\n" + \
    "Data for polynomials recv/sent 0 / 124800 b\n" + \
    "Data for oprf recv/sent 332961 / 16944 b\n" + \
    "ABY recv: online 117750 bytes, setup 4995165 bytes, total 5112915 bytes, base OTs 43434 bytes\n" + \
    "ABY sent: online 117750 bytes, setup 4995165 bytes, total 5112915 bytes, base OTs 43434 bytes\n" + \
    "Total recv: 5445876 bytes\n" + \
    "Total sent: 5254659 bytes\n" + \
    "Total recv w/o base OTs: 5395847 b\n" + \
    "Total sent w/o base OTs: 5187803 b\n"
    print(to_parse)
    import logging
    logger = logging.getLogger('__name__')

    parser = Parser(logger)
    data = parser.parse_output(to_parse)
    print(data)
