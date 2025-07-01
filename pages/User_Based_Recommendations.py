import pandas as pd
from surprise import Dataset, Reader, SVD
import streamlit as st

from shared.form import show_sidebar_form, dataset_form_in_columns

left, right = st.columns([3, 1])  # Wider left, narrower right

show_sidebar_form()

# Load and cache data
@st.cache_data
def load_data():
    df = pd.read_csv('data/fashion_products.csv')
    return df

df_default = load_data()
# Default dataset

# Use in page logic
df = dataset_form_in_columns(
    right,
    default_df=df_default,
    required_columns=["User ID", "Product ID", "Rating"],
    help_text="File must include columns: User ID, Product ID, Rating"
)
with left:
    st.title("🛍️ Fashion Product Recommender")
    if df is not None:
        # Streamlit UI
        st.subheader("📊 Dataset Preview")
        df_display = df.reset_index(drop=True)
        df_display.index = [''] * len(df_display)
        st.dataframe(df_display.head(3))
if df is not None:
    # Prepare Surprise dataset
    reader = Reader(rating_scale=(df['Rating'].min(), df['Rating'].max()))
    data = Dataset.load_from_df(df[['User ID', 'Product ID', 'Rating']], reader)
    train_set = data.build_full_trainset()

    # Train model
    sim_options = {'name': 'cosine', 'user_based': False}
    algo = SVD()
    algo.fit(train_set)


    st.markdown("Get personalized product suggestions based on real user ratings.")

    user_ids = df['User ID'].unique()
    selected_user = st.selectbox("Select a User ID", user_ids)

    # Only compute recommendations if a user is selected
    if selected_user:
        all_items = df['Product ID'].unique()
        user_items = df[df['User ID'] == selected_user]['Product ID'].tolist()
        items_to_predict = [item for item in all_items if item not in user_items]
        predictions = [algo.predict(uid=selected_user, iid=item) for item in items_to_predict]
        top_n = [
            pred for pred in predictions
            if not pred.details['was_impossible']
        ]
        top_n = sorted(top_n, key=lambda x: x.est, reverse=True)[:5]
        st.subheader(f"Top 5 Recommendations for User {selected_user}")
        for pred in top_n:
            st.markdown(f"- **Product ID:** `{pred.iid}` — _Estimated Rating_: **{pred.est:.2f}**")
