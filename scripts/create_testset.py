import json
import os

from scorecard.client import Scorecard
from scorecard.types import CustomSchemaInput, CustomVariable, FileUrl

client = Scorecard(api_key=os.environ["SCORECARD_API_KEY"])

# Create a Testset
testset = client.testset.create(
    name="Testset for Scorecard Demo",
    description="Demo of e2e testing with Textract and Pinecone retrieval",
    using_retrieval=True,
    custom_schema=CustomSchemaInput(
        variables=[
            CustomVariable(
                name="input_file_url",
                description="PDF hosted on S3",
                role="input",
                data_type="file_url",
            ),
            CustomVariable(
                name="Some JSON",
                description="Some JSON stuff",
                role="input",
                data_type="json_object",
            ),
            CustomVariable(
                name="extracted_text",
                description="Response from Textract",
                role="output",
                data_type="text",
            ),
        ]
    ),
)

if testset.id is None:
    raise ValueError("Testset ID is None, cannot create testcase.")

for i in range(10):
    client.testcase.create(
        testset_id=testset.id,
        user_query="What is in the PDF?",
        custom_inputs={
            "input_file_url": FileUrl(
                url="https://scorecard-testing.s3.amazonaws.com/jan_6.pdf",
                name="jan_6.pdf",
            ),
            "Some JSON": json.dumps(
                {
                    "key": "value",
                    "link": "https://www.google.com",
                    "number": 1,
                    "nested": {"key": "value"},
                }
            ),
        },
    )
