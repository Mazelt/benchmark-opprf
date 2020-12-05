# Quick start
install requirements
download appium-linux client.
run appimage
connect phone.
configure in psi.py.

# General Remarks

## Flakyness
The gtest suite shows some flakyness.
results are not always matching the expected result. 
The tests are running SUM on 2_20.

## Timings
hashing_t: client does cuckoo, server simple.

oprf_t: server seems to have a bit more to do

poly_t means:

for client -> evaluation of polynomials
for server -> generation of values and interpolation

poly_trans_t on client side is not meaningful since it counts in the time the
client waits for the server to complete polynomial creation. 
Only count in poly_trans_t of the server.
remove polytrans from client time or use server's value for both.

aby_online, _setup.  its synced and same for both.

total_t

other = waiting time, coordination.

# Experiments

## Desktop-APP
### Set-up
Server: Lenovo t480s
Client: OnePlus 5 (Android 9)

Wifi router with wired connection to server.
5GHz. 

### Batches
Topics to cover:
* Scaling of element numbers (not so important)
* Sweet-spot for low amount of elements and performance (bei tage-aufbrechen.)
* Differences between PSI types
* Unbalanced set performances !!
* Variation of extra arguments: Megabins, epsilon, hashfun (security)
* monitoring of network speeds (network em (later))
* monitoring of energy/cpu/memory usage on phone.

Future possible topics:
* Differences in ABY ciruit types. (not extensive analysis, DD)
* Enable SSE?
* Use newer NTL version? (only on server side)
* threading? on server side?


*Scaling of element numbers* 
Start low. 
Scale other parameters accordingly.

What are the metrics to test:

* Breaks: yes,no
* Running time
* Communication amount (beware of setup and online time.)
* Polynomial size

K=3, epsilon=1.27 (means Beta=1.27n), opprf output length:
2^8: 49, 2^12: 53, 2^16: 57, 2^20: 61
megabins for K=3 from table 2 of pinkas paper, polysize is related to max_b.
n   : #mbins : polys
2^12:  16    : 975
2^16:  248   : 1021
2^20:  4002  : 1024

this wasn't easy. computation is in test.py.
One has to use the formula from Pinkas et al for mega bins.
And at some point you have to increase maxb=1024 when the megabins are more then
half the bins.
For the unbalanced scenario this is a bit different. since we cant increase
megabins above half of Beta (bins on client side.)
So then the polysize is increasing. This gets computational expensive on the
server side pretty fast. Communication-wise this isn't a problem. since
polynomials are not that heavy.

*Sweet-spot for low amount of elements and performance*
What is a typical amount of keys for a day and the daily increment on the server
for each past day?

when the difference between client set and server set is too high. the
polynomials get too big! Also the setup time for aby might be too much.

Sweetspot important! when a client has just 2^10 elems but the server has 2^22
how much can we/should we increase the number of bins to decrease the polynomial
size? plot the functions?

*Differences between PSI types*
Choose 3 or 4 parameter sets to test for.
Run multiple runs for each psi type.

* Breaks: yes,no
* Running time
* Communication amount (beware of setup and online time.)


*Variation of extra arguments: Megabins, polysize,...*
Mostly megabin and polysize changes can bring value.
if not set, only one megabin is used and a really big polynomial has to be
interpolated. And.. i think the opprf is batched more efficiently with megabins.


## Desktop-App-WAN
TODO: get psi binary to run on remote linux vm
TODO: add wrapper script to remotely run server binary and download data.

## Desktop-Desktop
Add network delay to simulate LAN and not localhost speed.


#notes
Network traces, use network emulator to use traces.
net em (linux) -> dealy, packet loss.

15-20min each key. 

client-'multi-threading'= 'parallele' per-day ausführungen


log-scale for gbit.

pak fehlerbalken

energie/auslastung messen.

aby-compile auf performance?
aby-production.

messen wie lange gewartet wird.

limit ausrechnen für collision bei skalierung der serve elemente.

Wieviele runs?
In den titel!

erst perfektes setting

wsl