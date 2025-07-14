import pandas as pd
from surprise import Dataset, Reader, SVD
import streamlit as st

from shared.form import dataset_form_in_columns
from shared.const import show_side_bar_with_more

show_side_bar_with_more()
left, right = st.columns([3, 1])  # Wider left, narrower right


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
        st.write("#### What model is trying to tell?")
        st.markdown("""
        "People like you also liked this"
        or
        "You may like this product, because it's similar to others you've interacted with"
        """)
        st.write("""
        #### What actually happening?

        - We analyze patterns in customer ratings or interactions
        - We group together users with similar tastes, even if they’ve never bought the same product
        - We identify hidden connections between products — products that tend to be liked by the same type of people

            """)
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

st.markdown("---")
st.write("### What Else We Can Do")

st.markdown("""

- 🎁 **Personalized Product Recommendations** – suggest the right products for each user based on behavior  
- 🛒 **Next Best Offer Modeling** – predict what a customer is most likely to buy next  
- 🧮 **Collaborative Filtering & Content-Based Models** – depending on your data structure and product range  
- 💼 **B2B Bundle Suggestions** – recommend product kits or services based on client type or purchase patterns  
- 📊 **Recommendation System Dashboards** – monitor performance, CTRs, and customer lift over time  

If you’d like a custom recommendation engine built for your business, register [here](https://request.holitica.it/) or contact victor@holitica.it. You can also find Holitica on [LinkedIn](https://www.linkedin.com/company/holitica/).
""")
