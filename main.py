import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import datetime as dt

def segment_customer(row):
    if row['R_Score'] >= 5 and row['F_Score'] >= 5:
        return 'VIP'
    elif row['R_Score'] >= 4 and row['F_Score'] >= 4:
        return 'Loyal'
    elif row['R_Score'] == 5:
        return 'Recent'
    elif row['F_Score'] >= 4:
        return 'Frequent'
    elif row['M_Score'] >= 4:
        return 'Big Spender'
    else:
        return 'Others'

# Use a day after the last invoice as the reference point
df = pd.read_csv('uk-online-retail-clean.csv', index_col=0)

df['Revenue'] = df['Quantity'] * df['UnitPrice']
df['CustomerID'] = df['CustomerID'].astype(int)
# Make sure InvoiceDate is in datetime format
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
snapshot_date = df['InvoiceDate'].max() + dt.timedelta(days=1)

# Group by CustomerID and aggregate
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,  # Recency
    'InvoiceNo': 'nunique',                                   # Frequency
    'Revenue': 'sum'                                          # Monetary
})

# Rename columns for clarity
rfm.rename(columns={
    'InvoiceDate': 'Recency',
    'InvoiceNo': 'Frequency',
    'Revenue': 'Monetary'
}, inplace=True)

# Create R, F, M scores from 1 to 5
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1]).astype(int)
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)


rfm['Segment'] = rfm.apply(segment_customer, axis=1)

# Merge RFM table (with CustomerID, Segment) back to the main DataFrame
df_merged = df.merge(rfm[['Segment']], on='CustomerID')

# Total revenue per segment
segment_revenue = df_merged.groupby('Segment')['Revenue'].sum()

# Total revenue per segment
country_revenue = df_merged.groupby('Country')['Revenue'].sum()

# Total revenue across all customers
total_revenue = segment_revenue.sum()

# Fraction (as percentage)
segment_revenue_share = (segment_revenue / total_revenue * 100).round(2)

# Colors: [Others, VIP]
colors = ['#4682B4', '#FF6347']

# Segment labels
vip_label = 'VIP'
others_label = 'Others'

# Raw counts
vip_count = rfm[rfm['Segment'] == 'VIP'].shape[0]
others_count = rfm[rfm['Segment'] != 'VIP'].shape[0]
total_count = vip_count + others_count

# Convert to % share (rounded)
customer_counts_pct = [
    round(others_count / total_count * 100),
    round(vip_count / total_count * 100)
]

# Revenue share (assuming you already have these as %)
vip_revenue = round(segment_revenue_share.get('VIP', 0.0))
others_revenue = 100 - vip_revenue
revenue_contribution_pct = [others_revenue, vip_revenue]

# Labels (whole %)
customer_labels = [f"{others_label} {customer_counts_pct[0]}%", f"{vip_label} {customer_counts_pct[1]}%"]
revenue_labels = [f"{others_label} {others_revenue}%", f"{vip_label} {vip_revenue}%"]

# Plot
fig, axes = plt.subplots(1, 2, figsize=(6, 8))

axes[0].pie(customer_counts_pct, labels=customer_labels, colors=colors, startangle=90,
            wedgeprops={'width': 0.4})
axes[0].set_title('Customer Share')

axes[1].pie(revenue_contribution_pct, labels=revenue_labels, colors=colors, startangle=90,
            wedgeprops={'width': 0.4})
axes[1].set_title('Revenue Share')

st.title("Retail Customer Insights")
st.write("#### Raw Data sample")
st.caption("Dataset is made of UK-based non-store online retail transactions")
st.table(df_merged[["InvoiceNo", "Description", "Revenue", "Segment"]].head(3))
st.caption("There are other columns for customer and product ids")
st.caption("For presentation purposes data cleaning, preparation and RFM calculations are already performed")


st.write("### Let's dive in")
st.write("#### A Small Group, A Big Impact")
st.caption("10% of customers bring 37% of revenue")

# Display in Streamlit
st.pyplot(fig)


# Sort segments by count order
segment_order = rfm['Segment'].value_counts().index

fig, ax = plt.subplots(figsize=(10, 5))
sns.countplot(data=rfm, x='Segment', order=segment_order, palette='muted')

st.write("### A more detailed view on customer segments")

plt.title('Customer Count by Segment')
plt.xlabel('Segment')
plt.ylabel('Number of Customers')
plt.xticks(rotation=45)
plt.tight_layout()

# Better version using index directly
for p, segment in zip(ax.patches, segment_order):
    height = p.get_height()
    share = segment_revenue_share.get(segment, 0.0)
    ax.annotate(f'{share:.1f}%',
                (p.get_x() + p.get_width() / 2., height),
                ha='center', va='bottom', fontsize=9, color='black')
st.caption("% values represent each segment’s share of total revenue")
# Display in Streamlit
st.pyplot(fig)

st.write("#### VIPs choose different products")
st.caption("Top 10 Products Bought by VIPs vs Others. Sorted in alphabetical order")

top_vip = (
    df_merged[df_merged['Segment'] == 'VIP']
    .groupby('Description')['Quantity']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

top_others = (
    df_merged[df_merged['Segment'] != 'VIP']
    .groupby('Description')['Quantity']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

vip_products = set(top_vip.index)
other_products = set(top_others.index)

# Products only in VIPs
unique_vip = vip_products - other_products

vip_df = pd.DataFrame(top_vip.sort_index().index)


def highlight_unique(row):
    if row['Description'] in unique_vip:
        return ['background-color: #ffdddd'] * len(row)  # light red background
    else:
        return [''] * len(row)

styled_vip = vip_df.style.apply(highlight_unique, axis=1)

col1, col2 = st.columns(2)

with col1:
    st.write("### VIPs")
    st.dataframe(styled_vip)

with col2:
    st.write("### Others")
    st.dataframe(top_others.sort_index().index)


segment = st.selectbox("Select a customer segment", df_merged['Segment'].unique())
country = st.selectbox("Select a country", df_merged['Country'].unique())
group_df = df_merged[(df_merged['Segment'] == segment) & (df_merged['Country'] == country)]
top_products = (
    group_df.groupby('Description')['Quantity']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
customer_id = st.selectbox("Select a customer", df_merged[df_merged['Segment'] == segment]['CustomerID'].unique())

customer_products = df_merged[df_merged['CustomerID'] == customer_id]['Description'].unique()
recommended = top_products[~top_products.index.isin(customer_products)]
st.write("### Recommended Products for This Customer")
st.caption("Products that are popular in the group but Customer haven't tried")
st.dataframe(recommended.reset_index().rename(columns={'Description': 'Product', 'Quantity': 'Group Demand'}))

st.markdown("---")
st.write("## What Else We Can Do")

st.markdown("""
We offer tailored data analysis and modeling services to help you grow your online business.  
Here are just a few ways we can take:

- 🔍 **Advanced Customer Segmentation** – go beyond RFM with behavioral and lifecycle models
- 📦 **Product Affinity Analysis** – find which products are bought together or drive repeat purchases
- 🎯 **Campaign Targeting Optimization** – match the right product to the right customer at the right time
- 🧠 **Churn Prediction** – identify who is likely to stop buying and what you can do about it
- 📈 **Custom Dashboards** – get visual, up-to-date insights on demand

If you’d like a custom analysis on your store data, victor.shneer@gmail.com or message Holitica on LinkedIn.
""")
