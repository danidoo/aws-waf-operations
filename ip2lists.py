#!/usr/bin/env python3

import sys
import argparse
import boto3

def add_cidr(ip_set, new_cidr):
    response = client.get_ip_set(Name=ip_set['Name'], Scope='REGIONAL', Id=ip_set['Id'])
    lt = response['LockToken']

    addresses = response['IPSet']['Addresses']
    addresses.append(new_cidr)

    response = client.update_ip_set(Name=ip_set['Name'], Scope='REGIONAL', Id=ip_set['Id'], Addresses=addresses, LockToken=lt)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('cidr', help='a IP CIDR in the format of "X.X.X.X/X"')
    parser.add_argument('--list', help='w for whitelist, b for blacklist', required=True)
    args = parser.parse_args()

    if args.list == 'w':
        list_name = 'IP_whitelist'
    elif args.list == 'b':
        list_name = 'IP_blacklist'
    else:
        sys.exit('ERROR: Invalid list, it must be either w or b')
    
    client = boto3.client('wafv2', region_name='us-east-1')

    response = client.list_ip_sets(Scope='REGIONAL')
    ip_sets = response['IPSets']
    list = next(ip_set for ip_set in ip_sets if ip_set['Name'] == list_name)

    add_cidr(list, args.cidr)