from parser import ResumeParser

if __name__ == "__main__":
    parser = ResumeParser("sample_resume.pdf")
    data = parser.parse()

    print("\n📄 RESUME DATA EXTRACTED\n")
    for key, value in data.items():
        print(f"\n{key}:\n{value}")
