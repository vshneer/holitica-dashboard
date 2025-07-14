from PIL import Image
import streamlit as st
vip_label = 'VIP'
others_label = 'Others'

SLOGAN="""
Connecting Marketing, Technology and Data
"""

logo = Image.open("holitica-slogan-logo.png")

def show_side_bar_with_more():
    with st.sidebar:
        st.markdown("""Request a demo [here](https://request.holitica.it/)""")
        st.image(logo)
