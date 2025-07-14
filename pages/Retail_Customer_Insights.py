import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from shared.form import dataset_form_in_columns
from shared.rfm import build_rfm
from shared.const import show_side_bar_with_more
show_side_bar_with_more()
st.set_page_config(page_title="Retail Customer Insights")
left, right = st.columns([3, 1])  # Wider left, narrower right

@st.cache_data
def load_data():
    return pd.read_csv('data/simulated_transactions.csv')


default_df = load_data()
df = dataset_form_in_columns(
    right,
    default_df=default_df,
    required_columns=['InvoiceNo', 'Quantity', 'UnitPrice', 'CustomerID', 'InvoiceDate', 'Description'],
    help_text="File must include columns: Quantity, UnitPrice, CustomerID, InvoiceDate"
)

with left:

    if df is not None:
        ### Calculate RFM and merge
        df['Revenue'] = df['Quantity'] * df['UnitPrice']
        df['CustomerID'] = df['CustomerID'].astype(int)
        # Make sure InvoiceDate is in datetime format
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

        rfm = build_rfm(df, 'InvoiceDate', 'InvoiceNo', 'CustomerID', 'Revenue')
        # Merge RFM table (with CustomerID, Segment) back to the main DataFrame
        df_merged = df.merge(rfm[['Segment']], on='CustomerID')

        # Segment labels
        vip_label = 'VIP'
        others_label = 'Others'

        st.title("Retail Customer Insights")
        st.write("#### What we have in the data?")
        st.markdown('''
        Data features:
        - "InvoiceNo"   - order unique identifier or the invoice number 
        - "Description" - few words describing the product 
        - "Revenue"     - from the order  
        - "Segment"     - VIP customer, Loyal or Other
        - and more.. 
        
        Sample:
        ''')
        st.caption("For demonstration purposes data is simulated")
        df_display = df.reset_index(drop=True)
        df_display.index = [''] * len(df_display)
        st.dataframe(df_display.head(3))

if df is not None:
    # Calculation
    # Raw counts
    vip_count = rfm[rfm['Segment'] == 'VIP'].shape[0]
    others_count = rfm[rfm['Segment'] != 'VIP'].shape[0]
    total_count = vip_count + others_count
    # Total revenue per segment
    segment_revenue = df_merged.groupby('Segment')['Revenue'].sum()
    # Total revenue across all customers
    total_revenue = segment_revenue.sum()
    # Fraction (as percentage)
    segment_revenue_share = (segment_revenue / total_revenue * 100).round(2)
    # Revenue share (assuming you already have these as %)
    vip_revenue = round(segment_revenue_share.get(vip_label, 0.0))
    others_revenue = 100 - vip_revenue
    revenue_contribution_pct = [others_revenue, vip_revenue]
    # Convert to % share (rounded)
    customer_counts_pct = [
        round(others_count / total_count * 100),
        round(vip_count / total_count * 100)
    ]
    # Labels (whole %)
    customer_labels = [f"{others_label} {customer_counts_pct[0]}%", f"{vip_label} {customer_counts_pct[1]}%"]
    revenue_labels = [f"{others_label} {others_revenue}%", f"{vip_label} {vip_revenue}%"]

    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(6, 8))
    # Colors: [Others, VIP]
    colors = ['#4682B4', '#FF6347']

    axes[0].pie(customer_counts_pct, labels=customer_labels, colors=colors, startangle=90,
                wedgeprops={'width': 0.4})
    axes[0].set_title('Customer Share')

    axes[1].pie(revenue_contribution_pct, labels=revenue_labels, colors=colors, startangle=90,
                wedgeprops={'width': 0.4})
    axes[1].set_title('Revenue Share')


    st.write("### Let's dive in")
    st.write("#### A Small Group, A Big Impact")
    st.caption("Let's see what fraction of revenue VIP customers hold")
    st.write()
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


    ### What products VIPs prefer

    top_vip = (
        df_merged[df_merged['Segment'] == vip_label]
        .groupby('Description')['Quantity']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    top_others = (
        df_merged[df_merged['Segment'] != vip_label]
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
            return ['background-color: #FFA500'] * len(row)  # light red background
        else:
            return [''] * len(row)

    styled_vip = vip_df.style.apply(highlight_unique, axis=1)


    st.write("#### VIPs choose different products")
    st.caption("Top 10 Products Bought by VIPs vs Others. Sorted in alphabetical order")
    st.caption("Unique VIP preferences are in color")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### VIPs")
        st.dataframe(styled_vip)

    with col2:
        st.write("### Others")
        st.dataframe(top_others.sort_index().index)


    ### Recommendation

    st.write("### Recommend Products for the Customer")
    st.caption("Based on segment preferences we can build a recommendation system")

    segment = st.selectbox("Select a customer segment", df_merged['Segment'].unique())

    group_df = df_merged[(df_merged['Segment'] == segment)]
    top_products = (
        group_df.groupby('Description')['Quantity']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    customer_id = st.selectbox("Select a customer", df_merged[df_merged['Segment'] == segment]['CustomerID'].unique())

    customer_products = df_merged[df_merged['CustomerID'] == customer_id]['Description'].unique()
    recommended = top_products[~top_products.index.isin(customer_products)]

    st.caption("Products that are popular in the group but chosen Customer haven't tried")
    st.dataframe(recommended.reset_index().rename(columns={'Description': 'Product', 'Quantity': 'Group Demand'}))

st.markdown("---")
st.write("### What Else We Can Do")

st.markdown("""

- 🔍 **Advanced Customer Segmentation** – go beyond RFM with behavioral and lifecycle models
- 📦 **Product Affinity Analysis** – find which products are bought together or drive repeat purchases
- 🎯 **Campaign Targeting Optimization** – match the right product to the right customer at the right time
- 🧠 **Churn Prediction** – identify who is likely to stop buying and what you can do about it
- 📈 **Custom Dashboards** – get visual, up-to-date insights on demand

If you’d like a custom analysis on your data register [here](https://request.holitica.it/) or contact victor@holitica.it. Also you can find Holitica on [LinkedIn](https://www.linkedin.com/company/holitica/).
""")
