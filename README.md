# OpenSource Feedback Generator Framework for Scantron Exams

An open-source framework designed to generate detailed feedback reports for scantron-based exams. This app allows educators to easily upload student answers and corresponding JSON feedback data, then automatically processes and outputs customized feedback for each exam question.

## Features

- **Easy File Upload:**  
  Upload student answers via an Excel file and corresponding feedback via a JSON file.
  
- **Automated Feedback Generation:**  
  Automatically matches student answers with detailed justifications and provides correct answer information if a student's response is incorrect.
  
- **Downloadable Reports:**  
  View the generated feedback in the web interface and download it as a TXT file.
  
- **Streamlit-Powered Interface:**  
  Enjoy a modern, interactive interface built with Streamlit, making it simple for non-technical users to generate feedback reports.

## Technologies Used

- [Streamlit](https://streamlit.io/) – for creating interactive web applications.
- [Pandas](https://pandas.pydata.org/) – for data manipulation and reading Excel files.
- [Openpyxl](https://openpyxl.readthedocs.io/en/stable/) – for Excel file support.
- [JSON](https://www.json.org/) – for structured feedback data.

## Getting Started

### Prerequisites

Ensure you have Python installed. It is recommended to use a virtual environment. Then, install the required packages:

```bash
pip install -r requirements.txt
