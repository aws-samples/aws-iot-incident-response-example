import boto3
import os
import json
from datetime import datetime

iot_client = boto3.client('iot')
tagging_client = boto3.client('resourcegroupstaggingapi')

def lambda_handler(event, context): 
    print(event)

    ACCOUNT_ID = context.invoked_function_arn.split(":")[4]
    REGION = os.environ['AWS_REGION']

    response = iot_client.list_active_violations()

    things = []

    for violation in response['activeViolations']: 
        try: 
            action_response = iot_client.start_detect_mitigation_actions_task(
                taskId=str(violation['thingName'] + violation['violationId']), 
                target={
                    'violationIds' : [
                        violation['violationId']
                    ]
                }, 
                actions=[
                    'contain'
                ], 
                includeOnlyActiveViolations=True
            )
            things.append(violation['thingName'])
        except Exception as e: 
            print("Error applying containment ", e)

    current_datetime = datetime.now()
    timestamp = current_datetime.strftime("%d-%b-%Y %H:%M:%S")

    for thing in things: 
        response = tagging_client.tag_resources(
            ResourceARNList=[ 'arn:aws:iot:' + REGION + ':' + ACCOUNT_ID + ':thing/' + thing ],
            Tags={
                'QUARANTINED': timestamp
            }
        )

    print(things)

    return {
        "thingsDetected" : str(things) 
    }