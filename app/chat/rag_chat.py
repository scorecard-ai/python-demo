from openai import OpenAI

from ..extraction import textract, upload
from ..ingestion import chunking
from ..retrieval import local_store

client = OpenAI()

# Upload the file and run textract
TEST_FILE_PATH = "jan_6.pdf"
BUCKET_NAME = "scorecard-testing"
object_key = upload.upload_file_to_s3(TEST_FILE_PATH, BUCKET_NAME)
text = textract.extract_text_from_pdf(BUCKET_NAME, object_key)

# Now, chunk and add this to the local store
chunks = chunking.simple_chunk_text(text)
vector_store = local_store.LocalVectorStore()
for chunk in chunks:
    vector_store.add_text_chunk(chunk)

# Now add those results to a prompt
PROMPT_TEMPLATE = """Given the search results below, please answer the user's query.
Make sure to include references to the search results in your answer.
Do not add any information that is not in the search results.

<SEARCH_RESULTS>
{search_results}
</SEARCH_RESULTS>
<USER_QUERY>
{user_question}
</USER_QUERY>
"""

while True:
    # Now, ask the user for a query
    query = input("Enter a query: ")

    # Find the most relevant chunks
    results = vector_store.search(query, max_results=3)

    print("Search results: ")
    for result in results:
        print(f"{result.rank} ({result.distance}): {result.text}")

    formatted_results = "\n".join(f"{result.rank}. {result.text}" for result in results)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "system",
                "content": PROMPT_TEMPLATE.format(
                    search_results=formatted_results, user_question=query
                ),
            },
        ],
    )

    # Print the response
    print("Assistant: ")
    print(response.choices[0].message.content)
