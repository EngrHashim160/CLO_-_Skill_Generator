"""
Document Processor Module
This module handles the extraction and preprocessing of text from various document formats.
"""

import os
import re
import PyPDF2
import docx
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download necessary NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

class DocumentProcessor:
    """Class for processing documents and extracting text content."""

    def __init__(self):
        """Initialize the document processor."""
        self.stop_words = set(stopwords.words('english'))

    def extract_text_from_file(self, file_path):
        """
        Extract text from a file based on its extension.

        Args:
            file_path (str): Path to the document file

        Returns:
            str: Extracted text content
        """
        _, file_extension = os.path.splitext(file_path)

        if file_extension.lower() == '.pdf':
            return self._extract_from_pdf(file_path)
        elif file_extension.lower() in ['.docx', '.doc']:
            return self._extract_from_docx(file_path)
        elif file_extension.lower() == '.txt':
            return self._extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    def _extract_from_pdf(self, file_path):
        """Extract text from a PDF file."""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        return text

    def _extract_from_docx(self, file_path):
        """Extract text from a DOCX file."""
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text

    def _extract_from_txt(self, file_path):
        """Extract text from a TXT file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text

    def process_text(self, text):
        """
        Process raw text input directly.

        Args:
            text (str): Raw text content

        Returns:
            tuple: (preprocessed_text, sentences, words, keywords)
        """
        # Preprocess the text
        preprocessed_text = self.preprocess_text(text)

        # Tokenize the text
        sentences, words = self.tokenize_text(preprocessed_text)

        # Extract keywords
        keywords = self.extract_keywords(words, top_n=30)

        return preprocessed_text, sentences, words, keywords

    def preprocess_text(self, text):
        """
        Preprocess the extracted text.

        Args:
            text (str): Raw text content

        Returns:
            str: Preprocessed text
        """
        # Convert to lowercase
        text = text.lower()

        # Remove special characters and numbers
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\d+', ' ', text)

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def tokenize_text(self, text):
        """
        Tokenize text into sentences and words.

        Args:
            text (str): Preprocessed text

        Returns:
            tuple: (sentences, words)
        """
        sentences = sent_tokenize(text)
        words = word_tokenize(text)

        # Remove stopwords
        filtered_words = [word for word in words if word not in self.stop_words]

        return sentences, filtered_words

    def extract_keywords(self, words, top_n=50):
        """
        Extract keywords from the text based on frequency.

        Args:
            words (list): List of words
            top_n (int): Number of top keywords to return

        Returns:
            list: Top keywords
        """
        # Count word frequencies
        word_freq = {}
        for word in words:
            if len(word) > 3:  # Only consider words longer than 3 characters
                if word in word_freq:
                    word_freq[word] += 1
                else:
                    word_freq[word] = 1

        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

        # Return top N keywords
        return [word for word, freq in sorted_words[:top_n]]
