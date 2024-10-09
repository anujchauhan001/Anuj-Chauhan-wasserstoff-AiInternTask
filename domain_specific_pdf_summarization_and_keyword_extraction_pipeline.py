"""Install libraries for PDF processing, concurrency, and MongoDB integration. These libraries will handle PDF parsing (PyPDF2 or pdfminer.six), database integration (pymongo), and concurrency (concurrent.futures). """

!pip install PyPDF2 pdfminer.six pymongo nltk

""" Connect to MongoDB: Use the connection string to connect with MongoDB database."""

!pip install pymongo

from pymongo import MongoClient
from urllib.parse import quote_plus
connection_string = 'mongodb+srv://anujchauhan_user_name:123456789io@anujchauhan001db.xojem.mongodb.net/?retryWrites=true&w=majority&appName=AnujChauhan001db'
client = MongoClient(connection_string)
db = client['Anujchauhan001db']
collection = db['pdf_metadata']

print("Connected to MongoDB Atlas!")

""" Creating and Storing PDF Metadata in MongoDB"""

from datetime import datetime

pdf_metadata = {
    "name": "Sample PDF",
    "path": "/content/sample.pdf",
    "size": 2048,
    "summary": "This is a summary of the PDF content.",
    "keywords": ["keyword1", "keyword2", "keyword3"],
    "uploaded_at": datetime.utcnow()
}

print("PDF metadata has been successfully created!")

"""# This code is designed to process PDF files in a specified folder, extract text from them, generate summaries, and identify relevant keywords.
It then stores this information in a MongoDB database for easy retrieval and analysis."""

from datetime import datetime
import os
import json
from PyPDF2 import PdfReader
from pymongo import MongoClient
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter
import threading
import logging
import time

nltk.download('punkt')

# Set up error handling
logging.basicConfig(filename='pdf_processing.log', level=logging.ERROR)

def summarize_text(text):
    sentences = sent_tokenize(text)
    if len(sentences) == 0:
        return ""
    elif len(sentences) <= 3:
        return text
    elif len(sentences) <= 10:
        return ' '.join(sentences[:3])
    else:
        return ' '.join(sentences[:5])

def extract_keywords(text, num_keywords=5):
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalpha()]
    word_counts = Counter(words)
    keywords = word_counts.most_common(num_keywords)
    return [word for word, _ in keywords if word not in {"the", "is", "at", "on", "and"}]

def process_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            full_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"

        if not full_text.strip():  
            raise ValueError(f"No text found in {pdf_path}")

        summary = summarize_text(full_text)
        keywords = extract_keywords(full_text)

        pdf_metadata = {
            "name": os.path.basename(pdf_path),
            "path": pdf_path,
            "size": os.path.getsize(pdf_path),
            "summary": summary,
            "keywords": keywords,
            "uploaded_at": datetime.utcnow()
        }

        # Update MongoDB
        try:
            collection.update_one(
                {"path": pdf_path},
                {"$set": {
                    "summary": summary,
                    "keywords": keywords,
                    "size": pdf_metadata["size"],
                    "uploaded_at": pdf_metadata["uploaded_at"]
                }},
                upsert=True
            )
        except Exception as mongo_error:
            logging.error(f"MongoDB update failed for {pdf_path}: {mongo_error}")

        print(f"Processed and updated: {pdf_metadata['name']}")
        print(f"Size: {pdf_metadata['size']} bytes")
        print(f"Uploaded at: {pdf_metadata['uploaded_at']}")
        print("Summarized Successfully")

    except Exception as e:
        logging.error(f"Error processing {pdf_path}: {e}")
        print(f"Failed to process {pdf_path}. Check log for details.")

def process_pdfs_in_folder(folder_path):
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    threads = []

    start_time = time.time()  # Start the timer for performance metrics

    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        thread = threading.Thread(target=process_pdf, args=(pdf_path,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()  # End the timer
    total_time = end_time - start_time
    print(f"Total time taken to process PDFs: {total_time:.2f} seconds")

folder_path = '/content/pdf_files'
process_pdfs_in_folder(folder_path)
print("***************Summarized Every PDF Dataset Successfully ***************")

