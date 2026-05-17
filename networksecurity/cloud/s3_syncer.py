import subprocess


class S3Sync:
    # def sync_folder_to_s3(self,folder,aws_bucket_url):
    #     command = ["aws", "s3", "sync", folder, aws_bucket_url]
    #     subprocess.run(command, check=True)

    # def sync_folder_from_s3(self,folder,aws_bucket_url):
    #     command = ["aws", "s3", "sync", aws_bucket_url, folder]
    #     subprocess.run(command, check=True)

    def sync_folder_to_s3(self,folder,aws_bucket_url):
        command = f"aws s3 sync {folder} {aws_bucket_url} "
        print("\n" + "="*50)
        print(f"PYTHON IS RUNNING THIS COMMAND:")
        print(command)
        print("="*50 + "\n")
        subprocess.run(command, shell=True, check=True)

    def sync_folder_from_s3(self,folder,aws_bucket_url):
        command = f"aws s3 sync  {aws_bucket_url} {folder} "
        subprocess.run(command, shell=True, check=True)