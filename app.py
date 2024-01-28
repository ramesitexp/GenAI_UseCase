import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import PyPDF2 as pdf

load_dotenv()  #load all out environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text  

#Prompt Template 
input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System) with a deep understanding
of tech field,software engineering,data science,data analyst and big data engineer. Your task is to evaluate the resume
based on the given job description. You must consider the job market is very competitive and you should provide 
best assistance for improving the resume, Assign the percentage Matching based on Jd and missing keywords with high
accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure {{"JD match":"%"},"Missingkeywords:[]","Profile Summary":""}}
"""
st.title("Smart ATS")      
st.text("Improve Your Resume ATS") 
jd=st.text_area("Paste the job description")
uploaded_file=st.file_uploader("Upload your resume",type="pdf",help="please upload your pdf")

submit=st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt)
        st.subheader(response)
