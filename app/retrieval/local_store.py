import numpy as np
from openai import OpenAI
from scipy import spatial

client = OpenAI()


# Function to get embeddings
def get_embeddings(text):
    response = client.embeddings.create(input=text, model="text-embedding-ada-002")
    return response.data[0].embedding


# Class for the In-Memory Vector Store
class LocalVectorStore:
    class SearchResult:
        def __init__(self, text, rank, distance):
            self.text = text
            self.rank = rank
            self.distance = distance

        def to_json(self):
            return {"text": self.text, "rank": self.rank, "distance": self.distance}

    def __init__(self):
        self.text_chunks = []
        self.embeddings = []

    def add_text_chunk(self, text):
        embedding = get_embeddings(text)
        self.text_chunks.append(text)
        self.embeddings.append(embedding)

    def search(self, query, max_results=3):
        query_embedding = get_embeddings(query)
        distances = spatial.distance.cdist(
            [query_embedding], self.embeddings, "cosine"
        )[0]
        ranked_indices = np.argsort(distances)[:max_results]
        return [
            self.SearchResult(self.text_chunks[i], rank=rank, distance=distances[i])
            for rank, i in enumerate(ranked_indices)
        ]


if __name__ == "__main__":
    # Example usage
    vector_store = LocalVectorStore()
    vector_store.add_text_chunk("Sample text chunk 1")
    vector_store.add_text_chunk("Sample text chunk 2")

    # Search for a query
    results = vector_store.search("Query text")
    print(results)
