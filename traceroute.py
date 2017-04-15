#!/usr/bin/python

import argparse
import subprocess

address = 'google.com'
command = 'traceroute ' + address
output = subprocess.check_output(command, shell=True)

split_list = output.split('\n')
split_list = split_list[1:]

ip_name_list = []
ip_addr_list = []

for i in range(len(split_list)):
    line = split_list[i].split()
    for j in range(len(line)):
        if(j == 1):
            ip_name_list.append(line[j])
        elif(j == 2):
            ip_addr_list.append(line[j])

print(ip_name_list)
print(ip_addr_list)
