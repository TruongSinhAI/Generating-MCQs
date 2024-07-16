import streamlit as st
import requests

# Define the FastAPI endpoint URL
FASTAPI_URL = "http://localhost:8080/generate_mcqs/"

# Streamlit UI
st.title("MCQ Generator")

# Input text
text_input = st.text_area("Enter the text you want to generate MCQs from:")

if st.button("Generate MCQs"):
    if text_input:
        # Call the FastAPI endpoint
        response = requests.post(FASTAPI_URL, json={"text": text_input})

        if response.status_code == 200:
            mcqs = response.json()

            st.write("## Generated MCQs")
            for i, mcq in enumerate(mcqs):
                st.write(f"### Question {i + 1}: {mcq['questionTitle']}")
                if mcq['questionImage']!= "": st.image(mcq['questionImage'])
                st.write(f"**Score:** {mcq['questionScore']}")
                st.write("**Answers:**")
                for answer in mcq['questionAnswer']:
                    st.write(f"- {'(Correct)' if answer['status'] else '(Incorrect)'} {answer['title']}")
        else:
            st.error("Error generating MCQs. Please try again.")
    else:
        st.error("Please enter some text.")
