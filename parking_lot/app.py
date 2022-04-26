import json
import math
from time import time
import boto3

s3 = boto3.client('s3')


def entry_lambda_handler(event, context):
    bucket = 'parking-lot-s3'
    key = 'db.json'

    plate_number = event['queryStringParameters']['plate']
    if plate_number is None:
        return "plate number is missing", 400
    parking_lot = event['queryStringParameters']['parkingLot']
    if parking_lot is None:
        return "parking lot is missing", 400
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body']
        db = json.loads(content.read())
        for car_row in db.values():
            if plate_number == car_row['plate']:
                return "the car is already in the parking lot", 422
        ticket_id = int(max(db.keys())) + 1
    except:
        db = {}
        ticket_id = 0

    new_row = {'plate': plate_number, 'parkingLot': parking_lot, 'entryTime': time()}
    db[ticket_id] = new_row
    upload_byte_stream = bytes(json.dumps(db).encode('UTF-8'))
    s3.put_object(Bucket=bucket, Key=key, Body=upload_byte_stream)

    return f"a new car entry was registered, ticket_id is: {ticket_id}", 422


def exit_lambda_handler(event, context):
    bucket = 'parking-lot-s3'
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
