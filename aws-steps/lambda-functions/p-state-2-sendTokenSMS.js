const https = require('https'); // or https 

const defaultOptions = {
    host: 'example.com', //you sms api host
    port: 443, // or 80 for http
    headers: {
      'Authorization':'YOUR-API-KEY', 
      'Content-Type':'application/json'
    }
}

const post = (path, payload) => new Promise((resolve, reject) => {
    const options = { ...defaultOptions, path, method: 'POST' };
    const req = https.request(options, res => {
        let buffer = "";
        res.on('data', chunk => buffer += chunk)
        res.on('end', () => {
            if(buffer != "")
                resolve(JSON.parse(buffer))
            else
                res = {
                    statusCode: 200,
                    body: 'SMS Sent'
                }
                resolve(JSON.parse(res))
        })
    });
    req.on('error', e => reject(e.message));
    req.write(JSON.stringify(payload));
    req.end();
})

// Example usage
exports.handler = async (event, context) => new Promise( async (resolve, reject) => {
  var payload = {
    "senderid": "SenderId",
    "route": "Transactional", 
    "number": event.phonenumber,
    "message": "Your OTP for registration is : "+event.token
  }
    const response = await post('/api/apis/bulk-sms', payload); // sms api path
    
    return response;
})