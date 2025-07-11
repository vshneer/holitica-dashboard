import streamlit as st

from shared.form import show_sidebar_form

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
We turn data into clear insights that drive growth.
Our approach combines experience, common sense, and machine learning.
We bridge the gap between ***Marketing, Technology, and Data***.
""")


st.markdown("""
#### How we do it

We carefully prepare the data through cleaning and preprocessing.
When needed, we also build custom data pipelines and ETL jobs to ensure reliable and scalable data engineering.
We explore the data and formulate hypotheses.
Then we dive deep using statistical methods to validate or reject those hypotheses.
Iteration after iteration, we extract insights that are not only statistically valid but also practically significant.

Explore real-world data use cases — or try them out with ***your own data***:

- 📊 [Retail Customer Insights](./Retail_Customer_Insights)
- 🧠 [Customer Persona Discovery](./Customer_Persona_Discovery)
- 📉 [Understanding Customer Churn](./Understanding_Customer_Churn)
- 🧩 [User Based Recommendations](./User_Based_Recommendations)

""")

st.markdown("""
Curious to see it in action? Use the email form in the left sidebar to request a ***free demo***.

""")