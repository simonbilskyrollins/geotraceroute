#!/usr/bin/python

import argparse
import subprocess
import geoip2.database

reader = geoip2.database.Reader('/path/to/GeoLite2-City.mmdb')
address = 'google.com'
command = 'traceroute ' + address
output = subprocess.check_output(command, shell=True)

split_list = output.split('\n')
split_list = split_list[1:]

ip_name_list = []
ip_addr_list = []

# generate ip name list and ip address list
for i in range(len(split_list)):
    line = split_list[i].split()
    for j in range(len(line)):
        if j == 1:
            ip_name_list.append(line[j])
        elif j == 2:
            ip_addr_list.append(line[j])

# clean up ip address (remove parens)
for i in range(len(ip_addr_list)):
    word = ip_addr_list[i]
    word = word.replace('(', '')
    word = word.replace(')','')
    ip_addr_list[i] = word

# generate list of ip locations using geoip2
ip_locs = []
ip_lat_long = []

for i in range(len(ip_addr_list)):
    ip = ip_addr_list[i]
    
    if ip[:3] != '10.' and ip[:3] != '127':
        response = reader.city(ip)
        ip_locs.append(response.city.name)
        ip_lat_long.append((response.location.latitude, response.location.longitude))


print(ip_addr_list)
print
print(ip_locs)
print
print(ip_lat_long)
