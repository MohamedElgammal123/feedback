# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 21:58:12 2025

@author: Mohammed_magdy
"""

import streamlit as st
import pandas as pd
import json
from io import StringIO, BytesIO

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
      - "Q_text": The question text (not printed in output)
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
    """
    output = []
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
        
        if feedback_entry is None:
            output.append(f"{question_identifier}: No feedback found for question {question_identifier}\n")
            continue
        
        # Retrieve matching feedback based on the student's answer
        student_choice, correct_choice, justification = get_feedback_for_choice(student_answer, feedback_entry)
        
        # Construct output lines in the required text format
        output.append(f"{question_identifier}: student answer: {student_answer.upper()}")
        output.append(f"feedback: {justification}")
        # If student's answer is incorrect, include the correct answer line.
        if student_choice != correct_choice:
            output.append(f"correct answer is: {correct_choice.upper()}")
        output.append("")  # blank line for separation
    return "\n".join(output)

# Streamlit app
st.title("Student Feedback Generator")

st.write("Upload the Excel file containing student answers and the JSON feedback file.")

# File uploader for Excel file
excel_file = st.file_uploader("Upload Student Answers Excel file", type=["xlsx"])
# File uploader for JSON file
json_file = st.file_uploader("Upload Feedback JSON file", type=["json"])

if excel_file and json_file:
    try:
        # Read files into appropriate data structures
        student_df = load_student_answers(excel_file)
        # json.load() requires a text stream so we decode bytes to string if needed.
        feedback_data = load_feedback(json_file)
        
        # Generate feedback output text
        feedback_text = generate_feedback_text(student_df, feedback_data)
        
        st.subheader("Feedback Output")
        st.text_area("Feedback", feedback_text, height=300)
        
        # Provide a download button for the text file
        st.download_button(
            label="Download Feedback as TXT",
            data=feedback_text,
            file_name="feedback_output.txt",
            mime="text/plain"
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")
