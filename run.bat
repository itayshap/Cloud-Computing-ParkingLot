ECHO OFF
aws s3 mb s3://s3bucket-for-parking-lot-deploy
call sam build
call sam deploy
PAUSE
