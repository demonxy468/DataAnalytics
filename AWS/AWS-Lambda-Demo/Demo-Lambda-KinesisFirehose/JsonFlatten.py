from __future__ import print_function

import base64
import json
import pandas as pd
import cStringIO

print('Loading function')


def lambda_handler(event, context):
    output = []
    df = pd.DataFrame()
    
    for record in event['records']:
        print(record['recordId'])
        
        #Decode the stream data
        entry = base64.b64decode(record['data'])
        d = json.loads(entry)

        #Flatten the json data
        df = df.append(d, ignore_index=True)
        
        #put d back to Stream
        csv_buffer = cStringIO.StringIO()
        df.to_csv(csv_buffer,index=False,header=False)

        
        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(csv_buffer.getvalue())
        }
        output.append(output_record)

    print('Successfully processed {} records.'.format(len(event['records'])))

    return {'records': output}