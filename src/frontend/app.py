import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8001/copilot")

st.set_page_config(page_title="Support Ops Copilot", layout="centered")

st.title("Support Ops Copilot")
st.caption("AI-assisted support ticket triage")

st.subheader("Support Ticket")
language = st.selectbox("Language", ["English", "German"])
lang_code = "en" if language == "English" else "de"
ticket_text = st.text_area("Enter the support ticket:", height=150)

if st.button("Analyze Ticket"):
    if not ticket_text.strip():
        st.error("Please enter a support ticket.")
    else:
        with st.spinner("Analyzing ticket..."):
            try:
                response = requests.post(API_URL, json={"ticket_text": ticket_text,"language": lang_code}, timeout=30)

                if response.status_code != 200:
                    try:
                        detail = response.json().get("detail", "Unknown error")
                    except ValueError:
                        detail = "Unknown API error."
                    st.error(f"API Error: {response.status_code} - {detail}")
                else:
                    data = response.json()

                    st.subheader("Ticket Analysis")
                    col1, col2 = st.columns(2)
                    col1.metric("Category", data.get("category", "N/A"))
                    col2.metric("Priority", data.get("priority", "N/A"))

                    st.subheader("Retrieved Solutions")
                    retrieved = data.get("retrieved_tickets", [])

                    if retrieved:
                        for i, ticket in enumerate(retrieved, 1):
                            with st.expander(f"{i}. {ticket.get('category')} | Score: {ticket.get('score', 0):.2f}"):
                                st.write("**Ticket:**", ticket.get("text"))
                                st.write("**Historical Resolution:**",ticket.get("answer"))
                    else:
                        st.info("No relevant historical solutions found.")

                    st.subheader("Generated Draft")
                    st.text_area("Draft Response", data.get("draft_response", ""), height=150, disabled=True)

                    st.subheader("Guardrail Status")
                    action = data.get("guardrail_action", "UNKNOWN")
                    flags = data.get("guardrail_flags", [])

                    if action == "ALLOW":
                        st.success("Status: ALLOW")
                    elif action == "REDACT":
                        st.warning("Status: REDACT - PII was detected and redacted.")
                    elif action == "REVIEW":
                        st.warning("Status: REVIEW - Human review required.")
                    elif action == "BLOCK":
                        st.error("Status: BLOCK - Safety violation detected.")
                    else:
                        st.info(f"Status: {action}")

                    if flags:
                        st.write("Flags:", ", ".join(flags))

                    st.subheader("Final Response")
                    st.info(data.get("final_response", ""))

            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the FastAPI backend.")
            except requests.exceptions.Timeout:
                st.error("The API request timed out.")
            except requests.exceptions.RequestException as e:
                st.error(f"API request failed: {e}")