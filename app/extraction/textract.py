import time

import boto3
from tqdm import tqdm


def get_bucket_and_key_from_url(url):
    """Extracts the bucket name and key from an https:// or s3:// URL."""
    if url.startswith("https://"):
        url = url.replace("https://", "")
        # https://scorecard-testing-testing.s3.amazonaws.com/jan_6.pdf
        bucket_name = url.split(".")[0]
        key = url.split("/", 1)[1]
    elif url.startswith("s3://"):
        url = url.replace("s3://", "")
        bucket_name, key = url.split("/", 1)
    return bucket_name, key


# Function to extract text from a PDF file in an S3 bucket using Textract
def extract_text_from_pdf(s3_bucket_name, s3_object_key):
    textract_client = boto3.client("textract", region_name="us-east-1")

    # Start the asynchronous text detection job
    response = textract_client.start_document_text_detection(
        DocumentLocation={"S3Object": {"Bucket": s3_bucket_name, "Name": s3_object_key}}
    )
    job_id = response["JobId"]

    # Poll for job completion
    with tqdm(desc="Processing", unit=" seconds passed.", leave=False) as pbar:
        while True:
            response = textract_client.get_document_text_detection(JobId=job_id)
            status = response["JobStatus"]
            if status in ["SUCCEEDED", "FAILED"]:
                break
            pbar.update(1)
            time.sleep(1)

    # Process the results
    if status == "SUCCEEDED":
        raw_text = ""
        for block in response["Blocks"]:
            if block["BlockType"] == "LINE":
                raw_text += block["Text"] + "\n"
        return raw_text
    else:
        raise Exception(f"Text detection job failed with status: {status}")


# Example usage
if __name__ == "__main__":
    bucket_name = "scorecard-testing"
    object_name = "nature_paper.pdf"
    # Extract text from the PDF using Textract
    extracted_text = extract_text_from_pdf(bucket_name, object_name)
    print(extracted_text)
