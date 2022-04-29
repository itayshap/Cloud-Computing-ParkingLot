aws s3 rm s3://parkinglots3 --recursive
call sam delete --no-prompts
call aws s3 rb s3://s3bucket-for-parking-lot-deploy --force
PAUSE