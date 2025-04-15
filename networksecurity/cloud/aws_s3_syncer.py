import os

class S3syncer:
    def sync_folder_to_s3(self,folder,s3_bucket_url):
        command =f"aws s3 sync {folder} {s3_bucket_url}"
        os.system(command)

    def sync_s3_to_folder(self,folder,s3_bucket_url):
        command =f"aws s3 sync {s3_bucket_url} {folder}"
        os.system(command)    

        