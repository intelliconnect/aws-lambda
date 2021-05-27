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