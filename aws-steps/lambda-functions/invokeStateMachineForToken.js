const AWS = require('aws-sdk');
const stepFunctions = new AWS.StepFunctions();

exports.handler = async (event) => {
    let params = {
        stateMachineArn: "arn:aws:states:<REGION>:<ACCOUNT_ID>:stateMachine:MyStateMachine",
        input: JSON.stringify(event)
    }
    
    let data = await stepFunctions.startExecution(params).promise();
    console.log(data);
    return data;
};


// For this Lambda function to work, we need to set access permissions to execute Step functions
// For that we while creating lambda function, the role gets created, we can edit that role and attach policy named AWSStepFunctionsFullAccess