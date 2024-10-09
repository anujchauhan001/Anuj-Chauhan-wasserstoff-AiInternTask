This project is a Python-based script designed to efficiently process multiple PDF documents. The script extracts text, generates summaries, and identifies relevant keywords, storing the results in a MongoDB database. The processing pipeline is built to handle various document lengths and types while ensuring robust error handling and performance optimization.

## Table of Contents
1. System Requirements
2. Setup Instructions
3. How It Works
4. Usage
5. Error Handling


## System Requirements
- Python 3.7 or higher
- Required Python libraries:
  - PyPDF2
  - nltk
  - pymongo
  - threading
  - collections
- MongoDB server (local or remote)

## Setup Instructions
1. Install the required libraries: You can install the required libraries using pip.
2. Download NLTK data: The script uses the NLTK library for text processing. Download the necessary data by running.
3. MongoDB Setup: Ensure you have MongoDB installed and running. You can either set up a local instance or use a cloud-based MongoDB service. Update the MongoDB connection settings in the script as necessary.
4. Prepare PDF Files: Place your PDF files in the pdf_files directory located in the project root.

## How It Works
The PDF Processing Pipeline performs the following key functions:

Text Extraction: It reads the content of PDF files using the PyPDF2 library.
Summarization: It generates concise summaries based on the extracted text, adjusting the length according to the document size.
Keyword Extraction: It identifies and extracts relevant keywords from the document content.
MongoDB Integration: The script stores document metadata, summaries, and keywords in a MongoDB database, ensuring proper updates after processing.

## Usage
The script will automatically process all the PDF files located in the pdf_files directory. It will extract the necessary information, summarize the contents, and generate keywords. Once the processing is complete, the results will be stored in the MongoDB database that you have configured. This allows you to easily access and manage the metadata, summaries, and keywords generated from your PDF documents.

## Error Handling
The script includes robust error handling to manage issues such as corrupted files or MongoDB update failures. Any errors encountered during processing are logged in a file named pdf_processing.log, allowing for easy debugging and issue resolution.






