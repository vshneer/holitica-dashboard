import streamlit as st

# utils.py
import streamlit as st

CALL = """

#### 💡 Try This on Your Own Data!

"""

def show_sidebar_form():
    with st.sidebar:
        st.markdown(CALL)

        submission = show_email_form()

        if submission:
            st.write("📩 Captured email:", submission["email"])

def show_email_form():
    with st.form("email_form"):
        st.markdown("**Leave your email and a short message:**")
        email = st.text_input("Email")
        message = st.text_area("Tell me briefly about your use case")
        submitted = st.form_submit_button("Send")

        if submitted:
            st.success("Thanks! I’ll get back to you soon.")
            return {"email": email, "message": message}

    return None
