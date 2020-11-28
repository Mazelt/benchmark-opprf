import math
import numpy
from scipy.stats import binom
from mpmath import *
mp.dps= 15

def prob_maxb3(B, N, maxb):
    a = binom.cdf(N, N, (1.0/B))
    b = binom.cdf(maxb, N, (1.0/B))
    return B * (a - b)


def prob_maxb2(B, N, maxb):
    a = power(((math.e*N)/maxb),maxb)
    b = power(mpf(1.0/B),(maxb-1))
    return fmul(a,b)

def prob_maxb(B,N, maxb):
    summ = mpf(0.0)
    for i in range(maxb, N):
        c = power(mpf(1.0-(1.0/B)), (N-i))
        z = fmul(binomial(N, i), power(mpf(1.0/B), i))
        summ = fadd(summ, fmul(z,c))
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

# with security parameter 40: how high is maxb for Beta bins with n*K elements.
# The server puts n_server*K elements into nc*epsilon bins. 
def maxbBeta(n, K, beta, maxb, security=40):
    N = n * K
    B = beta
    maxb = maxb
    p = prob_maxb(B, N, maxb)
    print(p)
    while p > (2**(-security)):
        maxb += 1
        p = prob_maxb(B, N, maxb)
        if maxb % 10 == 0:
            print(p)
    return maxb


def maxMegaB(n, K, mega, polysize, security=40):
    N = n * K
    B = mega
    maxb = polysize
    p = prob_maxb(B, N, maxb)
    while p > (2**(-security)):
        maxb += 1
        p = prob_maxb(B, N, maxb)
    return maxb

# a bit faster because we only look from maxb above 900
def megabins2(n, K, Beta, security=40):
    N = n * K
    B = 1993
    maxb = 1023
    p = prob_maxb(B, N, maxb)
    while p > (2**(-security)):
        if maxb < 1024 or B*2>=Beta:
            print(f"maxb: {maxb + 1}")
            maxb +=1
        else:
            B+= 1
            print(f"B: {B}")
            maxb = 1023
        p = prob_maxb(B,N, maxb)
   
    return B, maxb


def get_bitlen(n):
    print(math.ceil(40 + math.log2(1.27*n)))


def get_parameters_stuff(nc, ns, K, epsilon=1.27):
    Beta = nc*epsilon
    # get megabins and polysize for ns and K
    mega, polysize = megabins2(ns, K)
    maxb = maxMegaB(ns, K, mega, polysize)
    print(f"mega {mega}, polysize {polysize},   maxb{maxb}")
    # if we have more megabins than bins: mega=bins
    if Beta <= mega:
        mega = Beta

    polysizebeta = maxbBeta(ns, K, Beta, 1)

    # after that: check wether megabins are more than half the bins
    if math.ceil(Beta/mega)*polysizebeta > polysize:
        mega = math.ceil(Beta/2)
        polysizebeta = maxbBeta(ns, K, Beta, polysize)
        polysize = 2 * polysizebeta

    # polysize = max(polysizebeta, maxb)
    print(f"n: {ns}, mega: {mega}, psize: {polysize}")
    return mega, polysize


def get_parameters(nc, ns , K, epsilon=1.27): 
    Beta = nc*epsilon
    # get megabins and polysize for ns and K
    mega, polysize = megabins2(ns, K, Beta)
    # polysize = max(polysizebeta, maxb)
    print(f"n: {ns}, mega: {mega}, psize: {polysize}")
    return mega, polysize

# print(maxbBeta(2**19,3, 2**12 * 1.27, 1))

# for i in range(19, 20):
#     get_parameters(2**12, 2**i, 3)
nc=2**10
epsilon =1.27
beta = nc*epsilon
ns = 2**19
print(f"ns/beta = {beta}")
print(maxbBeta(ns,3,beta,int(numpy.log2(beta))))


# get_bitlen(2**12)
