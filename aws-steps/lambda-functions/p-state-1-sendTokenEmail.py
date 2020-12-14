import json
import os
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def lambda_handler(event, context):
    # TODO implement
    #1 Read the input parameters
    firstName = event['firstname']
    lastName = event['lastname']
    emailID    = event['email']
    token   = event['tokenDetails']['token']
    tokenfor = event['tokenDetails']['tokenfor']
        
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "Millennial Weddings<info@millennialweddings.in>"
    
    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = emailID
    
    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    CONFIGURATION_SET = "mw-pwa-transactional"
    
    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "ap-south-1"
    
    # The subject line for the email.
    SUBJECT = firstName +", Your Millennial Weddings registration email token"
    
    if tokenfor == "forgotpassword" :
        SUBJECT = firstName +", Your Millennial Weddings forgot password email token"
    
    
    # The full path to the file that will be attached to the email.
    #ATTACHMENT = "path/to/customers-to-contact.xlsx"
    
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = "Hello " + firstName +",\r\nPlease note your Email/SMS token as "+ str(token) + ". Token is valid for 5 minutes\r\n \r\nWe are excited to see you consider us to find your perfect match.\r\n \r\nTeam Millennial Weddings \r\n \r\n \r\n \r\n \r\n \r\n \r\n DISCLAIMER : This e-mail is confidential. It may also be legally privileged. If you are not the addressee you may not copy, forward, disclose or use any part of it. Internet communications cannot be guaranteed to be timely secure, error or virus-free. The sender does not accept liability for any errors or omissions. We maintain strict security standards and procedures to prevent unauthorized access to information about you"
    
    # The HTML body of the email.
    #BODY_HTML = """\
    #<html>
    #<head></head>
    #<body>
    #<h1>Hello!</h1>
    #<p>Please see the attached file for a list of customers to contact.</p>
    #</body>
    #</html>
    #"""
    
    # The character encoding for the email.
    CHARSET = "utf-8"
    
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)
    
    # Create a multipart/mixed parent container.
    msg = MIMEMultipart('mixed')
    # Add subject, from and to lines.
    msg['Subject'] = SUBJECT 
    msg['From'] = SENDER 
    msg['To'] = RECIPIENT
    
    # Create a multipart/alternative child container.
    msg_body = MIMEMultipart('alternative')
    
    # Encode the text and HTML content and set the character encoding. This step is
    # necessary if you're sending a message with characters outside the ASCII range.
    textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
    #htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)
    
    # Add the text and HTML parts to the child container.
    msg_body.attach(textpart)
    #msg_body.attach(htmlpart)
    
    # Define the attachment part and encode it using MIMEApplication.
    #att = MIMEApplication(open(ATTACHMENT, 'rb').read())
    
    # Add a header to tell the email client to treat this part as an attachment,
    # and to give the attachment a name.
    #att.add_header('Content-Disposition','attachment',filename=os.path.basename(ATTACHMENT))
    
    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.
    msg.attach(msg_body)
    
    # Add the attachment to the parent container.
    #msg.attach(att)
    #print(msg)
    
    try:
        #Provide the contents of the email.
        response = client.send_raw_email(
            Source=SENDER,
            Destinations=[
                RECIPIENT
            ],
            RawMessage={
                'Data':msg.as_string(),
            },
            ConfigurationSetName=CONFIGURATION_SET
        )
    
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
    
    
    return {
        'statusCode': 200,
        'message': 'Email Sent'
    }

# For this Lambda function to work, we need to set access permissions to send Email
# For that we while creating lambda function, the role gets created, we can edit that role and edit exiting policy to this : 

# {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Effect": "Allow",
#             "Action": "logs:CreateLogGroup",
#             "Resource": "arn:aws:logs:<REGION>:<ACCOUNT_ID>:*"
#         },
#         {
#             "Effect": "Allow",
#             "Action": [
#                 "logs:CreateLogStream",
#                 "logs:PutLogEvents"
#             ],
#             "Resource": [
#                 "arn:aws:logs:<REGION>:<ACCOUNT_ID>:log-group:/aws/lambda/p-state-1-sendTokenEmail:*"
#             ]
#         },
#         {
#             "Effect": "Allow",
#             "Action": [
#                 "ses:SendEmail",
#                 "ses:SendRawEmail"
#             ],
#             "Resource": "*"
#         }
#     ]
# }