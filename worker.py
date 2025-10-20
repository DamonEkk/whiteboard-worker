import os
import boto3
import json
import time
from export import render_strokes

sqs = boto3.client("sqs")
queue_url = os.environ["SQS_QUEUE_URL"]

while True:
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=20
    )
    messages = response.get("Messages", [])
    if not messages:
        continue

    for msg in messages:
        try:
            body = json.loads(msg["Body"])
            roomID = body.get("roomID")
            canvasH = body.get("canvasH")
            canvasW = body.get("canvasW")

            render_strokes(roomID, canvasH, canvasW)

            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=msg["ReceiptHandle"]
            )
        except Exception as e:
            print("Failed to process message:", e)
            # SQS will retry and eventually send to DLQ

