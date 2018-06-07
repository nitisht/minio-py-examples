import base64
from io import BytesIO
import hashlib

from minio import Minio

minio_access_key = 'Q3AM3UQ867SPQQA43P2F'
minio_secret_key = 'zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG'
STORAGE_ENDPOINT = 'play.minio.io:9000'

# Add your bucket name here
STORAGE_BUCKET = 'testbucket'

content = BytesIO(b'Hello again')

minio = Minio(STORAGE_ENDPOINT, access_key=minio_access_key, secret_key=minio_secret_key, secure=True)

# Make bucket. Skip this if bucket already exists on the server
minio.make_bucket(STORAGE_BUCKET)

# Put object with custom metadata
minio.put_object(STORAGE_BUCKET, 'test_obj', content, content.getbuffer().nbytes,
                    metadata={
                        'x-amz-meta-testdata': 'testdata'
                    })

# Head object with metadata
obj = minio.stat_object(STORAGE_BUCKET, 'test_obj')
print(obj.metadata)
