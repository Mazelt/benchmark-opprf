import math
from scipy.stats import binom
from mpmath import *

print(mp)

def prob_maxb(B, N, maxb):


    a = binom.cdf(N, N, (1.0/B))
    b = binom.cdf(maxb, N, (1.0/B))
    return B * (a - b)

def prob_maxb_mp(B,N, maxb):
    summ = mpf(0)
    for i in range(maxb, N):
        a = binomial(N,i)
        b = mpf(1.0/B)
        c = mpf(1.0-(1.0/B))
        b = power(b,i)
        c = power(c,(N-i))
        z = fmul(a, b)

        summ += fmul(z,c)
    return fmul(B , summ)

def megabins_mp(n, K, maxb, security=40):
    N = n*K
    B = 200
    p = prob_maxb_mp(B, N, maxb)
    print(p)
    while p > power(2,(-security)):
        B +=1
        p = prob_maxb_mp(B, N, maxb)
    return B


def megabins(n, K, maxb, security=40):
    N = n*K
    B = 2
    p = prob_maxb(B, N, maxb)
    print(p)
    while p > (2**(-security)):
        B += 1
        p = prob_maxb(B, N, maxb)
    return B, maxb

def megabins2(n, K, security=40):
    N = n * K
    B =2
    maxb = 900
    p = prob_maxb(B, N, maxb)
    while p > (2**(-security)):
        if maxb < 1024:
            maxb +=1
        else:
            B+= 1
            maxb = 900
        p = prob_maxb(B,N, maxb)
    print(p)
    return B, maxb

def get_bitlen(n):
    print(math.ceil(40 + math.log2(1.27*n)))

def get_parameters(n, K, epsilon=1.27): 

    mega, polysize = megabins2(n, K)
    print(f"n: {n}, mega: {mega}, psize: {polysize}")
    return mega, polysize
    
for i in range(19, 21):
    get_parameters(2**i, 3)

# get_bitlen(2**12)