import os

os.system('aws s3 rm s3://parkinglots3 --recursive')
os.system('sam delete --no-prompts')
os.system('aws s3 rb s3://s3bucket-for-parking-lot-deploy --force')
