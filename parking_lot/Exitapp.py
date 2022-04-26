import json
import math
from time import time
import boto3

s3 = boto3.client('s3')


def exit_lambda_handler(event, context):
    bucket = 'parkinglots3'
    key = 'db.json'

    ticket_id = event['queryStringParameters']['ticketId']
    if ticket_id is None:
        return "ticket_id is missing", 400
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body']
        db = json.loads(content.read())
    except:
        return f"there is no entry registered to ticket_id.: {ticket_id}", 422

    if ticket_id not in db.keys():
        return f"there is no entry registered to ticket_id: {ticket_id}", 422
    car_row = db[ticket_id]
    entry_time = float(car_row['entryTime'])
    total_parked_time_in_minutes = (time() - entry_time) / 60
    total_charge = str(math.ceil(total_parked_time_in_minutes / 15) * 10) + '$'
    data = {
        'license plate': str(car_row['plate']),
        'parking_lot': str(car_row['parkingLot']),
        'total parked time in minutes': int(total_parked_time_in_minutes),
        'total charge': total_charge,
    }
    db.pop(ticket_id)
    upload_byte_stream = bytes(json.dumps(db).encode('UTF-8'))
    s3.put_object(Bucket=bucket, Key=key, Body=upload_byte_stream)

    return data
