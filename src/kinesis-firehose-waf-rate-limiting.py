# Counts requests from the same IP for a certain URI and if THRESOLD is exceeded, adds IP to AWS WAF IP Set list
# Required environment variables:
#      REGION: region where the AWS WAF IP Set is configured
#      THRESHOLD: the number of requests from the same IP to the specified URI that will trigger the blacklisting
#      IP_SET_NAME: the AWS WAF IP Set name that holds the blacklisted IPs
#      IP_SET_ID: the AWS WAF IP Set ID that holds the blacklisted IPs
#      URI: that uri that the requests should be counted against (starts with)

import base64
import json
import os
import boto3

region = os.environ['REGION']
uri = os.environ['URI']
threshold = int(os.environ['THRESHOLD'])
ip_set_name = os.environ['IP_SET_NAME']
ip_set_id = os.environ['IP_SET_ID']
print('Loading function')


def blacklist(ips):
    client = boto3.client('wafv2', region_name=region)
    response = client.get_ip_set(Name=ip_set_name, Scope='REGIONAL', Id=ip_set_id)
    lt = response['LockToken']
    addresses = response['IPSet']['Addresses']

    for ip in ips:
        cidr = ip + '/32'
        if cidr not in addresses:
            addresses.append(cidr)
            print('Blacklisting:', cidr)

    response = client.update_ip_set(Name=ip_set_name, Scope='REGIONAL', Id=ip_set_id, Addresses=addresses, LockToken=lt)

def lambda_handler(event, context):
    output = []

    client_ips = {}

    for record in event['records']:
        payload = base64.b64decode(record['data'])
        log = json.loads(payload)
        
        if log['httpRequest']['uri'].startswith(uri):
            clientIp = log['httpRequest']['clientIp']
            if clientIp in client_ips:
                client_ips[clientIp] += 1
            else:
                client_ips[clientIp] = 1
    
    print('IP count results')
    blacklist_ips = []
    for ip in client_ips:
        if client_ips[ip] > threshold:
            blacklist_ips.append(ip)
        print(ip, client_ips[ip])
    
    if len(blacklist_ips):
        blacklist(blacklist_ips)

    print('Successfully processed {} records.'.format(len(event['records'])))

    return {'records': event['records']}
