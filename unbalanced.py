import numpy
import random
random.seed(0)

bigmask = 2**32-1
smolmask = 2**17-1
# print(bin(bigmask))
# print(bin(smolmask))
# item = 2**29+2**12
# print(bin(item))
# print(bin(item & bigmask))
# print(bin(item & smolmask))

def generate(n):
    return [random.randint(0, bigmask) for x in range(n)]

for i in range(2**12):
    random.seed(i)
    s = generate(8)
    c = random.randint(0,bigmask)
    psm = not(c in s)
    sb = [e & smolmask for e in s]
    cb = c & smolmask
    psmb = not(cb in sb)
    if psm != psmb:
        print("AHHHHH")

