# Student Feedback Generator

An interactive, open-source tool that generates detailed feedback reports for scantron-based exams. This application allows educators to upload an Excel file with student answers and a JSON file containing feedback data (with LaTeX-formatted math expressions). The app then produces a Markdown report that is converted into a PDF, ensuring that the final output preserves rendered math expressions as seen in the app.

## Features

- **File Upload:**  
  Upload an Excel file with student answers (including the original file name as a referral) and a JSON file with feedback details.
  
- **Feedback Generation:**  
  Automatically maps each student answer to the corresponding feedback, refining the output with rendered LaTeX math expressions.

- **PDF Conversion:**  
  Generates a PDF from the Markdown report (with MathJax for proper math rendering) so that the final output matches the on-screen view.

## Technologies Used

- **[Streamlit](https://streamlit.io/):** For building the interactive web application.  
- **[Pandas](https://pandas.pydata.org/):** For data manipulation and reading Excel files.  
- **[openpyxl](https://openpyxl.readthedocs.io/en/stable/):** To support Excel file reading in Pandas.  
- **[pdfkit](https://pypi.org/project/pdfkit/):** For converting HTML (generated from Markdown) to PDF.  
- **[markdown](https://pypi.org/project/Markdown/):** For converting Markdown text to HTML.  
- **wkhtmltopdf:** A system dependency installed via `packages.txt` (in Streamlit Cloud) that pdfkit uses to generate PDFs.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/<your-username>/student-feedback-generator.git
   cd student-feedback-generator
