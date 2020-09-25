# 
# This function aims at parsing AWS WAF logs to flatten header fields and doing enrichment
#

import base64
import json
import pyasn
from user_agents import parse
from counter_robots import is_machine, is_robot

print('Loading function')
asndb = pyasn.pyasn('ipasn.dat')
ua = {}

def getUAInfo(user_agent_string):
    if user_agent_string in ua:
        return ua[user_agent_string]
    else:
        info = {}
        user_agent = parse(user_agent_string)
        browser = {}
        browser['family'] = user_agent.browser.family
        browser['version'] = user_agent.browser.version_string
        info['browser'] = browser

        os = {}
        os['family'] = user_agent.os.family
        os['version'] = user_agent.os.version_string
        info['os'] = os

        device = {}
        device['family'] = user_agent.device.family
        device['brand'] = user_agent.device.brand
        device['model'] = user_agent.device.model
        info['device'] = device

        ua[user_agent_string] = info
        return info

def lambda_handler(event, context):
    output = []

    for record in event['records']:
        payload = base64.b64decode(record['data'])
        log = json.loads(payload)

        # Flattens the header fields
        flatheaders = {}
        for item in log['httpRequest']['headers']:
            flatheaders[item['name'].lower()] = item['value']
        del(log['httpRequest']['headers'])
        log['httpRequest']['headers'] = flatheaders

        # Adds ASN number
        log['httpRequest']['asn'] = asndb.lookup(log['httpRequest']['clientIp'])[0]

        user_agent_string = log['httpRequest']['headers']['user-agent']

        # Adds user-agent information
        ua_info = getUAInfo(user_agent_string)
        log['httpRequest']['browser'] = ua_info['browser']
        log['httpRequest']['os'] = ua_info['os']
        log['httpRequest']['device'] = ua_info['device']

        # Adds robot information
        device_type = ''
        if is_machine(user_agent_string):
            device_type = 'machine'
        elif is_robot(user_agent_string):
            device_type = 'robot'
        else:
            device_type = 'browser'
        log['httpRequest']['deviceType'] = device_type

        payload = json.dumps(log)

        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(payload)
        }
        output.append(output_record)

    print('Successfully processed {} records.'.format(len(event['records'])))

    return {'records': output}
