import boto3

class S3Uploader:
    def __init__(self, bucket_name, access_key, secret_key):
        self.bucket_name = bucket_name
        self.access_key = access_key
        self.secret_key = secret_key
        self.s3 = boto3.client('s3', aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
    
    def upload_image(self, file_name, file_data):
        self.s3.upload_fileobj(file_data, self.bucket_name, file_name)
        return f'https://{self.bucket_name}.s3.amazonaws.com/{file_name}'