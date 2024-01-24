"""
Demo of using Canopy. Doesn't work yet.
"""

import os


# Step 2: Save the extracted text to a .txt file
def save_text_to_file(text, output_directory, file_name):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    file_path = os.path.join(output_directory, file_name)
    with open(file_path, "w") as file:
        file.write(text)
    return file_path


# Step 3: Use the canopy command to upsert the .txt file into your Canopy index
def upsert_to_canopy(file_path):
    os.system(f"canopy upsert {file_path}")


# Example usage
pdf_path = "nature_paper.pdf"
output_directory = "."
file_name = "document.txt"

# Extract text
extracted_text = ""

# Save to .txt
txt_file_path = save_text_to_file(extracted_text, output_directory, file_name)

# Upsert to Canopy
upsert_to_canopy(txt_file_path)
