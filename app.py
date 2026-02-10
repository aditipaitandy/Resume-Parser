import streamlit as st
import tempfile
from parser import ResumeParser

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Resume Parser",
    page_icon="📄",
    layout="wide"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.main-title {
    font-size: 38px;
    font-weight: 700;
}
.section-box {
    padding: 20px;
    border-radius: 12px;
    background-color: #f9f9f9;
    margin-bottom: 20px;
}
.skill-chip {
    display: inline-block;
    background-color: #e0ecff;
    color: #003366;
    padding: 6px 12px;
    border-radius: 20px;
    margin: 4px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("📂 Upload Resume")
uploaded_file = st.sidebar.file_uploader(
    "Upload PDF Resume",
    type=["pdf"]
)

st.sidebar.markdown("---")
st.sidebar.info("Built using Python, Streamlit & PDF Parsing")

# ---------- MAIN HEADER ----------
st.markdown('<div class="main-title">📄 Resume Parser System</div>', unsafe_allow_html=True)
st.write("Upload a resume to extract structured information like skills, projects, and education.")

# ---------- PROCESS FILE ----------
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    parser = ResumeParser(temp_path)
    data = parser.parse()

    st.success("✅ Resume parsed successfully!")

    col1, col2 = st.columns(2)

    # ---------- LEFT COLUMN ----------
    with col1:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("👤 Personal Details")
        st.write(f"**Name:** {data.get('Name', 'Not Found')}")
        st.write(f"**Email:** {data.get('Email', 'Not Found')}")
        st.write(f"**Phone:** {data.get('Phone', 'Not Found')}")
        st.write(f"**LinkedIn:** {data.get('LinkedIn', 'Not Found')}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("🎓 Education")
        st.write(data.get("Education", "Not Found"))
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------- RIGHT COLUMN ----------
    with col2:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("🧠 Summary")
        st.write(data.get("Summary", "Not Found"))
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("🛠 Skills")

        skills_text = data.get("Skills", "")
        if skills_text:
            skills = [s.strip() for s in skills_text.replace("\n", ",").split(",") if s.strip()]
            for skill in skills:
                st.markdown(f'<span class="skill-chip">{skill}</span>', unsafe_allow_html=True)
        else:
            st.write("Not Found")

        st.markdown('</div>', unsafe_allow_html=True)

    # ---------- FULL WIDTH SECTIONS ----------
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("📌 Projects")
    st.write(data.get("Projects", "Not Found"))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("📜 Certifications")
    st.write(data.get("Certifications", "Not Found"))
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("⬅️ Upload a resume PDF from the sidebar to get started.")
