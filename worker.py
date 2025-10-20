import os
import boto3
import json
import time
from export import render_strokes

sqs = boto3.client("sqs", region_name="ap-southeast-2")
queue_url = "https://sqs.ap-southeast-2.amazonaws.com/901444280953/n12197718-Whiteboard-A3"

while True:
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=20
    )
    messages = response.get("Messages", [])
    if not messages:
        time.sleep(1)
        continue

    for msg in messages:
        try:
            body = json.loads(msg["Body"])
            roomID = body.get("roomID")
            canvasH = body.get("canvasH", 3840)
            canvasW = body.get("canvasW", 2160)

            render_strokes(roomID, canvasH, canvasW)

            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=msg["ReceiptHandle"]
            )
        except Exception as e:
            print("Failed to process message:", e)
            # SQS will retry and eventually send to DLQ

