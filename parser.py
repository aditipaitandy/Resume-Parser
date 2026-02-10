import re
import pdfplumber


class ResumeParser:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.text = ""

    # ---------------- BASIC TEXT EXTRACTION ----------------
    def extract_text(self):
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                self.text += page.extract_text() + "\n"

    # ---------------- PERSONAL DETAILS ----------------
    def extract_name(self):
        return self.text.split("\n")[0].strip()

    def extract_email(self):
        match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', self.text)
        return match.group() if match else None

    def extract_phone(self):
        match = re.search(r'\+91[-\s]?\d{10}', self.text)
        return match.group() if match else None

    def extract_linkedin(self):
        match = re.search(r'linkedin\.com/\S+', self.text)
        return match.group() if match else None

    # ---------------- SECTION EXTRACTION ----------------
    def extract_section(self, start, end):
        pattern = rf"{start}(.*?){end}"
        match = re.search(pattern, self.text, re.S | re.I)
        return match.group(1).strip() if match else None

    def extract_summary(self):
        return self.extract_section("Summary", "Skills")

    def extract_skills(self):
        return self.extract_section("Skills", "Projects")

    def extract_projects(self):
        return self.extract_section("Projects", "Certifications")

    def extract_certifications(self):
        return self.extract_section("Certifications", "Education")

    def extract_education(self):
        pattern = r"Education(.*)"
        match = re.search(pattern, self.text, re.S | re.I)
        return match.group(1).strip() if match else None

    # ---------------- FINAL PARSER ----------------
    def parse(self):
        self.extract_text()
        return {
            "Name": self.extract_name(),
            "Email": self.extract_email(),
            "Phone": self.extract_phone(),
            "LinkedIn": self.extract_linkedin(),
            "Summary": self.extract_summary(),
            "Skills": self.extract_skills(),
            "Projects": self.extract_projects(),
            "Certifications": self.extract_certifications(),
            "Education": self.extract_education()
        }
