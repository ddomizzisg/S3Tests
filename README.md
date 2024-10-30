1) Deploy the container using ```docker compose up -d``` command.
2) Configure the S3 API credentials to interact with S3 services. Check this: [Amazon S3 credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html).
3) Enter into the container: ``docker compose exec s3client bash``
4) Upload data: ``python3 upload.py FILE_TO_PUSH``
5) Download data: ``python3 download.py requirements.txt``