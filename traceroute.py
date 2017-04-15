#!/usr/bin/python

import argparse
import subprocess

address = 'google.com'
command = 'traceroute ' + address
output = subprocess.check_output(command, shell=True)
print(output)
