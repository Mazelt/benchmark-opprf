from scipy.stats import binom
from numpy import log2
from math import ceil,floor
from  mpmath import mp
mp.dps = 50

def p2(b,n, max_b):
    smaller = binom.cdf(max_b-1,n,1/b)
    bigger = binom.cdf(n,n,1/b)
    res = bigger - smaller
    # for i in range(max_b,n+1):
    #     res += binom.pmf(i, n, 1/b)

    return b * res

def p(B, N, maxb):
    summ = mp.mpf(0.0)
    for i in range(maxb, N+1):
        c = mp.power(mp.mpf(1.0-(1.0/B)), (N-i))
        # print(c)
        b = mp.power(mp.mpf(1.0/B), i)
        # print(b)
        a = mp.binomial(N,i)
        # print(a)
        z = mp.fmul(a, mp.fmul(b, c))
        # print(z)
        y = mp.fmul(B,z)
        # print(y)
        summ = mp.fadd(summ,y)
        if i>2*maxb and i % maxb == 0:
            # print(f"i:{i} summ: {summ} y{y}")
            if y < mp.mpf(2**-60):
                return summ
    return summ

def is_small(x,nabla):
    if x < 2**(-nabla):
        return True
    else:
        return False
        # return x - 2**(-nabla)

def maxbins(cpot,spot):
    nabla = 40
    n1 = 2**spot
    n2 = 2**cpot
    n = 3*n1
    b = 1.27*n2
    max_b = int(n/b)
    prob = p(b, n, max_b)
    while prob > 2**(-nabla):
        max_b += 1
        prob = p(b, n, max_b)
    return max_b

def megabins(cpot, spot, limit=1024):
    nabla = 40
    n1 = 2**spot
    n2 = 2**cpot
    n = 3*n1
    m = 1
    beta = 1.27*n2
    max_bstart = 900
    max_b = max_bstart
    prob = p(m, n, max_b)
    while prob > 2**(-nabla):
        if max_b < limit or m*2>=beta:
            max_b +=1
        else:
            m += 1
            max_b = max_bstart
        prob = p(m, n, max_b)

    return m, max_b


def megabinsBeta(m, cpot, spot, max_bstart=900, limit=1024):
    nabla = 40
    n1 = 2**spot
    n2 = 2**cpot
    n = 3*n1
    m = m
    beta = ceil(1.27*n2)
    max_b = max_bstart
    prob = p(m, n, max_b)
    # print(prob)
    while prob > 2**(-nabla):
        if max_b < limit:
            max_b += 1
        else:
            m += 1
            max_b = max_bstart
        prob = p(m, n, max_b)
        # print(prob)
        # print(f"m:{m},maxb{max_b} prob {prob}")

    if m > beta:
        beta = m

    
    nbinsinmega = ceil(beta/m)
    mstrich = floor(beta/nbinsinmega)
    prob2 = p(mstrich, n, max_b)
    while prob2 > 2**-40:
        m+=1
        nbinsinmega = ceil(beta/m)
        mstrich = floor(beta/nbinsinmega)
        prob2 = p(mstrich, n, max_b)
    
    while prob < 2**-40 and prob2 < 2**-40:
        max_b -=1
        prob = p(m, n, max_b)
        nbinsinmega = ceil(beta/m)
        mstrich = floor(beta/nbinsinmega)
        prob2 = p(mstrich, n, max_b)
    if prob > 2**-40 or prob2 > 2**-40:
        max_b += 1
    if m > beta:
        beta = m
    return m, max_b, beta

# print(f"Big steps stopped at {max_b}")

# while not is_small(p(b, n, max_b-20)):
#     max_b += 1

# print(maxbins(12,12))
# for i in range(11,21):
#     print(maxbins(10,i))

def get_balanced():
    client = 10
    m = 2
    print(f"Get balanced {client}")
    for i in range(10,21):
        maxbstart = {
            10:945,
            11:963,
            12:974,
            13:1008,
            14:1013,
            15:1017,
            16:1020,
            17:1021,
            18:1023,
            19:1024,
            20:1024}
        mstart = {
            10:3,
            11:6,
            12:14,
            13:29,
            14:60,
            15:122,
            16:246,
            17:495,
            18:994,
            19:1995,
            20:4001
        }
        # m, max_b = megabins(10,i)
        # print(f"{i} - m:{m}, max_b: {max_b}")
        m, max_b, beta = megabinsBeta(
            mstart[i], i, i, max_bstart=maxbstart[i])
        print(f"{i} - m:{m}, max_b: {max_b}, epsilon: {beta/(1.27*2**i)} {40+log2(beta)<= 61}")
    # m = int(1.5*m)


