from unstructured.partition.auto import partition


def extract_text_from_pdf(pdf_path):
    elements = partition(pdf_path)
    return elements


elements = partition("doc_37.pdf")

for element in elements:
    print(f"Page {element.metadata.page_number} - {element.id}: {element.text}\n")
