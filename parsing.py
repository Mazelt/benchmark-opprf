
import re

re_success_result = re.compile(
    r"PSI circuit successfully executed. Result: (?P<result>\d+)")
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

class Parser(object):

    def __init__(self, logger):
        self.logger = logger
    
    def parse_output(self, s):
        lines = s.split('\n')
        data = {}
        for l in lines:
            m = re_success_result.match(l)
            if m:
                result = int(m.group(1))
                self.logger.debug(f'Result: {result}')
                data['result'] = result
                continue
            m = re_app_result.match(l)
            if m:
                result = int(m.group(1))
                self.logger.debug(f'Result: {result}')
                data['result'] = result
                continue
            m = re_time_hashing.match(l)
            if m:
                hashing_t = float(m.group(1))
                self.logger.debug(f'Hashing time in ms: {hashing_t}')
                data['hashing'] = hashing_t
                continue
            m = re_time_oprf.match(l)
            if m:
                oprf_t = float(m.group(1))
                self.logger.debug(f'OPRF time in ms: {oprf_t}')
                data['oprf'] = oprf_t
                continue
            m = re_time_poly.match(l)
            if m:
                poly_t = float(m.group(1))
                self.logger.debug(f"Polynomials time in ms: {poly_t}")
                data['poly'] = poly_t
                continue
            m = re_time_poly_trans.match(l)
            if m:
                poly_trans_t = float(m.group(1))
                self.logger.debug(
                    f"Polynomials transmission time in ms: {poly_trans_t}")
                data['poly_trans'] = poly_trans_t
                continue
            m = re_time_aby.match(l)
            if m:
                aby_online_t = float(m.group(1))
                aby_setup_t = float(m.group(2))
                aby_total_t = float(m.group(3))
                self.logger.debug(
                    f"Aby timings in ms: online {aby_online_t}, setup {aby_setup_t}, total {aby_total_t}")
                data['aby_online'] = aby_online_t
                data['aby_setup'] = aby_setup_t
                data['aby_total'] = aby_total_t
                continue
            m = re_time_total.match(l)
            if m:
                total_t = float(m.group(1))
                self.logger.debug(f"Total time in ms: {total_t}")
                data['total'] = total_t
                continue
            m = re_time_nobase.match(l)
            if m:
                nobase_t = float(m.group(1))
                self.logger.debug(f"Total time w/o base OTs in ms: {nobase_t}")
                data['nobase'] = nobase_t
                continue
        return data
