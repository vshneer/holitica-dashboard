import streamlit as st
import pandas as pd
import smtplib
from email.message import EmailMessage
import os
import smtplib
from email.message import EmailMessage
import env
import time
import re
import streamlit.components.v1 as components
import requests

CALL = """

#### 💡 Try it on Your Own Data!

"""

EMAIL_SENDER = os.getenv("EMAIL_SENDER")       # e.g., you@yourdomain.com
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")   # App password or regular password
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")   # Could be same as sender

def dataset_form_in_columns(
    right,
    default_df,
    required_columns=None,
    max_size_mb=5,
    help_text=None,
    default_name="Default dataset"
):
    """Two-column layout with dataset selection and validation on the right."""

    with right:
        st.header("🗂️ Data Source")
        choice = st.radio("Choose your dataset:", [default_name, "Upload your own"])

        if choice == default_name:
            return default_df

        uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
        if help_text:
            st.info(help_text)

        if uploaded_file is None:
            st.warning("Please upload a file.")
            return None

        # Size check
        if uploaded_file.size > max_size_mb * 1024 * 1024:
            st.error(f"File too large (limit: {max_size_mb} MB)")
            return None

        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Failed to read CSV: {e}")
            return None

        if required_columns:
            missing = [col for col in required_columns if col not in df.columns]
            if missing:
                st.error(f"Missing required columns: {', '.join(missing)}")
                return None

        st.success("✅ File successfully loaded")
        return df

def validate_uploaded_file(uploaded_file, required_columns=None, max_size_mb=5):
    """Validates uploaded CSV file for size and required columns."""
    if uploaded_file is None:
        st.warning("Please upload a file.")
        return None

    # Check size
    size_mb = uploaded_file.size / (1024 * 1024)
    if size_mb > max_size_mb:
        st.error(f"File too large: {size_mb:.2f} MB (limit is {max_size_mb} MB)")
        return None

    # Read file
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Could not read file: {e}")
        return None

    # Check columns
    if required_columns:
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            st.error(f"Missing required columns: {', '.join(missing)}")
            return None

    st.success("File successfully validated ✅")
    return df