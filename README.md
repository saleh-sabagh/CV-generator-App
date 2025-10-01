# CV Generator App

A **Python-based Resume Builder Application** with a user-friendly GUI that allows users to create professional resumes efficiently.

## Features

- Enter personal information, work experience, education, skills, and certifications in separate fields.
- Two save options:
  - **Temporary Save**: Save progress without finalizing.
  - **Final Save**: Save all entered data and proceed to PDF generation.
- Choose from **three PDF templates** to generate a dynamic, professional resume based on the provided information.
- Automatically fills the selected template with the entered data, saves the PDF, and displays it.

## How It Works

1. Launch the application.
2. Fill in the fields with your personal, educational, and professional information.
3. Save your work temporarily or finalize it.
4. After finalizing, select one of the three PDF templates.
5. The application generates a fully populated PDF resume that can be saved and viewed.

## Technologies Used

- Python
- GUI library (e.g., Tkinter, PyQt, or PySide6 — adjust as needed)
- PDF generation library (e.g., ReportLab, FPDF)

## Installation

1. Clone the repository:  
   ```bash
   git clone https://github.com/saleh-sabagh/CV-generator-App.git


2. Create a virtual environment and install dependencies:
   ```bash
    python -m venv venv
    pip install -r requirements.txt

3. Run the application:
    ```bash
    python main.py
