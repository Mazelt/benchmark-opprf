# Quick start
install requirements
download appium-linux client.
run appimage
connect phone.
configure in psi.py.

# Experiments
## Desktop-APP
### Set-up
Server: Lenovo t480s
Client: OnePlus 5 (Android 9)

Wifi router with wired connection to server.
5GHz. 

### Batches
Topics to cover:
* Scaling of element numbers
* Sweet-spot for low amount of elements and performance
* Differences between PSI types
* Unbalanced set performances
* Variation of extra arguments: Megabins, epsilon, hashfun
* monitoring of network speeds
* monitoring of energy/cpu/memory usage on phone.

Future possible topics:
* Differences in ABY ciruit types.
* Enable SSE?
* Use newer NTL version?
* threading? on server side?


*Scaling of element numbers* 
Start low. 
Remember the implementation breaking for n>2^16: it looks like this is because
the tests are working with k=2 and this reaches 62 bit opprf output length
requirement which is not supported by the used mersenne prime field.
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



*Sweet-spot for low amount of elements and performance*
What is a typical amount of keys for a day and the daily increment on the server
for each past day?

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
