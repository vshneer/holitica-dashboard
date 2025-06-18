import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv('rfm_merged.csv')

st.title("Retail Customer Insights")

st.write("## Customer Segments")

plt.figure(figsize=(10, 5))
sns.countplot(data=df, x='Segment', order=df['Segment'].value_counts().index)
plt.title('Customer Count by Segment')
plt.xlabel('Segment')
plt.ylabel('Number of Customers')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
