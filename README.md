# CLO Generator

**Student Name:** Muhammad Hashim
**Registration No:** 21MDSWE160

A specialized system for generating Course Learning Outcomes (CLOs) and skill sets from course content.

## Overview

The CLO Generator is designed to help educators automatically generate well-formed Course Learning Outcomes (CLOs) and relevant skill sets from their course content. The system uses natural language processing techniques to analyze course content and generate appropriate learning outcomes.

## Features

- Direct text input for course content
- Preprocess and analyze text using NLP techniques
- Generate well-formed CLOs based on course content
- Extract relevant skill sets from course content
- Visualize the generated CLOs and skills
- Export results to CSV files

## Project Structure

```
21MDSWE160_HASHIM_DL_CEP/
├── data/               # Directory for storing temporary data
├── models/             # NLP models for CLO generation
│   ├── __init__.py
│   └── clo_generator.py
├── output/             # Directory for storing generated outputs
├── utils/              # Utility functions
│   ├── __init__.py
│   └── document_processor.py
├── __init__.py
├── app.py              # Streamlit web application
├── run_app.py          # Script to run the Streamlit app
├── README.md
└── requirements.txt    # Project dependencies
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/EngrHashim160/CLO_-_Skill_Generator.git
   cd 21MDSWE160_HASHIM_DL_CEP
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Web Application

To run the web application:

```
streamlit run run_app.py
```

Then, open your web browser and navigate to the URL displayed in the terminal (usually http://localhost:8501).

### Using the Application

1. Enter a course title (optional)
2. Type or paste your course content in the text area
3. Click "Generate CLOs and Skills"
4. Adjust the number of CLOs and skills using the sliders
5. View the generated CLOs and skills
6. Export the results to CSV files if needed

## How It Works

1. **Text Processing**: The system processes the entered course content and preprocesses it to remove noise and normalize the text.

2. **Keyword Extraction**: Key terms and concepts are extracted from the preprocessed text using NLP techniques.

3. **CLO Generation**: Well-formed CLOs are generated based on the extracted keywords and concepts from the course content.

4. **Skill Set Extraction**: Relevant skills are extracted from the course content and organized into a coherent set.

5. **Visualization and Export**: The results are presented in a user-friendly format and can be exported to CSV files for further use.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
