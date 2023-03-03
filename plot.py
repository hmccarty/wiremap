#!/usr/bin/env python3

import matplotlib
try:
    matplotlib.use('Qt5Agg')
except:
    print("PyQt5 is required")
    exit()

import argparse
import matplotlib.pyplot as plt
import os
import sys
import numpy as np
import ipaddress

def get_hilbert_point(n, d):
    """
    Hilbert curve encoding
    Source: https://en.wikipedia.org/wiki/Hilbert_curve 
    """

    def rot(n, x, y, rx, ry):
        if ry == 0:
            if rx == 1:
                x = n-1 - x
                y = n-1 - y
            return y, x
        return x, y

    rx, ry, t = 0, 0, d
    s, x, y = 1, 0, 0
    while s < n:
        rx = 1 & (t//2)
        ry = 1 & (t ^ rx)
        x, y = rot(s, x, y, rx, ry)
        x += s * rx
        y += s * ry
        t = (t//4)
        s *= 2
    return x, y

def on_close(event):
    print("Exiting...")
    exit()

def main(): 

    parser = argparse.ArgumentParser(prog='plot')
    parser.add_argument('-s', '--start-address', type=str, default='0.0.0.0')
    parser.add_argument('-e', '--end-address', type=str, default='255.255.255.255')
    args = parser.parse_args()

    num_ips = 4294967296 # Assume IPv4
    start_address = args.start_address
    end_address = args.end_address

    def d2ip(d):
        return [str(ipaddress.ip_address(int(i))) for i in d]
    
    # Setup plot
    fig, ax = plt.subplots()
    fig.canvas.mpl_connect('close_event', on_close)

    # Source connected IPs
    if len(sys.argv) < 2:
        script_dir = os.path.realpath(os.path.dirname(__file__))
        input_file = os.path.join(script_dir, 'ips')
    else:
        input_file = sys.argv[1]

    my_ips = set()
    with open(input_file) as f:
        for line in f.readlines():
            _, ip = line.split(',')
            my_ips.add(int(ipaddress.ip_address(ip.strip())))

    # Create hilbert curve of all IPs 
    all_ip_x = []
    all_ip_y = []
    for d in range(int(ipaddress.ip_address(start_address)), int(ipaddress.ip_address(end_address))):
        x, y = get_hilbert_point(num_ips, d)
        all_ip_x.append(x)
        all_ip_y.append(y)

        # TODO: Fix incorrect labels
        ax.set_yticklabels(d2ip(all_ip_y), rotation=45)
        ax.set_xticklabels(d2ip(all_ip_x), rotation=45)
        ax.plot(all_ip_x, all_ip_y)

        if d in my_ips:
            ax.plot(x, y, 'o', color='red')

        plt.draw()
        plt.pause(0.001)


    # Plot data
    # ax.plot(all_ip_x, all_ip_y)
    # ax.plot(my_ip_x, my_ip_y, 'o')

    plt.show()

if __name__ == "__main__":
    main()
