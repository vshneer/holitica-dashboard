import streamlit as st

from shared.form import show_sidebar_form

show_sidebar_form()

st.set_page_config(page_title="Holitica")

st.title("Welcome to Holitica")

st.markdown("""
#### What We Can Do

We turn your data into clear, actionable insights that drive growth.
Here’s how we can help your business:

**Understand Your Customers** – segment your audience based on behavior, demographics, and value  
**Target More Effectively** – design high-performing ad audiences using real data, not guesses  
**Grow Sales with Insight** – match products, timing, and offers to the right people  
**Spot Opportunities Early** – identify trends, churn risks, and untapped market segments  
**Make Data Work for You** – from one-time reports to custom dashboards and automated predictions  

Our methods are powered by experience, common sense and machine learning. We connect Marketing, Technology and Data
""")


st.markdown("""
Explore real-world data use cases:

- 📊 [Retail Customer Insights](./Retail_Customer_Insights)
- 🧠 [Customer Persona Uncover](./Customer_Persona_Uncover)
- 📉 [Understanding Customer Churn](./Understanding_Customer_Churn)
- [User Based Recommendations](./User_Based_Recommendations)

""")

