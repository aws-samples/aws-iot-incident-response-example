import boto3
import os
import json
from datetime import datetime

iot_client = boto3.client('iot')
ssm_client = boto3.client('ssm-incidents')

RESPONSE_PLAN_ARN = os.environ['RESPONSE_PLAN_ARN']

def lambda_handler(event, context): 
    print(event)

    REGION = os.environ['AWS_REGION']

    message = json.loads(event['Records'][0]['Sns']['Message'])
    thing_name = message['thingName']
    timestamp = message['violationEventTime']
    violation_id = message['violationId']


    thing_data = iot_client.describe_thing(
        thingName=thing_name
    )

    logs_url = "https://console.aws.amazon.com/cloudwatch/home?region=" + REGION + "#logsV2:logs-insights$3FqueryDetail$3D$257E$2528end$257E0$257Estart$257E-3600$257EtimeType$257E$2527RELATIVE$257Eunit$257E$2527seconds$257EeditorString$257E$2527fields*20*40message*0a*7c*20filter*20clientId*20*3d*20*22" + thing_name + "*22$257EisLiveTail$257Efalse$257EqueryId$257E$25276709bc1f-8200-4c93-ae0c-82d32e322d6e$257Esource$257E$2528$257E$2527AWSIotLogsV2$2529$2529"
    thing_url = "https://console.aws.amazon.com/iot/home?region=" + REGION + "#/thing/" + thing_name

    response = ssm_client.start_incident(
        clientToken=str(timestamp),
        impact=3,
        relatedItems=[
           {
               'identifier': {
                   'type': 'OTHER',
                   'value': {
                       'url': logs_url
                   }
               },
               'title': 'IoT Logs Query URL'
           },
           {
               'identifier': {
                   'type': 'OTHER',
                   'value': {
                       'url': thing_url
                   }
               },
               'title': 'Thing additional information'
           }
        ],
        responsePlanArn=RESPONSE_PLAN_ARN,
        title='Critical IoT Device Incident | ' + violation_id, 
        triggerDetails={
            'rawData' : json.dumps(thing_data), 
            'timestamp': datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S'),
            'source' : 'iot.amazonaws.com'
        }
    )

