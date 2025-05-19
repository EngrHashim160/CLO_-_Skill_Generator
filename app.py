"""
Main Application Module
This module provides a Streamlit-based user interface for the CLO Generator system.
"""

import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
from utils.document_processor import DocumentProcessor
from models.clo_generator import CLOGenerator

def main():
    """Main function to run the Streamlit application."""
    st.title("CLO Generator")
    st.write("Enter course content to generate Course Learning Outcomes (CLOs) and skill sets")

    # Initialize processors
    doc_processor = DocumentProcessor()
    clo_generator = CLOGenerator()

    # Add information about CLOs
    with st.expander("About Course Learning Outcomes (CLOs)"):
        st.markdown("""
        **Course Learning Outcomes (CLOs)** are statements that describe the knowledge, skills, and abilities that students should acquire by the end of a course. Well-written CLOs:

        1. Focus on student learning rather than teaching activities
        2. Are specific and measurable
        3. Use action verbs to describe what students will be able to do
        4. Align with program and institutional outcomes

        This tool helps generate appropriate Course Learning Outcomes (CLOs) based on your course content.
        """)

    # Text input
    course_title = st.text_input("Course Title", "")
    course_content = st.text_area("Enter Course Content", height=300,
                                 placeholder="Enter your course content here. Include topics, concepts, and skills that students should learn.")

    if st.button("Generate CLOs and Skills") and course_content:
        # Process the text
        with st.spinner("Processing text..."):
            # Preprocess the text
            preprocessed_text = doc_processor.preprocess_text(course_content)

            # Tokenize the text
            sentences, words = doc_processor.tokenize_text(preprocessed_text)

            # Extract keywords
            keywords = doc_processor.extract_keywords(words, top_n=30)

            # Add a small delay to show the spinner
            time.sleep(1)

        # Display text statistics
        st.subheader("Text Analysis")
        stats_col1, stats_col2 = st.columns(2)

        with stats_col1:
            st.metric("Total Words", len(words))
            st.metric("Unique Words", len(set(words)))

        with stats_col2:
            st.metric("Total Sentences", len(sentences))
            st.metric("Keywords Extracted", len(keywords))

        # Display extracted keywords
        st.subheader("Key Concepts Identified")
        st.write(", ".join(keywords))

        # Generate CLOs
        with st.spinner("Generating CLOs..."):
            num_clos = st.slider("Number of CLOs to generate", 3, 10, 5)
            clos = clo_generator.generate_clos(keywords, num_clos=num_clos)

            # Add a small delay to show the spinner
            time.sleep(1)

        # Display generated CLOs
        st.subheader("Generated Course Learning Outcomes (CLOs)")

        for i, clo in enumerate(clos):
            # Display the CLO
            st.markdown(f"""
            <div style="border-left: 5px solid #4e79a7; padding-left: 15px; margin-bottom: 20px;">
                <h4>CLO {i+1}</h4>
                <p style="font-size: 16px;">{clo['clo']}</p>
                <p><b>Action Verb:</b> {clo['action_verb'].capitalize()}</p>
                <p><b>Domain:</b> {clo['domain'].capitalize()}</p>
            </div>
            """, unsafe_allow_html=True)

        # Generate skill sets
        with st.spinner("Extracting skill sets..."):
            num_skills = st.slider("Number of skills to extract", 5, 15, 10)
            skills = clo_generator.extract_skills(keywords, clos, num_skills=num_skills)

            # Add a small delay to show the spinner
            time.sleep(1)

        # Display extracted skills
        st.subheader("Extracted Skill Sets")

        for i, skill in enumerate(skills):
            st.markdown(f"- {skill}")

        # Visualize domains
        st.subheader("Educational Domain Distribution")

        domain_counts = {}
        for clo in clos:
            domain = clo['domain']
            domain_counts[domain] = domain_counts.get(domain, 0) + 1

        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#4e79a7', '#f28e2c', '#e15759']
        bars = ax.bar(domain_counts.keys(), domain_counts.values(), color=colors[:len(domain_counts)])

        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1, str(int(height)),
                        ha='center', va='bottom')

        ax.set_xlabel("Educational Domain")
        ax.set_ylabel("Count")
        ax.set_title("Distribution of Educational Domains in CLOs")
        plt.xticks(rotation=0)
        st.pyplot(fig)

        # Export options
        st.subheader("Export Results")

        if st.button("Export to CSV"):
            # Create a filename based on course title or timestamp
            filename_base = course_title.strip() if course_title else f"course_content_{int(time.time())}"
            filename_base = "".join(c if c.isalnum() else "_" for c in filename_base)

            # Prepare CLO data for export
            clo_data = []
            for i, clo in enumerate(clos):
                clo_data.append({
                    "CLO Number": f"CLO {i+1}",
                    "CLO Statement": clo['clo'],
                    "Action Verb": clo['action_verb'].capitalize(),
                    "Domain": clo['domain'].capitalize(),
                    "Keywords": ", ".join(clo['keywords'])
                })

            # Create DataFrame and export
            clo_df = pd.DataFrame(clo_data)
            clo_csv_path = os.path.join("output", f"{filename_base}_CLOs.csv")
            clo_df.to_csv(clo_csv_path, index=False)

            # Prepare skill data for export
            skill_data = [{"Skill": skill} for skill in skills]
            skill_df = pd.DataFrame(skill_data)
            skill_csv_path = os.path.join("output", f"{filename_base}_Skills.csv")
            skill_df.to_csv(skill_csv_path, index=False)

            st.success(f"Results exported to CSV files in the output directory")

if __name__ == "__main__":
    # Create necessary directories if they don't exist
    os.makedirs("data", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    main()
