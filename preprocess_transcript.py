'''
I tried doing OCR in the images available on the transcript however I kept running into errors
'''

import os
import string
from PyPDF2 import PdfReader
from num2words import num2words
import argparse

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF, or an empty string if an error occurs.
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""
        # Concatenate text from all pages in the PDF
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""

def clean_text(text):
    """
    Cleans the extracted text by converting to lowercase, removing punctuation,
    and converting digits to words.

    Args:
        text (str): Raw text to be cleaned.

    Returns:
        str: Cleaned text.
    """
    # Convert text to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    
    # Convert digits to words
    words = []
    for word in text.split():
        if word.isdigit():  # Check if the word is numeric
            try:
                word = num2words(int(word))  # Convert number to words
            except Exception as e:
                print(f"Error converting number {word}: {e}")
        words.append(word)
    
    # Join words back into a single string
    return " ".join(words)

def save_text_to_file(text, output_path):
    """
    Saves cleaned text to a .txt file.

    Args:
        text (str): Cleaned text to save.
        output_path (str): Path to the output .txt file.

    """
    try:
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(text)
        print(f"Text successfully saved to {output_path}")
    except Exception as e:
        print(f"Error saving text to file {output_path}: {e}")

def process_pdfs(input_folder, output_folder):
    """
    Processes all PDF files in the input folder by extracting, cleaning, 
    and saving their text to the output folder.

    Args:
        input_folder (str): Path to the folder containing PDF files.
        output_folder (str): Path to the folder for saving cleaned text files.

    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):  # Process only PDF files
            pdf_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".txt")
            
            print(f"Processing {filename}...")
            # Extract raw text from the PDF
            raw_text = extract_text_from_pdf(pdf_path)
            # Clean the extracted text
            cleaned_text = clean_text(raw_text)
            # Save the cleaned text to a .txt file
            save_text_to_file(cleaned_text, output_path)

if __name__ == "__main__":
    
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Extract text from PDF files, clean the text, and save it to .txt files in the specified output folder.")
    parser.add_argument("-inp", "--input_folder", required=True, help="Path to the folder containing input PDF files.")
    parser.add_argument("-op", "--output_folder", required=True, help="Path to the folder where cleaned text files will be saved.")

    args = parser.parse_args()
    
    # Process the PDFs
    process_pdfs(args.input_folder, args.output_folder)

