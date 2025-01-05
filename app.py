import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from google.generativeai import upload_file,get_file
import google.generativeai as genai


import os
from dotenv import load_dotenv
import time
from pathlib import Path
import tempfile

API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Page configuration
st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide"),    

st.title("Phidata Vedio AI Summarizer Agent :blue[cool] :sunglasses:")
st.header("Powerd by Gemini 2.0 Flash Experiance")

@st.cache_resource
def initialize_agent():
    agent = Agent(
        name="Phidata Vedio AI Summarizer Agent",
        model=Gemini(id="gemini-2.0-flash-experience"),
        tools=[DuckDuckGo()],
        instructions=["Upload a video file to get a summary of its contents."],
        show_tool_calls=True,
        markdown=True,
    )

# Initialize the agent
multimodel_agent = initialize_agent()

# file uploader

vedios_file = st.file_uploader(
    "Upload a video file", type=["mp4", "mov", "avi", "mkv", "webm"])

if vedios_file:
    with tempfile.NamedTemporaryFile(delete=False,suffix='mp4') as temp_vidios:
        temp_vidios.write(vedios_file.read())
        video_path=temp_vidios.name

    st.vidio(video_path,format='video/mp4',start_time=0)

user_query=st.text_area(
       "What would you like to know about this video?",
       placeholder="Ask a question or provide a topic to summarize",
       help="Ask a question or provide a topic to summarize",)

if st.button("Analyse Video",key="analyse_veido_button"):
    if not user_query:
        st.warning("Please provide a question or topic to summarize.")
    else:
        try:
            with st.spinner("Analyzing video..."):
            
                processed_vedio = upload_file(video_path)
            while processed_vedio.state.name=="PROCESSING":
                time.sleep(1)
                processed_vedio=get_file(processed_vedio.id)

            analysis_prompt=(f"""{user_query}""")
            response=multimodel_agent.run(analysis_prompt,vedios=[processed_vedio])

            st.subheader("Analysis")
            st.markdown(response.content)

        except Exception as error:
            st.error(f"An error occurred: {error}")
        finally:
            Path(video_path).unlink(missing_ok=True)

else:
    st.info("Click the button to start the analysis.")

st.markdown(
    """
    ---
    **Disclaimer:** This app is powered by [Gemini 2.0 Flash Experience](https://google.com).
    """,
    unsafe_allow_html=True,
)