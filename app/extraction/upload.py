import os

import boto3


def upload_file_to_s3(local_file_path, bucket_name):
    s3_object_key = os.path.basename(local_file_path)
    s3 = boto3.client("s3")
    s3.upload_file(local_file_path, bucket_name, s3_object_key)
    return s3_object_key


if __name__ == "__main__":
    local_pdf_path = "nature_paper.pdf"
    bucket_name = "scorecard-testing"

    # Upload the local PDF to S3
    upload_file_to_s3(local_pdf_path, bucket_name)
