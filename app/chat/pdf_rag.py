from openai import OpenAI

from ..extraction import textract
from ..ingestion import chunking
from ..retrieval import local_store

client = OpenAI()


def run_rag(file_path, query):
    # Upload the file and run textract
    bucket_name, object_key = textract.get_bucket_and_key_from_url(file_path)
    extracted_text = textract.extract_text_from_pdf(bucket_name, object_key)

    # Now, chunk and add this to the local store
    chunks = chunking.simple_chunk_text(extracted_text)
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
    # Find the most relevant chunks
    search_results = vector_store.search(query, max_results=3)

    print("Search results: ")
    for result in search_results:
        print(f"Result {result.rank} ({result.distance}): {result.text}\n")

    formatted_results = "\n".join(
        f"Result {result.rank} ({result.distance}):. {result.text}\n"
        for result in search_results
    )

    computed_prompt = PROMPT_TEMPLATE.format(
        search_results=formatted_results, user_question=query
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "system",
                "content": computed_prompt,
            },
        ],
    )

    # Print the response
    print("Assistant: ")
    assistant_response = response.choices[0].message.content
    print(assistant_response)

    return extracted_text, formatted_results, assistant_response, computed_prompt
