import subprocess
import sys

enp = 'enp0s31f6'
tc_reset_enp_netem = f"sudo tc qdisc del dev {enp} root"
tc_add_enp = f"sudo tc qdisc add dev {enp} root netem"
tc_add_ifb = "sudo tc qdisc add dev ifb0 root netem"
modeprobe = "sudo modprobe ifb"
ip_up = "sudo ip link set dev ifb0 up"
tc_ingress = f"sudo tc qdisc add dev {enp} ingress"
tc_filter = f"sudo tc filter add dev {enp} parent ffff: protocol ip u32 match u32 0 0 flowid 1:1 action mirred egress redirect dev ifb0"


def reset_networks():
    # checking root privileges
    ret = subprocess.run(['sudo','whoami'],capture_output=True)
    if ret.stdout!= b'root\n':
        raise Exception("Please start this script as root (using sudo).")
    # reset netem
    tc_reset_netem = f"sudo tc qdisc del dev {enp} root"
    reset_args = tc_reset_netem.split()
    ret = subprocess.run(reset_args, capture_output=True, check=False)
    if ret.returncode != 0 and 'Cannot delete qdisc with handle of zero' not in str(ret.stderr):
        raise Exception(str(ret.stderr))
    # reset ingress
    tc_reset_ingress = f"sudo tc qdisc del dev {enp} handle ffff: ingress"
    reset_args = tc_reset_ingress.split()
    ret = subprocess.run(reset_args, capture_output=True, check=False)
    if ret.returncode != 0 and 'Invalid handle' not in str(ret.stderr):
        raise Exception(str(ret.stderr))
    # modprobe -r
    reset_args = ['modprobe', '-r', 'ifb']
    subprocess.run(reset_args,capture_output=True)
    


def set_network(delay=80,loss=0.1,rateDown=24,rateUp=4):
    delay = int(delay/2)
    # checking root privileges
    ret = subprocess.run(['sudo','whoami'],capture_output=True)
    if ret.stdout!= b'root\n':
        raise Exception("Please start this script as root (using sudo).")
    # reset interface
    reset_networks()
    # add outbound
    add_args = tc_add_enp.split()
    options = f"delay {delay}ms 5ms 25% loss {loss}% 25% rate {rateDown}mbit"
    add_args.extend(options.split())
    ret = subprocess.run(add_args, check=True)
    # add inbound
    # modprobe ifb
    subprocess.run(modeprobe.split(), check=True)
    # ip link set dev ifb0 up
    subprocess.run(ip_up.split(), check=True)
    # tc qdisc add dev {enp} ingress
    subprocess.run(tc_ingress.split(), check=True)
    # tc filter add dev $ENP parent ffff: protocol ip u32 match u32 0 0 flowid 1:1 action mirred egress redirect dev ifb0
    subprocess.run(tc_filter.split(), check=True)
    add_args = tc_add_ifb.split()
    options = f"delay {delay}ms 5ms 25% rate {rateUp}mbit"
    add_args.extend(options.split())
    ret = subprocess.run(add_args, check=True)

reset_networks()