import os
import pathlib
import glob
import boto3
from botocore.exceptions import ClientError



class S3:
    def __init__(
            self,
            aws_access_key_id=None,
            aws_secret_access_key=None,
            region_name=None,
            endpoint=None):
        """
        Create S3 Connector
        """
        self.endpoint = endpoint if os.environ.get(
            'ENDPOINT') is not None else os.environ.get('ENDPOINT')

        self.client = boto3.client(
            's3',
            region_name=region_name,
            endpoint_url=self.endpoint,
            use_ssl=True,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )


    @staticmethod
    def _check_type(path, recursive=False):
        """
        Check type of path: one file, dir or list of files
        """
        if not isinstance(path, (list, str)):
            return None
        elif isinstance(path, list):
            return path
        elif isinstance(path, str):
            if os.path.isdir(path):
                if recursive:
                    return [f for f in glob.glob('f{path}/**/*', recursive=True) if pathlib.Path(f).is_file()]
                else:
                    return [os.path.join(path, i) for i in os.listdir(path) if pathlib.Path(i).is_file()]
            return [path]

    def upload(self, objet, recursive=False, bucket_name=None):
        filename = self._check_type(objet, recursive=recursive)
        for file in filename:
            self.client.upload_file(Bucket=bucket_name,  Key=file,  Filename=file)

    def check_bucket(self, bucket_name=None):
        try:
            self.client.head_bucket(Bucket=bucket_name)
            print("Bucket Exists!")
            return True
        except ClientError as error:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = int(error.response['Error']['Code'])
            if error_code == 403:
                print("Private Bucket. Forbidden Access!")
                return True
            if error_code == 404:
                print("Bucket Does Not Exist!")
                return False