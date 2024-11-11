# Importing necessary modules
import streamlit as st
from pathlib import Path
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key1 = os.getenv('api_key1')

# Set the page configuration
st.set_page_config(page_title="VitalImage Analytics", page_icon=":robot:")

# Configure the Gemini API key
genai.configure(api_key=api_key1)

# Model configuration
generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 8192,
}

# Safety settings
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# System prompt with Dietary Recommendations
system_prompt = """
As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues.

Your Responsibilities include:
1. **Detailed Analysis**: Thoroughly analyze each image, focusing on identifying any abnormal findings.
2. **Findings Report**: Document all observed anomalies or signs of disease. Clearly articulate these findings.
3. **Recommendations and Next Steps**: Based on your analysis, suggest potential next steps, including further tests or treatments that may be required.
4. **Treatment Suggestions**: If appropriate, recommend possible treatment options or interventions.
5. **Dietary Recommendations**: Based on the identified disease or health condition, provide a list of healthy foods or dietary guidelines that could aid in managing the condition.

Guidelines:
1. Scope of Response: Only respond if the image pertains to human health issues.
2. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are "unable to determine based on the provided image."
3. Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Doctor before making any decisions."

Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis, adhering to the structured approach outlined above.

Please provide an output with these headings:
1) Detailed Analysis
2) Findings Report
3) Recommendations and Next Steps
4) Treatment Suggestions
5) Dietary Recommendations
"""

# Set up the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Set the logo
st.image("ai-assistant--that--looks-like--nurse.png", width=150)

# Set the title and subtitle
st.title("AI 🤖 SyntheMedBot: 👨‍⚕️👩‍⚕️")
st.subheader("An application that helps users analyze medical images")

# File uploader for medical image
uploaded_file = st.file_uploader("Upload the medical image for analysis", type=["png", "jpg", "jpeg"])
if uploaded_file:
    # Display the uploaded image
    st.image(uploaded_file, width=250, caption="Uploaded medical image")

submit_button = st.button("Generate Analysis")

if submit_button and uploaded_file:
    # Retrieve the uploaded image data
    image_data = uploaded_file.getvalue()
    
    # Prepare image data for the model
    image_parts = [
        {
            "mime_type": "image/jpeg",
            "data": image_data
        },
    ]
    
    # Prepare the prompt for the model
    prompt_parts = [image_parts[0], system_prompt]
    
    st.title("Here is the analysis based on the uploaded image:")
    
    # Generate response
    response = model.generate_content(prompt_parts)
    st.write(response.text)
else:
    st.warning("Please upload an image before generating the analysis.")
