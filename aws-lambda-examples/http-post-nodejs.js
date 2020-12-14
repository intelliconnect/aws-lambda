const https = require('https'); // or https 

const defaultOptions = {
    host: 'example.com',
    port: 443, // or 80 for http
    headers: {
        'Content-Type': 'application/json',
    }
}

const post = (path, payload) => new Promise((resolve, reject) => {
    const options = { ...defaultOptions, path, method: 'POST' };
    const req = https.request(options, res => {
        let buffer = "";
        res.on('data', chunk => buffer += chunk)
        res.on('end', () => resolve(JSON.parse(buffer)))
    });
    req.on('error', e => reject(e.message));
    req.write(JSON.stringify(payload));
    req.end();
})


// Example usage
exports.handler = async (event, context) => new Promise( async (resolve, reject) => {
    // const token = await post('/auth/login', event); //event will be the payload required to send
    const token = 1234;
    console.log(token)
})