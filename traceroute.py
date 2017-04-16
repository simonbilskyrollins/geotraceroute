#!/usr/bin/python

import argparse
import subprocess
import re
import geoip2.database

def main(address):
    reader = geoip2.database.Reader('GeoLite2-City.mmdb')
    command = 'traceroute ' + address
    output = subprocess.check_output(command, shell=True)
    geoip = parse_route(reader, output)
    reader.close()
    return geoip

# generate ip name list and ip address list
def parse_route(reader, output):
    split_list = output.split('\n')
    for i in range(len(split_list)):
        if split_list[i][:10] != 'traceroute':
            break
        split_list.pop(i)

    hop = 1
    hops = []
    for line in split_list:
        hop_match = re.match(' (\d\d?)?\s+(.+)\s\((\d+\.\d+\.\d+\.\d+)\).*', line)
        if hop_match:
            try:
                hop = int(hop_match.group(1))
            except TypeError:
                pass
            domain = hop_match.group(2)
            ip_addr = hop_match.group(3)
            latitude, longitude = get_ip_location(reader, ip_addr)
            hop_dict = {'hop': hop, 'domain': domain, 'ip': ip_addr,
                        'latitude': latitude, 'longitude': longitude}
            hops.append(hop_dict)
    return hops

# generate list of ip locations using geoip2
def get_ip_location(reader, ip):
    if ip[:3] != '10.' and ip[:3] != '127':
        city = reader.city(ip)
        location = city.location
        return location.latitude, location.longitude
