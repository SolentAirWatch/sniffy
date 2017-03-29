var PORT = 33333;
var HOST = '127.0.0.1';

var dgram = require('dgram');

var message = {'timestamp': datetime.datetime.now(), 'NO2WE': 0, 'NO2AE': 0, 'SO2WE': 0, 'SO2AE': 0, 'TEMP': 0, 'VREF': 0};

var client = dgram.createSocket('udp4');

client.send(message, 0, message.length, PORT, HOST, function(err, bytes) {
    if (err) throw err;
    console.log('UDP message sent to ' + HOST +':'+ PORT);
    client.close();
});