import os
os.system('aws s3 mb s3://s3bucket-for-parking-lot-deploy')
os.system('sam build')
os.system('sam deploy')