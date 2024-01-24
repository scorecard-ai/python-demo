import os

from scorecard.client import Scorecard
from scorecard.types import RunStatus

from app.chat import pdf_rag

client = Scorecard(api_key=os.environ["SCORECARD_API_KEY"])

# Ask for a testset ID and scoring config ID
testset_id = int(input("Testset ID: "))
scoring_config_id = int(input("Scoring Config ID: "))

run = client.run.create(testset_id=testset_id, scoring_config_id=scoring_config_id)
if run.id is None:
    raise ValueError("Run ID is None, cannot update status.")

client.run.update_status(run.id, status=RunStatus.RUNNING_EXECUTION)
testcases = client.testset.get_testcases(testset_id)

for testcase in testcases.results[:1]:
    if testcase.id is None:
        continue

    testcase_id = testcase.id
    query = testcase.user_query

    print(f"Running testcase {testcase_id}...")
    print(f"User query: {query}")

    if testcase.custom_inputs is None:
        raise ValueError("Testcase has no custom inputs.")
    file = testcase.custom_inputs["input_file_url"]
    if file is None:
        raise ValueError("Testcase has no input file.")
    print(file)
    print(file.url)  # type: ignore
    (
        extracted_text,
        search_results,
        assistant_response,
        computed_prompt,
    ) = pdf_rag.run_rag(
        file.url, query  # type: ignore
    )

    client.testrecord.create(
        run_id=run.id,
        testcase_id=testcase_id,
        testset_id=395,
        user_query=testcase.user_query,
        custom_inputs=testcase.custom_inputs,
        custom_outputs={"extracted_text": extracted_text},
        context=search_results,
        response=assistant_response,
        # full_prompt=computed_prompt,
    )

client.run.update_status(run.id, status=RunStatus.AWAITING_SCORING)

print("Finished running testcases.")

# async def run_tests():
#     await client.run_tests(
#         # Your Testset ID
#         input_testset_id=395,
#         # Your Scoring Config ID
#         scoring_config_id=34,
#         # The model invocation that you would like to test
#         model_invocation=lambda prompt: prompt,
#     )


# # Run the async function
# asyncio.run(run_tests())
