import streamlit as st

from shared.form import show_sidebar_form
from dotenv import load_dotenv
import os

show_sidebar_form()

st.set_page_config(page_title="Holitica")

st.title("Welcome to Holitica")

st.markdown('''
#### Who we are

We’re a small team focused on data analytics, software engineering, and machine learning.

''')

st.markdown("""
#### What We Can Do

Have a question? We help you find the answer in your data.
Our approach combines experience, common sense, and machine learning.
We bridge the gap between ***Marketing, Technology, and Data***.
""")


st.markdown("""
#### Explore

use cases — or try them out with ***your own data***:

- 📊 [Retail Customer Insights](./Retail_Customer_Insights)
- 🧠 [Customer Persona Discovery](./Customer_Persona_Discovery)
- 📉 [Understanding Customer Churn](./Understanding_Customer_Churn)
- 🧩 [User Based Recommendations](./User_Based_Recommendations)

""")

st.markdown("""
Curious to see it in action? Use the email form in the left sidebar to request a ***free demo***.

""")