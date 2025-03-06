# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 23:12:20 2025

@author: Mohammed_magdy
"""

import streamlit as st
import pandas as pd
import json

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
        
        output.append(f"## {question_identifier}")
        
        if feedback_entry is None:
            output.append(f"**No feedback found for question {question_identifier}.**\n")
            continue
        
        # Retrieve matching feedback based on the student's answer
        student_choice, correct_choice, justification = get_feedback_for_choice(student_answer, feedback_entry)
        
        # Construct output in Markdown format. LaTeX formulas in the justifications (e.g., "$M = ...$")
        # will be rendered properly by Streamlit's Markdown.
        output.append(f"- **Student Answer:** {student_answer.upper()}")
        output.append(f"- **Feedback:** {justification}")
        if student_choice != correct_choice:
            output.append(f"- **Correct Answer:** {correct_choice.upper()}")
        output.append("")  # Blank line for separation
    
    return "\n".join(output)

# Streamlit app interface
st.markdown("# **Student Feedback Generator**")  # Bold and large title
st.markdown("### **Upload the files below:**")
st.write("Upload the Excel file containing student answers and the JSON feedback file.")

# File uploader for Excel file
excel_file = st.file_uploader("Upload Student Answers Excel file", type=["xlsx"])
# File uploader for JSON file
json_file = st.file_uploader("Upload Feedback JSON file", type=["json"])

# Add a Generate Feedback button
if st.button("Generate Feedback"):
    if excel_file is not None and json_file is not None:
        try:
            # Read files into appropriate data structures
            student_df = load_student_answers(excel_file)
            feedback_data = load_feedback(json_file)
            
            # Generate formatted feedback output in Markdown
            feedback_text = generate_feedback_text(student_df, feedback_data)
            
            st.markdown("### **Feedback Output**")
            # Display the feedback using st.markdown to render LaTeX expressions inline.
            st.markdown(feedback_text, unsafe_allow_html=True)
            
            # Provide a download button for the Markdown file (raw text)
            st.download_button(
                label="Download Feedback as Markdown",
                data=feedback_text,
                file_name="feedback_output.md",
                mime="text/markdown"
            )
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please upload both files before generating feedback.")
