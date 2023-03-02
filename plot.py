#!/usr/bin/env python3

import matplotlib.pyplot as plt
import os
import sys
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

def main():
    num_ips = 4294967296

    # Create hilbert curve of all IPs 
    all_ip_x = []
    all_ip_y = []
    for d in range(num_ips):
        x, y = get_hilbert_point(num_ips, d)
        all_ip_x.append(x)
        all_ip_y.append(y)

    # Source connected IPs
    if len(sys.argv) < 2:
        script_dir = os.path.realpath(os.path.dirname(__file__))
        input_file = os.path.join(script_dir, 'ips')
    else:
        input_file = sys.argv[1]

    my_ip_x = []
    my_ip_y = []
    with open(input_file) as f:
        for line in f.readlines():
            print(line)
            _, ip = line.split(',')
            d = int(ipaddress.ip_address(ip.strip()))
            x, y = get_hilbert_point(num_ips, d)
            my_ip_x.append(x)
            my_ip_y.append(y)

    # Plot data
    fig, ax = plt.subplots()
    ax.plot(all_ip_x, all_ip_y)
    ax.plot(my_ip_x, my_ip_y, 'o')

    plt.show()

if __name__ == "__main__":
    main()