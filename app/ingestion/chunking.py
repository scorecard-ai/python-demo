import nltk
from nltk.tokenize import sent_tokenize

nltk.download("punkt")  # Download the required model once


def chunk_text_by_sentence(text, desired_chunk_size=512):
    """
    Splits the text into chunks by sentence.

    :param text: The text to be chunked.
    :param desired_chunk_size: Desired chunk size in characters, adjusted to not break sentences.
    :return: A list of text chunks.
    """
    print("Chunking text by sentence...")
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""
    total_length = 0

    for sentence in sentences:
        if len(current_chunk) + len(sentence) > desired_chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            total_length += len(current_chunk)
            current_chunk = sentence
        else:
            current_chunk += " " + sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    print(
        f"Chunked into {len(chunks)} chunks with average length {total_length / len(chunks)}"
    )

    return chunks


def simple_chunk_text(text, desired_chunk_size=512):
    """
    Splits the text into chunks without breaking words.

    :param text: The text to be chunked.
    :param desired_chunk_size: Desired chunk size in characters.
    :return: A list of text chunks.
    """
    print("Chunking text by word...")
    chunks = []
    current_chunk = []
    total_length = 0

    for word in text.split():
        if sum(len(w) for w in current_chunk) + len(word) <= desired_chunk_size:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            total_length += len(chunks[-1])
            current_chunk = [word]

    if current_chunk:
        chunks.append(" ".join(current_chunk))
        total_length += len(chunks[-1])

    print(
        f"Chunked into {len(chunks)} chunks with average length {total_length / len(chunks)}"
    )

    return chunks
