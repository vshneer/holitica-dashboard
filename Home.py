import streamlit as st

from shared.const import CALL, SLOGAN
from shared.form import show_email_form

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
""")


st.markdown("""
Explore real-world data use cases:

- 📊 [Retail Customer Insights](./Retail_Customer_Insights)
- 🧠 [Customer Persona Uncover](./Customer_Persona_Uncover)
- 📉 [Churn Prediction](./Churn_Prediction)

""")

st.markdown(CALL)

submission = show_email_form()

if submission:
    # Optional: log it or send to email / CSV / database
    st.write("Captured email:", submission["email"])
