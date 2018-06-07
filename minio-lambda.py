import base64
from io import BytesIO
import hashlib
import random
import string
import sys
import time
import json
import threading

from minio import Minio

# Generate random name for object copy
def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# Parse bucket and object name from event data, 
# Spawn a thread to copy the object to another bucket
def lambda_handler(event):
    r = json.dumps(event)
    message = json.loads(r)
    bucket_name = message['Records'][0]['s3']['bucket']['name']
    object_name = message['Records'][0]['s3']['object']['key']
    t1 = threading.Thread(target=copy, args=(bucket_name,object_name))
    t1.start()

# Perform a server side copy. 
def copy(bucket_name, object_name):
    try:
        copy_result = minio.copy_object(TARGET_STORAGE_BUCKET, id_generator()+'_copied_object', bucket_name+'/'+object_name)
        print(copy_result)
    except ResponseError as err:
        print(err)

minio_access_key = 'Q3AM3UQ867SPQQA43P2F'
minio_secret_key = 'zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG'
STORAGE_ENDPOINT = 'play.minio.io:9000'

# Add your source and target bucket name here
STORAGE_BUCKET = 'srctestbucket'
TARGET_STORAGE_BUCKET = 'desttestbucket'

minio = Minio(STORAGE_ENDPOINT, access_key=minio_access_key, secret_key=minio_secret_key)

minio.make_bucket(STORAGE_BUCKET)
minio.make_bucket(TARGET_STORAGE_BUCKET)

# Listen for bucket notifications
events = minio.listen_bucket_notification(STORAGE_BUCKET, '','', ['s3:ObjectCreated:Put'])

# Call lambda_handler for each event
for event in events:
    lambda_handler(event)