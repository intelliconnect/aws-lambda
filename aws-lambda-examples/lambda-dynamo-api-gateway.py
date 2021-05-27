import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
  # TODO implement
  dynamodb = boto3.resource('dynamodb')
  data = dynamodb.Table('test_table')
  response = data.scan()
  return {
    'statusCode': 200,
    'status': True,
    'data': response['Items']
  }