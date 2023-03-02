#!/usr/bin/env python3

import os
import sys
from datetime import datetime
from requests import get

def main():
    if len(sys.argv) < 2:
        script_dir = os.path.realpath(os.path.dirname(__file__))
        output_file = os.path.join(script_dir, 'ips')
    else:
        output_file = sys.argv[1]
    
    ip = get('https://api.ipify.org').content.decode('utf8')
    with open(output_file, 'a') as f:
        f.write(f'{datetime.now()},{ip}\n')

if __name__ == "__main__":
    main()
