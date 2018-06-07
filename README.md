# Minio Python SDK Examples

## Server Side Encryption

Minio supports [S3 SSE-C encryption](https://docs.aws.amazon.com/AmazonS3/latest/dev/ServerSideEncryptionCustomerKeys.html) where users provide and manage the encryption keys. Data is encrypted at rest. Here are some important points regarding Minio SSE-C

- Minio does not store the encryption key you provide. Instead, we store a randomly salted HMAC value of the encryption key in order to validate future requests. The salted HMAC value cannot be used to derive the value of the encryption key or to decrypt the contents of the encrypted object. That means, if you lose the encryption key, you lose the object.

- [TLS based Minio deployment](https://docs.minio.io/docs/how-to-secure-access-to-minio-server-with-tls) is mandatory for Minio SSE-C to work. Minio server will reject encryption requests on HTTP deployment.

Refer to [demo code here](./minio-encryption.py) to see Minio SSE-C in action using minio-py SDK.

## Custom metadata

You can add custom metadata to an object using the minio-py `put_object` method. To add custom metadata, create a Python `dictionary` with relevant custom metadata and pass it to `put_object`. Refer to [demo code here](./minio-metadata.py) to see this in action.

## Lambda functions

Lambda functions allow performing activities based on notifications issued by Minio server. Supported event types are

| Supported Event Types | | |
|:---------------------------|--------------------------------------------|-------------------------|
| `s3:ObjectCreated:Put`     | `s3:ObjectCreated:CompleteMultipartUpload` | `s3:ObjectAccessed:Head`|
| `s3:ObjectCreated:Post`    | `s3:ObjectRemoved:Delete`                  |
| `s3:ObjectCreated:Copy`    | `s3:ObjectAccessed:Get`                    |

Follow these steps to setup your lambda functions:

- Setup `listen_bucket_notification` on specific bucket. By default all events are enabled.

- Wait for events in a loop.

- When event data is available, parse the `json` response from server and spawn a lambda function to perform the specific task.

Refer to [demo code here](./minio-lambda.py) to see a sample lambda function in action.
