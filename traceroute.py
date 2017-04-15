#!/usr/bin/python

import argparse
import subprocess
import re
import geoip2.database

reader = geoip2.database.Reader('GeoLite2-City.mmdb')

def main():
    address = 'google.com'
    command = 'traceroute ' + address
    output = subprocess.check_output(command, shell=True)
    return parse_route(output)

# generate ip name list and ip address list
def parse_route(output):
    split_list = output.split('\n')
    split_list = split_list[1:]

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
            latitude, longitude = get_ip_location(ip_addr)
            hop_dict = {'hop': hop, 'domain': domain, 'ip': ip_addr,
                        'latitude': latitude, 'longitude': longitude}
            hops.append(hop_dict)
    return hops

# generate list of ip locations using geoip2
def get_ip_location(ip):
    if ip[:3] != '10.' and ip[:3] != '127':
        response = reader.city(ip)
        location = response.location
        return location.latitude, location.longitude
