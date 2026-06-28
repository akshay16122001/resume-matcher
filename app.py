import streamlit as st
from parser import parse_resume
from matcher import match_resume_to_jd, generate_ats_resume
from pdf_generator import generate_pdf_resume
import tempfile
import os

st.set_page_config(
    page_title="AI Resume Matcher",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Resume & Job Matcher")
st.markdown("**Upload your resume + paste a JD → Get ATS-optimized tailored resume PDF!**")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Your Resume")
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF only)",
        type="pdf"
    )
    if uploaded_file:
        st.success(f"✅ Uploaded: {uploaded_file.name}")

with col2:
    st.subheader("💼 Job Description")
    jd_text = st.text_area(
        "Paste the job description here",
        height=250,
        placeholder="Paste the full job description here..."
    )

st.divider()

if st.button("🚀 Generate Tailored Resume", type="primary", use_container_width=True):
    if not uploaded_file:
        st.error("⚠️ Please upload your resume PDF!")
    elif not jd_text:
        st.error("⚠️ Please paste a job description!")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        try:
            with st.spinner("📄 Reading your resume..."):
                resume_text = parse_resume(tmp_path)

            with st.spinner("🔍 Analyzing match..."):
                analysis = match_resume_to_jd(resume_text, jd_text)

            st.subheader("📊 Match Analysis")
            st.markdown(analysis)
            st.divider()

            with st.spinner("✨ Building ATS-optimized resume..."):
                tailored_content = generate_ats_resume(resume_text, jd_text)

            st.subheader("📄 Your Tailored Resume")
            st.markdown(tailored_content)
            st.divider()

            with st.spinner("📥 Generating PDF..."):
                output_pdf = "tailored_resume.pdf"
                generate_pdf_resume(tailored_content, output_pdf)

                with open(output_pdf, "rb") as f:
                    pdf_bytes = f.read()

                st.download_button(
                    label="📥 Download Tailored Resume PDF",
                    data=pdf_bytes,
                    file_name="Akshay_Vadala_Tailored_Resume.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

                st.success("✅ Your tailored ATS-optimized resume is ready!")

        finally:
            os.unlink(tmp_path)

st.divider()
st.markdown("Built with ❤️ using Groq + LLaMA 3.3 + Streamlit")