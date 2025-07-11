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
RECAPTCHA_SITE_KEY = os.getenv("RECAPTCHA_SITE_KEY")
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")

def verify_recaptcha(response_token):
    secret = RECAPTCHA_SECRET_KEY
    payload = {
        'secret': secret,
        'response': response_token
    }
    r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)
    return r.json().get("success", False)

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def send_email(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    try:
        with smtplib.SMTP("smtp-relay.brevo.com", 587) as smtp:
            smtp.starttls()
            smtp.login("91cb9c001@smtp-brevo.com", EMAIL_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        st.error(f"Email failed to send: {e}")

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

def show_sidebar_form():
    with st.sidebar:
        st.markdown(CALL)
        show_email_form()

def show_email_form():
    response_token = st.query_params.get("g-recaptcha-response", [None])[0]
    with st.form("email_form"):
        st.markdown("**Leave your email and a short message:**")
        email = st.text_input("Email")
        message = st.text_area("Tell me briefly about your use case")
        # Inject HTML for reCAPTCHA
        captcha_html = f"""
        <script src="https://www.google.com/recaptcha/api.js" async defer></script>
        <div class="g-recaptcha" data-sitekey="{RECAPTCHA_SITE_KEY}"></div>
        """
        components.html(captcha_html, height=90)
        submitted = st.form_submit_button("Send")

        if submitted:
            if not is_valid_email(email):
                st.warning("Please enter a valid email.")
            elif not verify_recaptcha(response_token):
                st.error("reCAPTCHA verification failed.")
            else:
                st.success("Thanks! I’ll get back to you soon.")
                send_email(email, message)
                st.experimental_rerun()
