import json
import boto3
ec2_client = boto3.client('ec2')
#use po-managed-EC2 role ARN and name below
USER_DEFINED_ROLE_ARN = "arn:aws:iam::754985934811:instance-profile/TestAdminRole"
USER_DEFINED_ROLE_NAME = "TestAdminRole"

def lambda_handler(event, context):
    # TODO implement
    print ("event", event)
    print ('lets verify the current role or update if no role assigned', event['detail']['instance-id'])
    verify_role(event['detail']['instance-id'])
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def verify_role(instanceid):
    response = ec2_client.describe_iam_instance_profile_associations(
    AssociationIds=[

    ],
    Filters=[
        {
            'Name': 'instance-id',
            'Values': [
                instanceid,
            ]
        },
    ],
    MaxResults=123,
    )
    if response['IamInstanceProfileAssociations']:
       print ("Role looks already set", response['IamInstanceProfileAssociations'])
    else:
       print ("lets attach suggest role")
       attach_role(instanceid)
    print ("response",response)

def attach_role(instance_id):
    print ("in attach role")
    response = ec2_client.associate_iam_instance_profile(
    IamInstanceProfile={
        'Arn': USER_DEFINED_ROLE_ARN, 
        'Name': USER_DEFINED_ROLE_NAME
    },
    InstanceId=instance_id
    )
