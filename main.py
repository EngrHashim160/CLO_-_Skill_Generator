"""
Main entry point for the CLO Generator system.
"""

import os
import argparse
from utils.document_processor import DocumentProcessor
from models.clo_generator import CLOGenerator

def process_document(file_path, output_dir, num_clos=5, num_skills=10):
    """
    Process a document to generate CLOs and skill sets.
    
    Args:
        file_path (str): Path to the document file
        output_dir (str): Directory to save the output
        num_clos (int): Number of CLOs to generate
        num_skills (int): Number of skills to extract
    """
    # Initialize processors
    doc_processor = DocumentProcessor()
    clo_generator = CLOGenerator()
    
    # Extract text from the document
    print(f"Processing document: {file_path}")
    text = doc_processor.extract_text_from_file(file_path)
    
    # Preprocess the text
    print("Preprocessing text...")
    preprocessed_text = doc_processor.preprocess_text(text)
    
    # Tokenize the text
    print("Tokenizing text...")
    sentences, words = doc_processor.tokenize_text(preprocessed_text)
    
    # Extract keywords
    print("Extracting keywords...")
    keywords = doc_processor.extract_keywords(words, top_n=30)
    
    # Generate CLOs
    print(f"Generating {num_clos} CLOs...")
    clos = clo_generator.generate_clos(keywords, num_clos=num_clos)
    
    # Extract skill sets
    print(f"Extracting {num_skills} skills...")
    skills = clo_generator.extract_skills(keywords, clos, num_skills=num_skills)
    
    # Print results
    print("\n=== Generated Course Learning Outcomes (CLOs) ===")
    for i, clo in enumerate(clos):
        print(f"CLO {i+1}: {clo['clo']}")
        print(f"Taxonomy Level: {clo['taxonomy_level'].capitalize()} | Action Verb: {clo['action_verb'].capitalize()}")
        print()
    
    print("\n=== Extracted Skill Sets ===")
    for i, skill in enumerate(skills):
        print(f"- {skill}")
    
    # Save results to files
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        
        # Save CLOs
        clo_file_path = os.path.join(output_dir, "generated_clos.txt")
        with open(clo_file_path, "w", encoding="utf-8") as f:
            f.write("=== Generated Course Learning Outcomes (CLOs) ===\n\n")
            for i, clo in enumerate(clos):
                f.write(f"CLO {i+1}: {clo['clo']}\n")
                f.write(f"Taxonomy Level: {clo['taxonomy_level'].capitalize()} | Action Verb: {clo['action_verb'].capitalize()}\n\n")
        
        # Save skills
        skill_file_path = os.path.join(output_dir, "extracted_skills.txt")
        with open(skill_file_path, "w", encoding="utf-8") as f:
            f.write("=== Extracted Skill Sets ===\n\n")
            for skill in skills:
                f.write(f"- {skill}\n")
        
        print(f"\nResults saved to {output_dir}")

def main():
    """Main function to run the CLO Generator from the command line."""
    parser = argparse.ArgumentParser(description="Generate CLOs and skill sets from course content")
    parser.add_argument("file_path", help="Path to the document file")
    parser.add_argument("--output", "-o", help="Directory to save the output", default="output")
    parser.add_argument("--clos", "-c", type=int, help="Number of CLOs to generate", default=5)
    parser.add_argument("--skills", "-s", type=int, help="Number of skills to extract", default=10)
    
    args = parser.parse_args()
    
    process_document(args.file_path, args.output, args.clos, args.skills)

if __name__ == "__main__":
    main()
