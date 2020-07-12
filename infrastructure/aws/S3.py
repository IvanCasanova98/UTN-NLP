import boto3
import os


class S3Handler:

    def __init__(self):
        try:
            import config
            AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
            AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
        except:
            AWS_ACCESS_KEY_ID = os.getenv("SECRET_ACCESS_KEY")
            AWS_SECRET_ACCESS_KEY = os.getenv("SECRET_SECRET_KEY")

        self.client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    def download_dir(self, prefix, local, bucket):

        keys = []
        dirs = []
        next_token = ''
        base_kwargs = {
            'Bucket': bucket,
            'Prefix': prefix,
        }
        while next_token is not None:
            kwargs = base_kwargs.copy()
            if next_token != '':
                kwargs.update({'ContinuationToken': next_token})
            results = self.client.list_objects_v2(**kwargs)
            contents = results.get('Contents')
            for i in contents:
                k = i.get('Key')
                if k[-1] != '/':
                    keys.append(k)
            next_token = results.get('NextContinuationToken')
        for k in keys:
            dest_pathname = os.path.join(local, k.replace(prefix, ''))
            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))
            self.client.download_file(bucket, k, dest_pathname)
