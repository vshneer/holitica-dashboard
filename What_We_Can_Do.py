import streamlit as st

from dotenv import load_dotenv
import os
from shared.const import show_side_bar_with_more
from urllib.parse import parse_qs

show_side_bar_with_more()
st.set_page_config(page_title="Holitica")


query_params = st.experimental_get_query_params()
page = query_params.get("page", ["home"])[0]


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
- 📉 [Understanding Customer Churn](./Understanding_Customer_Churn)
- 🧩 [User Based Recommendations](./User_Based_Recommendations)

""")

st.markdown("""
Curious to see it in action? Request a demo [here](https://request.holitica.it/).

""")