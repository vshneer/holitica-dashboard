import streamlit as st

from shared.const import CALL, SLOGAN
from shared.form import show_email_form

st.set_page_config(page_title="Holitica")

st.title("Welcome to Holitica")
st.markdown("""
We analyze behavior data to help businesses target more effectively.

Explore real-world data use cases:

- 📊 [Retail Customer Insights](./Retail_Customer_Insights)
- 🧠 [Ad Persona Design](./Ad_Persona_Design)
- 📉 [Churn Prediction](./Churn_Prediction)

""")

st.markdown(CALL)

submission = show_email_form()

if submission:
    # Optional: log it or send to email / CSV / database
    st.write("Captured email:", submission["email"])
