import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import re

# Predefined skills list
skills_list = [
    "Python", "Java", "C++", "SQL", "JavaScript", "HTML", "CSS", 
    "Machine Learning", "Deep Learning", "Excel", "Pandas", "Numpy",
    "Communication", "Leadership", "Problem Solving", "Teamwork"
]

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

# Match skills using regex
def extract_skills(text, skills):
    matched = []
    for skill in skills:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            matched.append(skill)
    return matched

# Handle file upload
def browse_file():
    # Make dialog appear on top
    app.lift()
    app.attributes('-topmost', True)
    app.after_idle(app.attributes, '-topmost', False)

    file_path = filedialog.askopenfilename(
        title="Select a Resume PDF",
        filetypes=[("PDF files", "*.pdf")]
    )
    if file_path:
        resume_text = extract_text_from_pdf(file_path)
        matched_skills = extract_skills(resume_text, skills_list)

        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Matched Skills:\n")
        result_text.insert(tk.END, ", ".join(matched_skills) if matched_skills else "No skills matched.")
    else:
        messagebox.showwarning("No File", "Please select a valid PDF file.")

# Create main window
app = tk.Tk()
app.title("Automated Resume Matcher")
app.geometry("700x600")

# Job description label and textbox
tk.Label(app, text="Paste Job Description:").pack()
job_desc_text = tk.Text(app, height=7, width=80)
job_desc_text.pack()

# Upload button
tk.Button(app, text="Upload Resume", command=browse_file).pack(pady=10)

# Result display with scrollbar
result_text = tk.Text(app, height=20, width=80)
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(app, command=result_text.yview)
result_text.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Run the app
app.mainloop()
