"""
Test script for the CLO Generator system.
"""

import os
import sys
import nltk

# Download necessary NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

from utils.document_processor import DocumentProcessor
from models.clo_generator import CLOGenerator

def test_document_processor():
    """Test the document processor functionality."""
    print("Testing DocumentProcessor...")

    # Create a test document
    test_file_path = "test_document.txt"
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write("""
        # Introduction to Machine Learning

        Machine learning is a field of artificial intelligence that uses statistical techniques to give
        computer systems the ability to "learn" from data, without being explicitly programmed.

        ## Topics Covered

        1. Supervised Learning
           - Classification
           - Regression

        2. Unsupervised Learning
           - Clustering
           - Dimensionality Reduction

        3. Reinforcement Learning
           - Q-Learning
           - Policy Gradients

        ## Learning Objectives

        Students will understand the fundamental concepts of machine learning and be able to apply
        various algorithms to solve real-world problems. They will gain experience with data
        preprocessing, model selection, and evaluation techniques.
        """)

    # Initialize document processor
    doc_processor = DocumentProcessor()

    # Test text extraction
    text = doc_processor.extract_text_from_file(test_file_path)
    print(f"Extracted {len(text)} characters from the test document")

    # Test text preprocessing
    preprocessed_text = doc_processor.preprocess_text(text)
    print(f"Preprocessed text length: {len(preprocessed_text)} characters")

    # Test tokenization
    sentences, words = doc_processor.tokenize_text(preprocessed_text)
    print(f"Tokenized into {len(sentences)} sentences and {len(words)} words")

    # Test keyword extraction
    keywords = doc_processor.extract_keywords(words, top_n=10)
    print(f"Extracted {len(keywords)} keywords: {', '.join(keywords)}")

    # Clean up
    os.remove(test_file_path)

    print("DocumentProcessor tests completed successfully\n")
    return keywords

def test_clo_generator(keywords):
    """Test the CLO generator functionality."""
    print("Testing CLOGenerator...")

    # Initialize CLO generator
    clo_generator = CLOGenerator()

    # Test CLO generation
    clos = clo_generator.generate_clos(keywords, num_clos=3)
    print(f"Generated {len(clos)} CLOs:")
    for i, clo in enumerate(clos):
        print(f"CLO {i+1}: {clo['clo']}")
        print(f"Taxonomy Level: {clo['taxonomy_level']} | Action Verb: {clo['action_verb']}")

    # Test skill extraction
    skills = clo_generator.extract_skills(keywords, clos, num_skills=5)
    print(f"\nExtracted {len(skills)} skills:")
    for skill in skills:
        print(f"- {skill}")

    print("CLOGenerator tests completed successfully")

def main():
    """Main function to run the tests."""
    print("=== CLO Generator System Tests ===\n")

    # Test document processor
    keywords = test_document_processor()

    # Test CLO generator
    test_clo_generator(keywords)

    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    # Add the parent directory to the path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    main()
