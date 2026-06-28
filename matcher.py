from groq import Groq
import os

try:
    import streamlit as st
    api_key = st.secrets.get("GROQ_API_KEY")
except Exception:
    api_key = None

if not api_key:
    api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)


def match_resume_to_jd(resume_text, jd_text):
    prompt = f"""
    You are a senior technical recruiter with 10+ years of experience.
    Analyze the resume and job description below carefully.
    
    RESUME:
    {resume_text}
    
    JOB DESCRIPTION:
    {jd_text}
    
    Provide a detailed analysis in this exact format:
    
    MATCH SCORE: X/100
    
    TOP MATCHING SKILLS:
    - skill 1
    - skill 2
    - skill 3
    - skill 4
    - skill 5
    
    SKILL GAPS:
    - gap 1
    - gap 2
    - gap 3
    
    IMPROVEMENT SUGGESTIONS:
    - suggestion 1
    - suggestion 2
    - suggestion 3
    
    OVERALL VERDICT:
    Write 2-3 sentences summarizing the candidate's fit for this role.
    
    Be specific, honest, and actionable.
    """

    message = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )

    return message.choices[0].message.content


def generate_cover_letter(resume_text, jd_text, company_name):
    prompt = f"""
    You are an expert career coach. Write a compelling cover letter.
    
    RESUME:
    {resume_text}
    
    JOB DESCRIPTION:
    {jd_text}
    
    COMPANY: {company_name}
    
    Requirements:
    - 3 strong paragraphs
    - Highlight top 3 matching skills with specific examples
    - Show genuine interest in the company mission
    - Professional but warm tone
    - Strong opening sentence
    - End with a confident call to action
    - Do NOT use generic phrases like "I am writing to apply"
    """

    message = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=800
    )

    return message.choices[0].message.content


def generate_ats_resume(resume_text, jd_text):
    prompt = f"""
    You are a senior ATS resume expert.
    
    ORIGINAL RESUME:
    {resume_text}
    
    JOB DESCRIPTION:
    {jd_text}
    
    Create a complete ATS-optimized resume following these rules:
    1. Keep ALL real information — name, contact, education, certifications
    2. Extract exact keywords from JD and add them naturally
    3. Rewrite bullet points to match JD language
    4. Add relevant technical skills from JD that candidate likely has
    5. Keep same structure and sections
    6. Use strong action verbs
    7. Include metrics and numbers
    
    Format EXACTLY like this:
    
    AKSHAY VADALA
    (513) 259-8742 | akshayvadalaa@gmail.com | linkedin.com/in/akshayvadala | Cincinnati, OH
    
    PROFESSIONAL SUMMARY:
    [3 sentences tailored to JD with exact keywords]
    
    CORE TECHNICAL SKILLS:
    [Category]: [skills]
    [Category]: [skills]
    [Category]: [skills]
    [Category]: [skills]
    
    WORK EXPERIENCE:
    
    Cigna | Data Analyst | Jun 2024 – Present
    • [tailored bullet using JD keywords]
    • [tailored bullet using JD keywords]
    • [tailored bullet using JD keywords]
    • [tailored bullet using JD keywords]
    • [tailored bullet using JD keywords]
    • [tailored bullet using JD keywords]
    
    Infinity Infolab | Data Analyst | Jul 2021 – Jul 2023
    • [tailored bullet using JD keywords]
    • [tailored bullet using JD keywords]
    • [tailored bullet using JD keywords]
    • [tailored bullet using JD keywords]
    • [tailored bullet using JD keywords]
    
    EDUCATION:
    University of Cincinnati — Master of Science, Information Technology | Aug 2023 – Dec 2024
    
    CERTIFICATIONS:
    • Generative AI Fundamentals — Databricks
    • Fundamentals of Data Analytics — NASSCOM
    • Advanced RPA Professional — Automation Anywhere
    
    Use real details from resume. Mirror JD keywords throughout. Keep ATS score above 90%.
    """

    message = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000
    )

    return message.choices[0].message.content


if __name__ == "__main__":
    from parser import parse_resume

    resume_text = parse_resume("Akshay_Vadala_RelaDyne_PREMIUM.pdf")

    jd_text = """
    We are looking for a Data Scientist with 3+ years of experience.
    Requirements:
    - Strong Python and SQL skills
    - Experience with machine learning models
    - Power BI or Tableau experience
    - Cloud platforms (AWS or Azure)
    - Strong communication skills
    """

    print("🔍 Analyzing your resume...\n")
    result = match_resume_to_jd(resume_text, jd_text)
    print(result)

    print("\n✨ Generating ATS resume...\n")
    ats_resume = generate_ats_resume(resume_text, jd_text)
    print(ats_resume)