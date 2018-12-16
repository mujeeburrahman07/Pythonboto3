import json
import boto3
iam_client = boto3.client('iam')
DEFAULT_POLICY_ARN_TO_ATTACH = "arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM"
REQUIRED_SERVICE_TO_CHECK = "ec2"
import re


def lambda_handler(event, context):
    # TODO implement
    print ("event", event)
    attach_policy_in_role(event)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def attach_policy_in_role(event):
    #response = iam_client.list_roles()
    #print "service name is", event_info['detail']['requestParameters']['assumeRolePolicyDocument']['Statement'][0]['Principal']['Service'][0]
    service_name = event['detail']['requestParameters']['assumeRolePolicyDocument']
    role_name = event['detail']['requestParameters']['roleName']
    match = re.search('ec2.amazonaws.com',service_name)
    if match:
       print ("its a ec2 service", match.group(0))
       print ("call attach policy")
       attach_policy(role_name)
    else:
       print ("its some other service, no action needed..", match)
    #print response

def attach_policy(role_name):
    print ("role_name", role_name)
    response = iam_client.attach_role_policy(
    RoleName=role_name,
    PolicyArn=DEFAULT_POLICY_ARN_TO_ATTACH
)
    return response
