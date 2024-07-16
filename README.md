![project-image01](https://github.com/user-attachments/assets/25f0275d-05df-413f-9117-08b539c0a7c6)

# MCQ Generator

This project is a web application that generates Multiple Choice Questions (MCQs) from a given text. It uses a FastAPI backend to handle the MCQ generation logic and a Streamlit frontend to provide a user-friendly interface for interacting with the backend.

## Features

- **Text Summarization:** Summarizes the input text to extract key information.
- **MCQ Generation:** Generates MCQs from the summarized text, including questions, answers, and scores.
- **Interactive Web UI:** Provides an easy-to-use web interface for inputting text and viewing generated MCQs.

## Technologies Used

- **FastAPI:** A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
- **Streamlit:** An open-source app framework for Machine Learning and Data Science projects.
- **NLTK:** Summarize text, remove Stop words, sentences and words tokenize, filter the keyphrase from text.

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Backend Setup (FastAPI)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mcq-generator.git](https://github.com/TruongSinhAI/Generating-MCQs.git
   cd Generating-MCQs
   ```
2. Run backend:
   ```bash
   python main.py
   ```  
3. Run Front end:
   ```bash
   streamlit run app.py
   ```

