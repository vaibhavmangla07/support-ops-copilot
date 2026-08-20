import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables (useful if API URL is configurable)
load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Support Ops Copilot",
    page_icon="🎧",
    layout="wide"
)

def render_analyzer():
    st.header("🔍 Ticket Analyzer")
    st.write("Automatically categorize and prioritize customer support tickets.")
    
    with st.form("analyze_form"):
        subject = st.text_input("Ticket Subject", placeholder="e.g. Cannot access my account")
        description = st.text_area("Ticket Description", placeholder="e.g. I have been trying to login for 3 hours but keep getting a 500 error on the main page.", height=150)
        submitted = st.form_submit_button("Analyze Ticket")
        
        if submitted:
            if not subject or not description:
                st.error("Please provide both subject and description.")
                return
                
            with st.spinner("Analyzing with LLM..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/analyze-ticket",
                        json={"subject": subject, "description": description}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.success("Analysis Complete")
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Priority", data.get("priority"))
                        col2.metric("Category", data.get("category"))
                        col3.metric("Sentiment", data.get("sentiment"))
                        
                        st.subheader("Suggested Action")
                        st.info(data.get("suggested_action"))
                        
                        st.subheader("Tags")
                        st.write(", ".join(data.get("tags", [])))
                    else:
                        st.error(f"Error from API: {response.text}")
                except Exception as e:
                    st.error(f"Failed to connect to backend: {e}")

def render_knowledge_search():
    st.header("📚 Knowledge Search")
    st.write("Search historical tickets and knowledge base articles using semantic search.")
    
    query = st.text_input("Search Query", placeholder="e.g. How to reset a password?")
    k = st.slider("Number of results", min_value=1, max_value=10, value=3)
    
    if st.button("Search", type="primary"):
        if not query:
            st.warning("Please enter a query.")
            return
            
        with st.spinner("Searching Vector Database..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/search-knowledge",
                    json={"query": query, "k": k}
                )
                
                if response.status_code == 200:
                    documents = response.json().get("documents", [])
                    st.success(f"Found {len(documents)} relevant documents.")
                    
                    for i, doc in enumerate(documents):
                        with st.expander(f"Result {i+1}", expanded=(i==0)):
                            st.write(doc)
                else:
                    st.error(f"Error from API: {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")

def main():
    st.sidebar.title("🎧 Support Ops Copilot")
    st.sidebar.markdown("---")
    
    app_mode = st.sidebar.selectbox("Choose Mode", ["Ticket Analyzer", "Knowledge Search"])
    
    st.sidebar.markdown("---")
    st.sidebar.info("A production-quality AI application designed to assist support operations. Simplicity beats complexity.")
    
    if app_mode == "Ticket Analyzer":
        render_analyzer()
    elif app_mode == "Knowledge Search":
        render_knowledge_search()

if __name__ == "__main__":
    main()
