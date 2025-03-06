# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 23:12:20 2025

@author: Mohammed_magdy
"""

import streamlit as st
import pandas as pd
import json
import pdfkit
import markdown

def convert_md_to_pdf(md_text):
    """
    Convert Markdown text to PDF using pdfkit.
    This function converts the Markdown to HTML (with basic styling) and then to PDF.
    """
    # Convert Markdown to HTML
    html_text = markdown.markdown(md_text, extensions=['fenced_code'])
    # Add basic CSS for styling
    html_with_style = f"""
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{
            font-family: sans-serif;
            margin: 2em;
        }}
        h1, h2, h3, h4 {{
            color: #333;
        }}
        p {{
            font-size: 12pt;
        }}
        li {{
            font-size: 12pt;
            margin-bottom: 0.5em;
        }}
      </style>
    </head>
    <body>
      {html_text}
    </body>
    </html>
    """
    # On Streamlit Cloud, wkhtmltopdf is installed via packages.txt and available in PATH.
    pdf = pdfkit.from_string(html_with_style, False)
    return pdf

def load_student_answers(file):
    """
    Loads student answers from an uploaded Excel file.
    Expected columns: "Question" (e.g., Q1, Q2, ...) and "Answer" (e.g., A, B, C, D).
    """
    return pd.read_excel(file)

def load_feedback(file):
    """
    Loads the feedback data from an uploaded JSON file.
    The JSON structure should have keys like "Q1_Eq_q_1" containing:
      - "Q_text": The question text (with possible LaTeX formatting)
      - "Q_justifications": A list of [option_text, explanation] pairs.
      - "correct_choice_ID": The correct answer letter (e.g., "a").
    """
    return json.load(file)

def get_feedback_for_choice(student_answer, feedback_entry):
    """
    Maps the student's answer (e.g., 'A') to its corresponding feedback justification.
    The ordering in "Q_justifications" corresponds to:
      index 0 = a, index 1 = b, index 2 = c, index 3 = d.
    
    Returns:
      - student_choice (in lowercase),
      - correct_choice (from the feedback entry, in lowercase),
      - justification text corresponding to the student's answer.
    """
    student_choice = student_answer.strip().lower()
    correct_choice = feedback_entry['correct_choice_ID'].lower()
    
    # Convert letter to index: 'a' -> 0, 'b' -> 1, etc.
    mapping_index = ord(student_choice) - ord('a')
    if 0 <= mapping_index < len(feedback_entry['Q_justifications']):
        justification = feedback_entry['Q_justifications'][mapping_index][1]
    else:
        justification = "No justification available"
    
    return student_choice, correct_choice, justification

def generate_feedback_text(student_df, feedback_data):
    """
    Generate the feedback text output using the student answers and feedback data.
    The output is formatted in Markdown so that any LaTeX expressions (delimited by $)
    are rendered in the browser.
    """
    output = []
    output.append("# Feedback Report\n")
    
    # Process each student answer row
    for _, row in student_df.iterrows():
        # Assume Excel "Question" column provides identifiers like "Q1", "Q2", etc.
        question_identifier = str(row['Question']).strip()
        student_answer = row['Answer']
        
        # Find matching feedback entry by searching for keys that start with the question identifier
        feedback_entry = None
        for key in feedback_data:
            if key.startswith(question_identifier):
                feedback_entry = feedback_data[key]
                break
        
        output.append(f"## {question_identifier}\n")
        
        if feedback_entry is None:
            output.append(f"**No feedback found for question {question_identifier}.**\n")
            continue
        
        # Retrieve matching feedback based on the student's answer
        student_choice, correct_choice, justification = get_feedback_for_choice(student_answer, feedback_entry)
        
        # Construct output in Markdown format.
        output.append(f"- **Student Answer:** {student_answer.upper()}")
        output.append(f"- **Feedback:** {justification}")
        if student_choice != correct_choice:
            output.append(f"- **Correct Answer:** {correct_choice.upper()}")
        output.append("")  # Blank line for separation
    
    return "\n".join(output)

# Streamlit app interface
st.markdown("# **Student Feedback Generator**")
st.markdown("### **Upload the files below:**")
st.write("Upload the Excel file containing student answers and the JSON feedback file.")

# File uploader for Excel file
excel_file = st.file_uploader("Upload Student Answers Excel file", type=["xlsx"])
# File uploader for JSON file
json_file = st.file_uploader("Upload Feedback JSON file", type=["json"])

if st.button("Generate Feedback"):
    if excel_file is not None and json_file is not None:
        try:
            # Load files into appropriate data structures
            student_df = load_student_answers(excel_file)
            feedback_data = load_feedback(json_file)
            
            # Generate formatted feedback output in Markdown
            feedback_text = generate_feedback_text(student_df, feedback_data)
            
            st.markdown("### **Feedback Output**")
            st.markdown(feedback_text, unsafe_allow_html=True)
            
            # Convert the Markdown feedback into a PDF binary stream
            pdf_bytes = convert_md_to_pdf(feedback_text)
            
            # Provide a download button for the PDF
            st.download_button(
                label="Download Feedback as PDF",
                data=pdf_bytes,
                file_name="feedback_output.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please upload both files before generating feedback.")
