import base64
from io import BytesIO
import hashlib

from minio import Minio

# Note that https is mandatory for SSE-C to work or server will reject SSE-C requests
minio_access_key = 'Q3AM3UQ867SPQQA43P2F'
minio_secret_key = 'zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG'
STORAGE_ENDPOINT = 'play.minio.io:9000'

# Add your bucket name here
STORAGE_BUCKET = 'testbucket'

content = BytesIO(b'Hello again')

key = b'32byteslongsecretkeymustprovided'
encryption_key = base64.b64encode(key).decode()
encryption_key_md5 = base64.b64encode(hashlib.md5(key).digest()).decode()

minio = Minio(STORAGE_ENDPOINT, access_key=minio_access_key, secret_key=minio_secret_key)

# Make bucket. Skip this if bucket already exists on the server
minio.make_bucket(STORAGE_BUCKET)

# Put object with special headers which encrypt object in S3 with provided key
minio.put_object(STORAGE_BUCKET, 'test_crypt.txt', content, content.getbuffer().nbytes,
                    metadata={
                        'x-amz-server-side-encryption-customer-algorithm': 'AES256',
                        'x-amz-server-side-encryption-customer-key': encryption_key,
                        'x-amz-server-side-encryption-customer-key-MD5': encryption_key_md5
                    })

# Get decrypted object with same headers
obj = minio.get_object(STORAGE_BUCKET, 'test_crypt.txt', request_headers={
    'x-amz-server-side-encryption-customer-algorithm': 'AES256',
    'x-amz-server-side-encryption-customer-key': encryption_key,
    'x-amz-server-side-encryption-customer-key-MD5': encryption_key_md5
})

print(obj.read())
