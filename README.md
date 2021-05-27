# AWS Lambda
 
 ![AWS Lambda Logo](/images/logo.png)
 
* AWS Lambda is an Amazon Web Services compute service that runs your back-end code in response to events and manages compute resources for you. 
* The code running on AWS Lambda is called a Lambda function.
* You can write your code in the integrated editor within the AWS management console OR if your code requires custom libraries, you can create a .ZIP file containing all necessary components upload it as a codebase
* You can also select from pre-built samples, or blueprints.
* Code can be written in JavaScript using Node.js, Python, .NET, Ruby, Go or in Java.
* A Lambda function contains code, dependencies, and configuration information
* Configuration includes information like the handler that will receive the event, the AWS Identity and Access Management (IAM) role that AWS Lambda can use to execute the Lambda function


#### AWS Lambda can receive event data from multiple sources as shown below and perform various operations to provide required response.
![AWS Lambda Functioning](/images/lambda.png)

#### To create a Lambda function

1. Sign in to the [Lambda console](https://console.aws.amazon.com/lambda).
2. Choose **Create function**.
3. For **Function name**, enter ``my-function``.
4. Choose **Create function.**

The example function returns a 200 response to clients, and the text ``Hello from Lambda!``.

The default Lambda function code should look similar to the following:
```
exports.handler = async (event) => {
    const response = {
        statusCode: 200,
        body: JSON.stringify('Hello from Lambda!'),
    };
    return response;
};
```

We can invoke Lambda Functions by integrating with following interfaces based on different use cases : 
* **API Gateway** : Amazon API Gateway is an AWS service for creating, publishing, maintaining, monitoring, and securing REST, HTTP, and WebSocket APIs at any scale.
* **AWS SDKs** : Provides language-specific APIs (for e.g : NodeJS - [aws-sdk](https://www.npmjs.com/package/aws-sdk), Python - [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)).
* **AWS CloudWatch Events** : CloudWatch Events can invoke lambda function asynchronously with an event document that wraps the event from its source.

#### Calling Lambda function using an API Gateway : 

![API-Gateway](/images/API-Gateway.png)

Now we'll create a Lambda Function in Python3.8 to connect to Dynomo DB and fetch some records.
You can create a table from [DynamoDB Console](https://console.aws.amazon.com/dynamodb/)
To access DynamoDB, from our Lambda function, we need to add Permissions to the Lambda function Role.

The example function returns a 200 response to clients, with data from the mentioned table.
```
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
```

We will now create an HTTP API from API Gateway to receive requests from clients.

#### Steps: 
1. Sign in to the [API Gateway console](https://console.aws.amazon.com/apigateway)
2. Do one of the following:
    * To create your first API, for **HTTP API**, choose **Build**.
    * If you've created an API before, choose **Create API**, and then choose **Build** for **HTTP API**.
3. For **Integrations**, choose **Add integration**.
4. Choose **Lambda**.
5. For **Lambda function**, enter ``my-function``.
6. For **API name**, enter ``my-http-api``.
7. Choose **Next**.
8. Review the route that API Gateway creates for you, and then choose **Next**.
9. Review the stage that API Gateway creates for you, and then choose **Next**.
10. Choose **Create**.

Now you've created an HTTP API with a Lambda integration that's ready to receive requests from clients.

#### To test your API
1. Sign in to the [API Gateway console](https://console.aws.amazon.com/apigateway.)
2. Choose your API.
3. Note your API's invoke URL.

![AWS API Gateway](/images/my-http-api.png)

4. Copy your API's invoke URL, and enter it in a web browser. Append the name of your Lambda function to your invoke URL to call your Lambda function. By default, the API Gateway console creates a route with the same name as your Lambda function, my-function.
The full URL should look like ``https://abcdef123.execute-api.us-east-2.amazonaws.com/my-function``.
Your browser sends a ``GET`` request to the API.

5. Verify your API's response. You should see the response in above given format in your browser.


#### Calling Lambda function using an AWS SDK : 
![AWS SDK](/images/aws-sdk.png)
![AWS SDK boto3](/images/boto3.png)

Now we'll create a Lambda Function in NodeJS to POST a request to any external API and will invoke this Lambda function from our Client side using AWS-SDK.
The example function returns a 200 response to clients, with data from the requested external API.

```
const https = require('https');

const getStatus = (defaultOptions, path, payload) => new Promise((resolve, reject) => {
    const options = { ...defaultOptions, path, method: 'GET' };
    const req = https.request(options, res => {
        let buffer = "";
        res.on('data', chunk => buffer += chunk)
        res.on('end', () => resolve(JSON.parse(buffer)))
    });
    req.on('error', e => reject(e.message));
    req.write(JSON.stringify(payload));
    req.end();
})

exports.handler = async (event) => {
    // TODO 
    const defaultOptions = {
        host: event._hostname, //_hostname : example.com, passed from event as a parameter
        port: 443, // or 80 for http
        headers: {
            'Content-Type': 'application/json',
        }
    }

    var status_info = await getStatus(defaultOptions,event._pathname,''); //_pathname : /users/add, passed from event as a parameter
    
    // TODO implement
    const response = {
        statusCode: 200,
        body: JSON.stringify(status_info),
    };
    return response;
};
```
To invoke this Lambda function from Client side :
* boto3 - Python
```
import boto3
client = boto3.client('lambda',
                        region_name=region_name,
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key)
payload = {"id:"id","name:"name","age":"age"}
result = client.invoke(FunctionName='myfunctionname',
                    InvocationType='RequestResponse',                                      
                    Payload=json.dumps(payload))
```

* aws-sdk - NodeJS
```
const AWS    = require('aws-sdk');
const lambda = new AWS.Lambda;
const payload = {"id:"id","name:"name","age":"age"}
var params = {
  FunctionName: "my-function", 
  InvocationType='RequestResponse'
  Payload: payload
};
lambda.invoke(params, function(err, data) {
    if (err) 
        console.log(err, err.stack); // an error occurred
    else     
        console.log(data);           // successful response
});
```
Hence, we can use this response from our Lambda function.

#### Calling Lambda function using AWS CloudWatch Event : 

Now we'll create a Lambda Function in Python3.8 to Send an Email Alert Everyday except Sunday at 9:30 am IST (4:00am GMT).
To Schedule this, we will use **Cloudwatch Events**

* Pre-requisites :
- Verified Source Email to Send Email From [To Know More](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses.html)
- Permissions for Lambda Function to Send Email : 
```
{
     "Effect": "Allow",
     "Action": [
        "ses:SendEmail",
        "ses:SendRawEmail"
     ],
     "Resource": "*"
}
```
For Code [refer here](https://github.com/intelliconnect/aws-lambda/tree/master/aws-lambda-examples/send-email.py)

#### To create CloudWatch Event - Rule - to schedule Lambda function invocation.
1. Go to [Cloudwatch console]().
2. Go to **Event** -> **Rules**
3. Create **Rule**
4. Add details as shown below : 

![AWS SDK boto3](/images/cloudwatch-event-rule.png)

Click on **Configure details**, your Lambda invocation will be scheduled.


