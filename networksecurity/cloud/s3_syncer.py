import os

class S3Sync:
    def __init__(self):
        pass
    def sync_folder_to_S3(self, folder, aws_bucket_url):
        command = f"aws s3 sync {folder} {aws_bucket_url}"
        os.system(command)
    def sync_folder_from_S3(self, folder, aws_bucket_url):
        command = f"asw s3 sync {aws_bucket_url} {folder}"
        os.system(command)