import json
import boto3
from boto3.dynamodb.conditions import Key
import random
from datetime import datetime, timedelta, time

#That's the lambda handler, you can not modify this method
# the parameters from JSON body can be accessed like deviceId = event['deviceId']
def lambda_handler(event, context):
    # Instanciating connection objects with DynamoDB using boto3 dependency
    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')
    lambdaclient = boto3.client('lambda')
    
    # Getting the table the table Temperatures object
    tableNewRegistration = dynamodb.Table('RegistrationToken')
    
    # Getting the current datetime and transforming it to string in the format bellow
    eventDateTime = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    expiryDateTime = (datetime.now() + timedelta(seconds=300)).strftime("%s")
    expiryDateTime = int(expiryDateTime)
  
    # Parameters from API
    phonenumber = event['phonenumber']
    email = event['email']
    firstname = event['firstname']
    lastname = event['lastname']
    if 'tokenfor' in event :
        tokenfor = event['tokenfor']
    else:
        tokenfor = "newregistration"
        
    
    newToken = random.randint(1000, 9999)
    

    # Putting a try/catch to log to user when some error occurs
    try:
        print('here?')
        tableNewRegistration.put_item(
           Item={
                'eventDateTime': eventDateTime,
                'phonenumber': int(phonenumber),
                'firstname':firstname,
                'lastname':lastname,
                'email':email,
                'token': newToken,
                'expiryDateTime': expiryDateTime
            }
        )
        
        # Add User to Archive Table for future use
        tableRegistrationArchiveInfo = dynamodb.Table('RegistrationUsers')
        responseNewregistrationUser = tableRegistrationArchiveInfo.query(KeyConditionExpression=Key('phonenumber').eq(phonenumber))
        if responseNewregistrationUser['Items']:        
            #checkPhoneNumber = response['Items'][0]['phonenumber']
            print("Found")
        else:
            print('Add')
            tableRegistrationArchiveInfo.put_item(
               Item={
                    'eventDateTime': eventDateTime,
                    'phonenumber': int(phonenumber),
                    'firstname':firstname,
                    'lastname':lastname,
                    'email':email
                }
            )
        
        return {
            'statusCode': 200,
            'status':True,
            'message':'Succesfully Added Token!',
            'token':newToken,
            'tokenfor':tokenfor
        }
    except:
        #print('Closing lambda function')
        return {
                'statusCode': 400,
                'status':False,
                'message':'Error Generarting Token'
        }


# For this Lambda function to work, we need to set access permissions to connect with Dynamo DB
# For that we while creating lambda function, the role gets created, we can edit that role and attach policy named AmazonDynamoDBFullAccess