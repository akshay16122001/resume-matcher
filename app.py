import streamlit as st
from parser import parse_resume
from matcher import match_resume_to_jd, generate_cover_letter
import tempfile
import os

# Page config
st.set_page_config(
    page_title="AI Resume Matcher",
    page_icon="🎯",
    layout="wide"
)

# Header
st.title("🎯 AI Resume & Job Matcher")
st.markdown("**Upload your resume and paste a job description to get instant AI-powered analysis.**")
st.divider()

# Two columns layout
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
        height=200,
        placeholder="Paste the full job description here..."
    )
    company_name = st.text_input(
        "Company Name",
        placeholder="e.g. Google, Amazon, Microsoft"
    )

st.divider()

# Analyze button
if st.button("🚀 Analyze Match", type="primary", use_container_width=True):
    if not uploaded_file:
        st.error("⚠️ Please upload your resume PDF!")
    elif not jd_text:
        st.error("⚠️ Please paste a job description!")
    elif not company_name:
        st.error("⚠️ Please enter the company name!")
    else:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        try:
            # Extract resume text
            with st.spinner("📄 Reading your resume..."):
                resume_text = parse_resume(tmp_path)

            # Get match analysis
            with st.spinner("🔍 Analyzing match..."):
                analysis = match_resume_to_jd(resume_text, jd_text)

            # Display analysis
            st.subheader("📊 Match Analysis")
            st.markdown(analysis)
            st.divider()

            # Generate cover letter
            with st.spinner("✉️ Writing your cover letter..."):
                cover_letter = generate_cover_letter(
                    resume_text, jd_text, company_name
                )

            # Display cover letter
            st.subheader("✉️ Generated Cover Letter")
            st.markdown(cover_letter)

            # Download button
            st.download_button(
                label="📥 Download Cover Letter",
                data=cover_letter,
                file_name=f"cover_letter_{company_name}.txt",
                mime="text/plain",
                use_container_width=True
            )

        finally:
            # Clean up temp file
            os.unlink(tmp_path)

st.divider()
st.markdown("Built with ❤️ using Groq + LLaMA 3.3 + Streamlit")