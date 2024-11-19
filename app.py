import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd
from pandasai import Agent
import plotly.express as px

# Load environment variables
load_dotenv()

# Initialize API Key
openai_api_key = os.getenv("PANDASAI_API_KEY")

# Function to interact with CSV
def chat_with_csv(df, prompt):
    pandas_ai = Agent(df, api_key=openai_api_key)
    result = pandas_ai.chat(prompt)
    if isinstance(result, pd.DataFrame):
        return result
    elif isinstance(result, list) or isinstance(result, dict):
        try:
            result_df = pd.DataFrame(result)
            return result_df
        except Exception as e:
            st.error(f"Could not convert result to DataFrame: {e}")
    return result

# Main Streamlit App
def main():
    st.set_page_config(layout="wide", page_title="CSV Convo Genie", page_icon="📊")
    
    # Sidebar with Title and File Upload
    with st.sidebar:
        st.title("📊 CSV Convo Genie")
        st.markdown("Upload a CSV file to get started. Then, query it as if you're chatting!")
        input_csv = st.file_uploader("Upload CSV", type=['csv'])
        if input_csv:
            st.success("CSV Uploaded Successfully!")
        st.markdown("---")


    # Main Content
    st.title("Welcome to CSV Convo Genie! 🚀")
    st.markdown("### Unlock the power of AI to analyze your CSV data effortlessly.")
    
    if not openai_api_key:
        st.error("API Key is not set. Please configure it in the environment.")
        return

    if input_csv:
        # Load and display CSV
        data = pd.read_csv(input_csv)
        col1, col2 = st.columns([2, 3])

        with col1:
            st.subheader("🔍 Data Preview")
            st.dataframe(data, use_container_width=True)
            
            st.subheader("📊 Data Insights")
            with st.expander("View Statistics", expanded=True):
                st.write(data.describe())

        with col2:
            st.subheader("💬 Chat with your CSV")
            input_text = st.text_area("Enter your query:", placeholder="e.g., What is the average sales for each category?")

            if st.button("Ask CSV", key="ask_button"):
                if input_text:
                    with st.spinner("Analyzing your query..."):
                        result = chat_with_csv(data, input_text)
                    
                    # Display results
                    if isinstance(result, pd.DataFrame):
                        st.success("Here are the results:")
                        st.dataframe(result, use_container_width=True)

                        # Generate a scatter plot if result is numeric
                        if len(result.columns) >= 2:
                            try:
                                fig = px.scatter(result, x=result.columns[0], y=result.columns[1],
                                                 title="Query Result Visualization")
                                st.plotly_chart(fig, use_container_width=True)
                            except Exception as e:
                                st.warning("Unable to generate visualization for this result.")
                    else:
                        st.success("Here are the results:")
                        st.write(result)
                else:
                    st.warning("⚠️ Please enter a query.")
    else:
        # Prompt user to upload a file
        st.info("👈 Upload a CSV file from the sidebar to get started!")

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center;'>"
        "Built with ❤️ by Streamlit and PandasAI."
        "</div>",
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()