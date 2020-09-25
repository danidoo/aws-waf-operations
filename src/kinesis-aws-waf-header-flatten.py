# 
# This function aims at flattening header fields of the AWS WAF to help with Elasticsearch dashboards
#

from __future__ import print_function

import base64
import json

print('Loading function')

def lambda_handler(event, context):
    output = []

    for record in event['records']:
        payload = base64.b64decode(record['data'])

        # Flattens the header fields
        log = json.loads(payload)
        flatheaders = {}
        for item in log['httpRequest']['headers']:
            flatheaders[item['name'].lower()] = item['value']
        log['httpRequest']['flatheaders'] = flatheaders
        
        payload = json.dumps(log)

        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(payload)
        }
        output.append(output_record)

    print('Successfully processed {} records.'.format(len(event['records'])))

    return {'records': output}