def get_unbalanced():
    client = 9
    m = 2
    print(f"Get unbalanced {client}")
    maxbstart = {
        9: 600,
        10: 945,
        11: 963,
        12: 974,
        13: 1008,
        14: 1013,
        15: 1017,
        16: 1020,
        17: 1021,
        18: 1023,
        19: 1024,
        20: 1024,
        21: 1024,
        22: 1024,
        23: 1024,
        24: 1024}
    mstart_9 = {
        9: 1,
        10: 3,
        11: 6,
        12: 14,
        13: 29,
        14: 60,
        15: 122,
        16: 246,
        17: 495,
        18: 994,
        19: 1995,
        20: 4001,
        21: 8032,
        22: 16113,
        23: 32321,
        24: 64820
    }
    mstart_10 = {
        10: 3,
        11: 6,
        12: 14,
        13: 29,
        14: 60,
        15: 122,
        16: 246,
        17: 495,
        18: 994,
        19: 1995,
        20: 4001,
        21: 8032,
        22: 16113,
        23: 32321,
        24: 64820
    }
    mstart_12 = {
        12: 14,
        13: 29,
        14: 60,
        15: 122,
        16: 246,
        17: 495,
        18: 994,
        19: 1995,
        20: 4001,
        21: 8032,
        22: 16113,
        23: 32321,
        24: 64820
    }
    for i in range(16, 25):
       
        # m, max_b = megabins(10,i)
        # print(f"{i} - m:{m}, max_b: {max_b}")
        if client == 9:
            m, max_b, beta = megabinsBeta(mstart_9[i], client, i, max_bstart=maxbstart[i])
        elif client == 10:
            m, max_b, beta = megabinsBeta(mstart_10[i], client, i, max_bstart=maxbstart[i])
        elif client == 12:
            m, max_b, beta = megabinsBeta(
                mstart_12[i], client, i, max_bstart=maxbstart[i])
        print(
            f"{i} - m:{m}, max_b: {max_b}, beta{beta}, epsilon: {beta/(1.27*(2**client))} {40+log2(beta)<= 61}")
    # m = int(1.5*m)

get_unbalanced()
# get_balanced()
# print(megabinsBeta(5202,12,20,max_bstart=800,limit=900))
# for i in range(100):
#     prob = p(5202,3*(2**20), 817+i)
#     print(f"{i} {prob<2**-40} {prob}")

#unbalanced newest changeds:
#10
# 10 - m:5, max_b: 947, beta1301, epsilon: 1.0003998523622046 True
# 11 - m:9, max_b: 965, beta1301, epsilon: 1.0003998523622046 True
# 12 - m:17, max_b: 976, beta1301, epsilon: 1.0003998523622046 True
# 13 - m:32, max_b: 1010, beta1301, epsilon: 1.0003998523622046 True
# 14 - m:66, max_b: 974, beta1301, epsilon: 1.0003998523622046 True
# 15 - m:131, max_b: 977, beta1301, epsilon: 1.0003998523622046 True
# 16 - m:261, max_b: 980, beta1301, epsilon: 1.0003998523622046 True
# 17 - m:651, max_b: 810, beta1301, epsilon: 1.0003998523622046 True
# 18 - m:1301, max_b: 812, beta1301, epsilon: 1.0003998523622046 True
# 19 - m:1997, max_b: 1024, beta1997, epsilon: 1.5355868602362204 True
# 20 - m:4006, max_b: 1024, beta4006, epsilon: 3.0804010826771653 True
# 21 - m:8035, max_b: 1024, beta8035, epsilon: 6.178487942913386 True
# 22 - m:16115, max_b: 1024, beta16115, epsilon: 12.391578494094489 True
# 23 - m:32321, max_b: 1024, beta32321, epsilon: 24.853131151574804 True
# 24 - m:64822, max_b: 1024, beta64822, epsilon: 49.844672736220474 True

# Get unbalanced 12
# 12 - m:17, max_b: 925, beta5202, epsilon: 1.0000153789370079 True
# 13 - m:32, max_b: 1010, beta5202, epsilon: 1.0000153789370079 True
# 14 - m:63, max_b: 1015, beta5202, epsilon: 1.0000153789370079 True
# 15 - m:127, max_b: 1005, beta5202, epsilon: 1.0000153789370079 True
# 16 - m:261, max_b: 980, beta5202, epsilon: 1.0000153789370079 True
# 17 - m:521, max_b: 983, beta5202, epsilon: 1.0000153789370079 True
# 18 - m:1041, max_b: 986, beta5202, epsilon: 1.0000153789370079 True
# 19 - m:2601, max_b: 815, beta5202, epsilon: 1.0000153789370079 True
# 20 - m:5202, max_b: 817, beta5202, epsilon: 1.0000153789370079 True
# 21 - m:8035, max_b: 1024, beta8035, epsilon: 1.5446219857283465 True
# 22 - m:16115, max_b: 1024, beta16115, epsilon: 3.097894623523622 True
# 23 - m:32321, max_b: 1024, beta32321, epsilon: 6.213282787893701 True
# 24 - m:64822, max_b: 1024, beta64822, epsilon: 12.461168184055119 True